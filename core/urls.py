from django.conf.urls import url
from core.views import UserRegistrationView, UserAuthenticationView, UserLogoutView, ObjectiveCreateView, \
    ObjectiveListView

app_name = 'core'
urlpatterns = [
    url(r'^auth/', include('knox.urls'))
    url(r'^objective-create/', ObjectiveCreateView.as_view(), name='objective_create'),
    url(r'^objective-list/', ObjectiveListView.as_view(), name='objective_list'),
]
