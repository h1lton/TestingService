from django.urls import path

from tests.views import *

urlpatterns = [
    path('', TestListView.as_view(), name='home'),

    path('test/<int:test_id>', test_view, name='test'),
    path('test/<int:test_id>/start-over', start_over, name='start_over'),

    path('login', LoginUser.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register'),
    path('logout', logout_user, name='logout'),
]
