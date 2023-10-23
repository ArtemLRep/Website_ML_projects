from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from .models import *
from django import forms


class BankLoanForm(forms.ModelForm):
    class Meta:
        model = BankLoanData
        fields = ['amount', 'term', 'credit_score',
                  'income', 'years_in_current_job', 'home_ownership',
                  'purpose', 'monthly_debt', 'years_of_credit_history',
                  'number_of_open_accounts', 'number_of_credit_problems', 'current_credit_balance',
                  'maximum_open_credit', 'bankruptcies', 'tax_liens']
        widgets = {"amount": forms.NumberInput(attrs={"class": "form-control", "min": 0,
                                                      "placeholder": 10000, "required": True
                                                      }),

                   "term": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 12 * 50,
                                                    "placeholder": 12, "required": True
                                                    }),

                   "credit_score": forms.NumberInput(attrs={"class": "form-control", "min": 0,
                                                            "placeholder": 500, "required": True
                                                            }),

                   "income": forms.NumberInput(attrs={"class": "form-control", "min": 0,
                                                      "placeholder": 500, "required": True
                                                      }),

                   "years_in_current_job": forms.NumberInput(attrs={"class": "form-control", "min": 0, "max": 70,
                                                                    "placeholder": 6, "required": True}),

                   "home_ownership": forms.Select(attrs={"required": True, "class": "form-select"}),

                   "purpose": forms.Select(attrs={"required": True, "class": "form-select"}),

                   "monthly_debt": forms.NumberInput(attrs={"class": "form-control", "min": 0,
                                                            "placeholder": 6000, "required": True}),

                   "years_of_credit_history": forms.NumberInput(attrs={"class": "form-control", "min": 0,
                                                                       "placeholder": 10, "max": 70,
                                                                       "required": True}),

                   "number_of_open_accounts": forms.NumberInput(attrs={"class": "form-control", "min": 0,
                                                                       "placeholder": 2, "required": True}),

                   "number_of_credit_problems": forms.NumberInput(attrs={"class": "form-control", "min": 0,
                                                                         "placeholder": 0, "required": True}),

                   "current_credit_balance": forms.NumberInput(attrs={"class": "form-control", "min": 0,
                                                                      "placeholder": 5000, "required": True}),

                   "maximum_open_credit": forms.NumberInput(attrs={"class": "form-control", "min": 0,
                                                                   "placeholder": 10000, "required": True}),

                   "bankruptcies": forms.NumberInput(attrs={"class": "form-control", "min": 0,
                                                            "placeholder": 0, "required": True}),

                   "tax_liens": forms.NumberInput(attrs={"class": "form-control", "min": 0,
                                                         "placeholder": 0, "required": True}),

                   }

    def clean_current_credit_balance(self):
        credit_balance = self.cleaned_data['current_credit_balance']
        if credit_balance is None:
            raise ValidationError("This field required")
        elif credit_balance > 6000:
            raise ValidationError("Input correct")
        else:
            return credit_balance


class UserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = CustomUser
        fields = ('username', 'password')


class DateForm(forms.Form):
    period = forms.ChoiceField(choices=(("Today", "Today"), ("Month", "Month"),
                                        ("Year", "Year"), ("Select period", "Select period")),
                               widget=forms.Select(attrs={"class": "form-select", "id": "period"}))
    left_date = forms.DateTimeField(widget=forms.DateInput(attrs={"type": "date", "class": "form-control",
                                                                  "id": "left_date"
                                                                  }), required=False)
    right_date = forms.DateTimeField(widget=forms.DateInput(attrs={"type": "date", "class": "form-control",
                                                                   "id": "right_date"
                                                                   }), required=False)


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = FeedbackModel
        fields = ("project", "topic", "text")
        widgets = {"project": forms.Select(attrs={"required": True, "class": "form-control"}),
                   "topic": forms.Select(attrs={"class": "form-control", "required": True}),
                   "text": forms.Textarea(attrs={"class": "form-control", "required": True}),
                   }


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"class": "form-control"}))
    work_place = forms.CharField(label="Place of work/study (optional)",
                                 widget=forms.TextInput(attrs={"class": "form-control"}),
                                 required=False)
    birth_date = forms.DateTimeField(label="Birth date (optional)",
                                     widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
                                     required=False)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'work_place', 'birth_date', 'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"class": "form-control"}))
    work_place = forms.CharField(label="Place of work/study (optional)",
                                 widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    birth_date = forms.DateField(label="Birth date (optional)",
                                 widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
                                 required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'work_place', 'birth_date')


class UpdateUserProfileForm(forms.ModelForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"class": "form-control"}))
    work_place = forms.CharField(label="Place of work/study (optional)",
                                 widget=forms.TextInput(attrs={"class": "form-control"}),
                                 required=False)
    birth_date = forms.DateField(label="Birth date (optional)",
                                 widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
                                 required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'work_place', 'birth_date')


class PasswordUpdateForm(PasswordChangeForm):
    old_password = forms.CharField(label="Old password",
                                   widget=forms.PasswordInput(attrs={"class": "form-control", "type": "password"}),
                                   required=True)
    new_password1 = forms.CharField(label="New password",
                                    widget=forms.PasswordInput(attrs={"class": "form-control", "type": "password"}),
                                    required=True)
    new_password2 = forms.CharField(label="Repeat password",
                                    widget=forms.PasswordInput(attrs={"class": "form-control", "type": "password"}),
                                    required=True)

    class Meta:
        model = CustomUser
        fields = ("old_password", "new_password1", "new_password2")


class SwanClfDataForm(forms.ModelForm):
    image = forms.ImageField(validators=[FileExtensionValidator(
        allowed_extensions=("jpg", "png"))],
        error_messages={"invalid_extension": "This format is not supported"},
        label="Input Image",
        widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = SwanClfData
        fields = ("image",)


class SwanSegDataForm(forms.ModelForm):
    image = forms.ImageField(validators=[FileExtensionValidator(
        allowed_extensions=("jpg", "png"))],
        error_messages={"invalid_extension": "This format is not supported"},
        label="Input Image",
        widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = SwanSegData
        fields = ("image",)
