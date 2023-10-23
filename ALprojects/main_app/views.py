from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, update_session_auth_hash, authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from datetime import datetime
from django.core.paginator import Paginator
from torchvision.models import resnet34, ResNet34_Weights
from torchvision import transforms
from torch.nn.functional import softmax
from .torch_models import linear_clf, UNet

from torchvision.transforms import ToPILImage

from .forms import *
from .utils import *
import xgboost as xgb
from PIL import Image
import torch
import joblib
import sklearn
import pandas as pd
import numpy as np


# Create your views here.
def index(request):
    return render(request, 'main_app/index.html')


def about(request):
    title = "About"
    context = {"title": title}
    return render(request, 'main_app/about.html', context=context)


def cms_project(request):
    return render(request, 'main_app/projects_templates/CMS_project.html')


def segmentation_project_view(request):
    unet_model = UNet()
    device = "cpu"
    unet_model.load_state_dict(torch.load("main_app/static/main_app/ML_models/unet_model.pth",
                                          map_location=torch.device(device)))

    to_tensor_resize_transform = transforms.Compose([transforms.ToTensor(),
                                                     transforms.Resize(size=(272, 272), antialias=True), ])
    val_transform = transforms.Compose([transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)), ])

    to_pil = ToPILImage()

    if request.method == "POST":
        form = SwanSegDataForm(request.POST, request.FILES)
        if form.is_valid():
            img = SwanSegImage()
            img.image = form.cleaned_data["image"]

            img.save()
            image_name = img.image.name.split("/")[-1]
            image = Image.open(img.image.path)
            img_tensor = to_tensor_resize_transform(image)  # PIL image -> torch.tensor -> Resize
            if img_tensor.shape[0] != 3:
                error_msg = "Number of channels is not 3!"
                context = {"form": form, "error_msg": error_msg, "img": img}
                return render(request, 'main_app/projects_templates/seg_project.html', context=context)

            img_input = val_transform(img_tensor)  # torch.tensor -> Normalized
            img_input = torch.unsqueeze(img_input, 0)  # Input tensor to UNet Model

            output = torch.sigmoid(unet_model(img_input))
            mask = (output > 1 / 2).to(torch.float32)  # output mask of image

            mask_PIL_image = to_pil(torch.squeeze(mask))
            mask_PIL_image.save(f"media/swan_segmentation/masks/mask_{image_name}")

            mask_db = SwanSegMask()
            mask_db.mask = f"swan_segmentation/masks/mask_{image_name}"
            mask_db.save()

            segmented_img = img_tensor * mask  # Get segmented image
            segmented_img = torch.squeeze(segmented_img)

            seg_PIL_img = to_pil(segmented_img)
            seg_PIL_img.save(f"media/swan_segmentation/result_images/result_{image_name}")

            seg_img_db = SwanSegResultImage()
            seg_img_db.res_image = f"swan_segmentation/result_images/result_{image_name}"
            seg_img_db.save()

            if request.user.is_authenticated:
                print("SAVE TO DB")
                obj = form.save(commit=False)
                obj.user_id = request.user.id
                obj.image_id = img
                obj.mask_id = mask_db
                obj.res_image_id = seg_img_db
                obj.save()

                history = HistoryModel(
                    user=CustomUser.objects.get(pk=request.user.id),
                    result=seg_img_db,
                    project=ProjectNames.objects.get(pk=3),
                    data_id=obj.pk
                )
                history.save()

            context = {"form": form, "img": img, "seg_img": seg_img_db}
            return render(request, 'main_app/projects_templates/seg_project.html', context=context)
    else:
        form = SwanSegDataForm()
    context = {"form": form}
    return render(request, 'main_app/projects_templates/seg_project.html', context=context)


def seg_project_history(request, data_id):
    data = SwanSegData.objects.get(pk=data_id)
    image = data.image_id
    res_img = data.res_image_id
    context = {"img": image, "res_img": res_img, "data": data}
    return render(request, "main_app/seg_history.html", context=context)


