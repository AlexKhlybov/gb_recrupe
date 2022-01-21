from django.contrib import admin
from import_export import resources

from apps.users.models import User

admin.site.register(User)


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        exclude = ('password', )
