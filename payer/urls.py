from django.urls import path
from .views import *
urlpatterns = [
    path('', upload_page, name='upload-page'),
    path('upload/', UploadView.as_view(), name='upload'),
    path('view-mappings/', view_mappings, name='view-mappings'),
    path('view-payer-details/', view_payer_details, name='view-payer-details'),
    path('view-payers/', view_payers, name='view-payers'),
    path('view-payer-groups/', view_payer_groups, name='view-payer-groups'),
    path('view-payer-mappings/', view_payer_mappings, name='view-payer-mappings'),
    path('view-payer-group-mappings/', view_payer_group_mappings, name='view-payer-group-mappings'),
]