from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name="main_page"),
    path('about/', about, name="about"),
    path('bank_loan/', bank_loan, name='bank_loan'),
    path('bank_loan_history/<int:bank_loan_data_id>', bank_loan_history, name="bank_loan_history"),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_view, name="logout"),
    path('feedback/', feedback_view, name="feedback"),
    path('classification_project/', cv_project_view, name="clf_project"),
    path('classification_project_history/<int:data_id>', cv_project_history, name="clf_project_history"),
    path('user_page/', user_page_view, name="user_page"),
    path('edit_data/', user_data_edit_view, name="edit_data"),
    path('view_all_feedbacks/', user_feedback_view, name="user_feedback"),
    path('password_update/', password_update, name="password_update"),
    path('authentication_error/', authentication_error, name="authentication_error"),
    path('feedback_thank/', feedback_thank, name="feedback_thank"),
    path('segmentation_project', segmentation_project_view, name="seg_project"),
    path('segmentation_project_history/<int:data_id>', seg_project_history, name="seg_project_history"),
    path('CMS_project/', cms_project, name="cms_project"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
