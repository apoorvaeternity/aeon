from django.conf.urls import url
from core.views import UserRegistrationView, UserAuthenticationView

app_name = 'core'
urlpatterns = [
    url(r'^register/', UserRegistrationView.as_view(), name='register'),
    url(r'^login/', UserAuthenticationView.as_view(), name='login'),
]
