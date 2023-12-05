from django.urls import path

from .views import TitofistoMediaView, TitofistoUploadView
from .settings import ENABLE_UPLOAD, UPLOAD_NAMESPACE

app_name = "titofisto"

urlpatterns = [
    path("<path:name>", TitofistoMediaView.as_view()),
]

if ENABLE_UPLOAD:
    urlpatterns.insert(
        0,
        path(
            f"{UPLOAD_NAMESPACE}/<str:slot_name>/<str:token>/",
            TitofistoUploadView.as_view(),
            name="upload",
        ),
    )
