from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.main.urls', namespace='main')),
    path('users/', include('apps.users.urls', namespace='user')),
    path('news/', include('apps.news.urls', namespace='news')),
    path('companies/', include('apps.companies.urls', namespace='companies')),
    path('vacancies/', include('apps.vacancies.urls', namespace='vacancies')),
    path('resume/', include('apps.resume.urls', namespace='resume')),
    path('notify/', include('apps.notify.urls', namespace='notify')),
    path('moderation/', include('apps.moderation.urls', namespace='moderation')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