def cv_project_view(request):
    to_tensor_transform = transforms.Compose([transforms.ToTensor()])
    val_transform = transforms.Compose([transforms.Resize(size=(224, 224), antialias=True),
                                        transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)), ])

    device = "cpu"
    resnet34_model = resnet34(weights=ResNet34_Weights.DEFAULT).to(device)
    resnet34_model.fc = linear_clf
    resnet34_model.load_state_dict(torch.load('main_app/static/main_app/ML_models/resnet34_pretrained_model.pth',
                                              map_location=torch.device(device)))

    resnet34_model.eval()
    if request.method == "POST":
        form = SwanClfDataForm(request.POST, request.FILES)
        if form.is_valid():
            img = SwanImage()
            img.image = form.cleaned_data["image"]

            img.save()

            image = Image.open(img.image.path)
            image_processed = to_tensor_transform(image)

            if image_processed.shape[0] != 3:
                error_msg = "Number of channels is not 3!"
                context = {"form": form, "error_msg": error_msg, "img": img}
                return render(request, 'main_app/projects_templates/clf_project.html', context=context)

            image_processed = torch.unsqueeze(val_transform(image_processed), 0)
            out = softmax(resnet34_model(image_processed), 1)
            arg_max = torch.argmax(out).item()
            proba = out[0][arg_max].item()
            if proba > 0.1:
                swan_pk = arg_max
            else:
                swan_pk = 3
            result = SwanClfResult.objects.get(pk=swan_pk)

            if request.user.is_authenticated:
                obj = form.save(commit=False)
                obj.result = result
                obj.user_id = request.user.id
                obj.image_id = img
                obj.proba = proba
                obj.save()

                history = HistoryModel(
                    user=CustomUser.objects.get(pk=request.user.id),
                    result=result,
                    project=ProjectNames.objects.get(pk=2),
                    data_id=obj.pk
                )
                history.save()

            proba = round(proba * 100, 3)
            print(proba)
            context = {"form": form, "img": img, "result": result, "proba": proba}

            return render(request, 'main_app/projects_templates/clf_project.html', context=context)
    else:
        form = SwanClfDataForm()

    context = {"form": form}
    return render(request, 'main_app/projects_templates/clf_project.html', context=context)


def cv_project_history(request, data_id):
    data = SwanClfData.objects.prefetch_related("result").get(pk=data_id)
    img = data.image_id
    proba = round(data.proba * 100, 2)
    print(proba)
    context = {"img": img, "data": data, "proba": proba}
    return render(request, "main_app/clf_history.html", context)


@login_required(login_url=reverse_lazy("authentication_error"))
def feedback_thank(request):
    title = "Feedback thank"
    context = {"title": title}
    return render(request, "main_app/feedback_thank.html", context=context)


def authentication_error(request):
    title = "Authentication Required"
    context = {"title": title}
    return render(request, 'main_app/authentication_required.html', context=context)


@login_required(login_url=reverse_lazy("authentication_error"))
def feedback_view(request):
    if request.method == "POST":
        feedback_form = FeedbackForm(request.POST)
        if feedback_form.is_valid():
            obj = feedback_form.save(commit=False)
            obj.user_id = request.user.id
            obj.save()
            return redirect(reverse_lazy("feedback_thank"))
    else:
        feedback_form = FeedbackForm()
    title = "Feedback"
    context = {"feedback_form": feedback_form, "title": title}
    return render(request, 'main_app/feedback.html', context=context)


@login_required(login_url=reverse_lazy("authentication_error"))
def user_page_view(request):
    user_id = request.user.id
    page = request.GET.get("page")
    if request.method == "POST":
        page = 1
        date_form = DateForm(request.POST)
        if date_form.is_valid():
            period = date_form.cleaned_data["period"]
            if period == "Today":
                left_date = datetime.today().replace(minute=0, hour=0, second=0)
                right_date = datetime.today().replace(minute=59, hour=23, second=59)
            else:
                left_date = date_form.cleaned_data["left_date"]
                right_date = date_form.cleaned_data["right_date"].replace(minute=59, hour=23, second=59)
            t1 = HistoryModel.objects.filter(user_id=user_id,
                                             date_time__gte=left_date,
                                             date_time__lte=right_date).order_by("-date_time")
        else:
            t1 = HistoryModel.objects.filter(user_id=user_id).order_by("-date_time")
    else:
        date_form = DateForm()
        t1 = HistoryModel.objects.filter(user_id=user_id).order_by("-date_time")

    paginate_by = 10
    paginator = Paginator(t1, paginate_by)
    table_paginator = paginator.get_page(page)

    page_range = paginator.page_range

    feedback_data = FeedbackModel.objects.filter(user_id=user_id).order_by("-date_time_last_change")[:10]

    title = "Account"

    context = {"table_paginator": table_paginator,
               "date_form": date_form, "page_range": page_range,
               "feedback_data": feedback_data, "title": title
               }

    return render(request, 'main_app/user_menu.html', context=context)


