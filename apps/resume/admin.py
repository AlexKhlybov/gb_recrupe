from django.contrib import admin
from import_export import resources

from apps.resume.models import (Courses, Education, Experience, Resume,
                                ResumeModeration, ResumeSkills)

admin.site.register(Resume)
admin.site.register(Experience)
admin.site.register(ResumeSkills)
admin.site.register(Education)
admin.site.register(Courses)
admin.site.register(ResumeModeration)


# from import_export import resources
# from import_export.fields import Field
# from import_export.widgets import ManyToManyWidget


class ResumeResource(resources.ModelResource):
    class Meta:
        model = Resume
        exclude = ('created_at', 'updated_at')


class ResumeSkillsResource(resources.ModelResource):
    class Meta:
        model = ResumeSkills
        exclude = ('id', )


class EducationResource(resources.ModelResource):
    class Meta:
        model = Education


class ExperienceResource(resources.ModelResource):
    class Meta:
        model = Experience


class CoursesResource(resources.ModelResource):
    class Meta:
        model = Courses

class ResumeModerationResource(resources.ModelResource):
    class Meta:
        model = ResumeModeration