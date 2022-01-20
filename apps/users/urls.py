from django.urls import path

from apps.users import views as users

app_name = 'users'

urlpatterns = [
    path('login/', users.auth_user_view, name='login'),
    path('logout/', users.user_logout, name='logout'),
    path('registration/', users.registration, name='registration'),
    path('editemployee/', users.edit_epmloyee, name='editemployee'),
    path('editcompany/', users.edit_company, name='editcompany'),
]
