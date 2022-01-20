from import_export import resources
from django.contrib import admin

from apps.users.models import User, EmployeeProfile

admin.site.register(User)
admin.site.register(EmployeeProfile)



class UserResource(resources.ModelResource):
    class Meta:
        model = User
        exclude = ('password', )
