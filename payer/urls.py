from django.urls import path
from .views import upload_page, UploadView

urlpatterns = [
    path('', upload_page, name='upload-page'),  
    path('upload/', UploadView.as_view(), name='upload'),
]