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
    path("password-change/", users.UserPwdChangeView.as_view(), name="pwd_change",),
    path("password-change/done/", users.UserPwdChangeDoneView.as_view(), name="pwd_change_done"),
    # reset password urls
    # re_path(
    #     r"^password-reset/$",
    #     PasswordResetView.as_view(
    #         template_name="authnapp/password_reset.html",
    #         email_template_name="authnapp/password_reset_email.html",
    #         success_url=reverse_lazy("auth:password_reset_done"),
    #         form_class=MyPassResetForm,
    #     ),
    #     name="password_reset",
    # ),
    # re_path(
    #     r"^password-reset/done/$",
    #     PasswordResetDoneView.as_view(
    #         template_name="authnapp/password_reset_done.html",
    #     ),
    #     name="password_reset_done",
    # ),
    # re_path(
    #     r"^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$",
    #     PasswordResetConfirmView.as_view(
    #         template_name="authnapp/password_reset_confirm.html",
    #         success_url=reverse_lazy("auth:password_reset_complete"),
    #         form_class=MyPassSetForm,
    #     ),
    #     name="password_reset_confirm",
    # ),
    # re_path(
    #     r"^password-reset/complete/$",
    #     PasswordResetCompleteView.as_view(
    #         template_name="authnapp/password_reset_complete.html",
    #     ),
    #     name="password_reset_complete",
    # ),
]
