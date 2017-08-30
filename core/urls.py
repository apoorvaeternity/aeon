from django.conf.urls import url
from core.views import UserRegistrationView

app_name = 'core'
urlpatterns = [
    url(r'^register/', UserRegistrationView.as_view(), name='register'),
]