def bank_loan(request):
    columns_names = ['Current Loan Amount', 'Term', 'Credit Score', 'Annual Income',
                     'Years in current job', 'Home Ownership', 'Purpose', 'Monthly Debt',
                     'Years of Credit History', 'Number of Open Accounts',
                     'Number of Credit Problems', 'Current Credit Balance',
                     'Maximum Open Credit', 'Bankruptcies', 'Tax Liens']
    columns_input_relation = {"Current Loan Amount": "amount", "Term": "term", "Credit Score": "credit_score",
                              "Annual Income": "income", "Years in current job": "years_in_current_job",
                              "Home Ownership": "home_ownership", "Purpose": "purpose",
                              "Monthly Debt": "monthly_debt", "Years of Credit History": "years_of_credit_history",
                              "Number of Open Accounts": "number_of_open_accounts",
                              "Number of Credit Problems": "number_of_credit_problems",
                              "Current Credit Balance": "current_credit_balance",
                              "Maximum Open Credit": "maximum_open_credit", "Bankruptcies": "bankruptcies",
                              "Tax Liens": "tax_liens"
                              }
    labels = ["Not approved", "Approved"]
    result = -1
    valid = False
    if request.method == "POST":
        form = BankLoanForm(request.POST)
        valid = form.is_valid()
        if valid:
            input_data = form.cleaned_data
            input_data["term"] = term_transformer(input_data["term"])
            input_data["years_in_current_job"] = years_in_current_job_transformer(input_data["years_in_current_job"])
            input_data["home_ownership"] = str(input_data["home_ownership"])
            input_data["purpose"] = str(input_data["purpose"])
            row = pd.DataFrame(columns=columns_names, index=[0])

            for col in row.columns:
                row[col] = input_data[columns_input_relation[col]]

            pipeline = joblib.load("main_app/static/main_app/ML_models/bank_loan_model_pipeline.pkl")

            proba = pipeline.predict_proba(row)[:, 1]
            result_pk = (proba > 1 / 2)[0]
            result = ResultCategory.objects.get(pk=int(result_pk))
            if request.user.is_authenticated:
                obj = form.save(commit=False)
                obj.result = result
                obj.user_id = request.user.id
                obj.save()
                history = HistoryModel(
                    user=CustomUser.objects.get(pk=request.user.id),
                    result=ResultCategory.objects.get(pk=int(result_pk)),
                    project=ProjectNames.objects.get(pk=1),
                    data_id=obj.pk
                )
                history.save()

        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
    else:
        form = BankLoanForm()

    title = "Bank Loan project"
    context = {"form": form, "labels": labels, "title": title,
               "valid": valid, "result": result}
    return render(request, 'main_app/projects_templates/bank_loan.html', context)


def bank_loan_history(request, bank_loan_data_id):
    data = BankLoanData.objects.prefetch_related("purpose", "home_ownership", "result").get(pk=bank_loan_data_id)
    context = {"data": data}
    return render(request, "main_app/bank_loan_history.html", context=context)


class RegisterUser(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'main_app/sign_up.html'
    title = "Registration"
    success_url = reverse_lazy('main_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def form_valid(self, form):
        form.save()
        username = self.request.POST["username"]
        password = self.request.POST["password1"]
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)
        return redirect(self.success_url)

    def form_invalid(self, form):
        return super().form_invalid(form)


class LoginUser(LoginView):
    form_class = UserAuthenticationForm
    template_name = 'main_app/sign_in.html'
    title = "Authorization"

    def get_success_url(self):
        return reverse_lazy('main_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def form_invalid(self, form):
        return super().form_invalid(form)


def logout_view(request):
    logout(request)
    return redirect('main_page')


@login_required(login_url=reverse_lazy("authentication_error"))
def user_feedback_view(request):
    user_id = request.user.id
    feedbacks = FeedbackModel.objects.filter(user_id=user_id).order_by('-date_time_last_change')

    paginate_by = 5
    paginator = Paginator(feedbacks, paginate_by)

    page = request.GET.get("page")

    page_obj = paginator.get_page(page)
    for page in page_obj:
        print(page.id)
    context = {"page_obj": page_obj}
    return render(request, "main_app/user_feedback.html", context=context)


@login_required(login_url=reverse_lazy("authentication_error"))
def user_data_edit_view(request):
    if request.method == "POST":
        form = UpdateUserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("user_page")
        else:
            for field in form:
                print(field.name, field.errors)
    else:
        form = UpdateUserProfileForm(instance=request.user)

    context = {"form": form}
    return render(request, 'main_app/user_edit_data.html', context=context)


@login_required(login_url=reverse_lazy("authentication_error"))
def password_update(request):
    if request.method == "POST":
        form = PasswordUpdateForm(request.user, request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('user_page')
        else:
            for field in form:
                print(field.name, field.errors)
    else:
        form = PasswordUpdateForm(request.user)

    context = {"form": form}

    return render(request, "main_app/change_password.html", context=context)
