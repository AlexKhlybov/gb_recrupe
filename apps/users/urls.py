from django.urls import path, re_path

from apps.users import views as users

app_name = 'users'

urlpatterns = [
    path('login/', users.auth_user_view, name='login'),
    path('logout/', users.user_logout, name='logout'),
    path('registration/', users.registration, name='registration'),
    path('editemployee/', users.edit_epmloyee, name='editemployee'),
    path('editcompany/', users.edit_company, name='editcompany'),
    path('editmoderator/', users.edit_moderator, name='editmoderator'),
    # change password urls
    path('password-change/', users.UserPwdChangeView.as_view(), name="pwd_change",),
    path('password-change/done/', users.UserPwdChangeDoneView.as_view(), name="pwd_change_done"),
    # reset password urls
    path('password-reset/',users.UserPwdResetView.as_view(), name="pwd_reset",),
    path('password-reset/done/', users.UserPwdResetDoneView.as_view(), name="pwd_reset_done",),
    re_path(r'^reset/$', users.UserPwdResetConfirmView.as_view(), name="pwd_reset_confirm",),
    path('reset/complete/', users.UserPwdResetCompleteView.as_view(), name="pwd_reset_complete",),
]
