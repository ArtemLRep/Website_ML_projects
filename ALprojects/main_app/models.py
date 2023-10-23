import os

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    work_place = models.CharField(max_length=200, verbose_name="work_place", blank=True, null=True)
    birth_date = models.DateField(verbose_name="birth_date", blank=True, null=True)

    def __str__(self):
        return str(self.username)


class ProjectNames(models.Model):
    project_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.project_name)


class HomeOwnershipCategory(models.Model):
    home_category = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.home_category


class PurposeCategory(models.Model):
    purpose_category = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.purpose_category


class ResultCategory(models.Model):
    result_cat = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.result_cat


class BankLoanData(models.Model):
    date_time = models.DateTimeField(verbose_name="date_time", auto_now_add=True)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    amount = models.FloatField(help_text="Input float value", verbose_name="amount", null=True)

    credit_score = models.IntegerField(help_text="Input integer value", verbose_name="credit score", null=True)

    term = models.PositiveIntegerField(help_text="Input integer value", verbose_name="Loan term in months", null=True)

    income = models.FloatField(help_text="Input float value", verbose_name="income", null=True)

    years_in_current_job = models.IntegerField(help_text="Input integer value", verbose_name="years on current job",
                                               null=True)

    home_ownership = models.ForeignKey(HomeOwnershipCategory, on_delete=models.CASCADE, help_text="Chose category")

    purpose = models.ForeignKey(PurposeCategory, on_delete=models.CASCADE, help_text="Chose category")

    monthly_debt = models.FloatField(help_text="Input float value", verbose_name="monthly debt", null=True)

    years_of_credit_history = models.FloatField(help_text="Input float value",
                                                verbose_name="years of credit history", null=True)

    number_of_open_accounts = models.IntegerField(help_text="Input integer value",
                                                  verbose_name="number of open accounts", null=True)

    number_of_credit_problems = models.IntegerField(help_text="Input integer value",
                                                    verbose_name="number of credit problems", null=True)

    current_credit_balance = models.FloatField(help_text="Input float value",
                                               verbose_name="current credit balance", null=True)

    maximum_open_credit = models.FloatField(help_text="Input float value",
                                            verbose_name="maximum open credit", null=True)

    bankruptcies = models.IntegerField(help_text="Input float value",
                                       verbose_name="bankruptcies", null=True)

    tax_liens = models.IntegerField(help_text="Input float value",
                                    verbose_name="tax liens", null=True)

    result = models.ForeignKey(ResultCategory, on_delete=models.CASCADE)

    def __str__(self):
        date_time = self.date_time.strftime("%Y-%m-%d")
        model_str = f"user_id: {self.user} date_time: {date_time} result: {self.result}"
        return model_str


class SwanClfResult(models.Model):
    result = models.CharField(max_length=100)

    def __str__(self):
        return self.result


class SwanImage(models.Model):
    image = models.ImageField(upload_to="swan_classification/photos/", max_length=200)

    def __str__(self):
        return self.image.url


class SwanClfData(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
    result = models.ForeignKey(SwanClfResult, on_delete=models.CASCADE)
    proba = models.FloatField(default=1)
    image_id = models.ForeignKey(SwanImage, on_delete=models.CASCADE)


class SwanSegImage(models.Model):
    image = models.ImageField(upload_to="swan_segmentation/photos/", max_length=200)

    def __str__(self):
        return self.image.url


class SwanSegMask(models.Model):
    mask = models.ImageField(upload_to="swan_segmentation/masks/", max_length=200)

    def __str__(self):
        return self.mask.url


class SwanSegResultImage(models.Model):
    res_image = models.ImageField(upload_to="swan_segmentation/result_images/", max_length=200)

    def __str__(self):
        return self.res_image.url


class SwanSegData(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
    image_id = models.ForeignKey(SwanSegImage, on_delete=models.CASCADE)
    mask_id = models.ForeignKey(SwanSegMask, on_delete=models.CASCADE)
    res_image_id = models.ForeignKey(SwanSegResultImage, on_delete=models.CASCADE)


class FeedbackTopicModel(models.Model):
    topic_cat = models.CharField(max_length=300, unique=True)

    def __str__(self):
        return str(self.topic_cat)


class FeedbackModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    topic = models.ForeignKey(FeedbackTopicModel, on_delete=models.CASCADE)
    project = models.ForeignKey(ProjectNames, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000, verbose_name="text")
    answer = models.TextField(max_length=1000, verbose_name="answer", blank=True)
    date_time_created = models.DateTimeField(verbose_name="date_time_created", auto_now_add=True)
    date_time_last_change = models.DateTimeField(verbose_name="date_time_last_change", auto_now=True)


class HistoryModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project = models.ForeignKey(ProjectNames, on_delete=models.CASCADE)
    date_time = models.DateTimeField(verbose_name="date_time", auto_now_add=True)
    result = models.CharField(max_length=100, verbose_name="result")
    data_id = models.IntegerField(blank=True, default=1)
