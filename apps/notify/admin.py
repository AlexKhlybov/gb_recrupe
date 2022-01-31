from import_export import resources

from django.contrib import admin

from apps.notify.models import Notify, NotifyTemplate, SMTPAccount


@admin.register(SMTPAccount)
class SMTPAccountAdmin(admin.ModelAdmin):
    list_display = ("__str__", "is_active")


@admin.register(Notify)
class NotifyAdmin(admin.ModelAdmin):
    list_display = ("__str__", "type", "event", "user", "email", "created_at", "send_at", "sent_at")

    readonly_fields = ("created_at",)
    list_filter = ("event", "type")
    search_fields = ("subject", "text")
    raw_id_fields = ("user",)


@admin.register(NotifyTemplate)
class NotifyTemplateAdmin(admin.ModelAdmin):
    change_form_template = "notify/send_notify.html"
    fields = (
        "title",
        "is_active",
        "subject",
        "text",
        "user",
        "email",
        "type",
        "event",
        "send_at",
    )
    list_display = ("title", "is_active", "type", "event", "user", "email", "send_at")
    list_filter = ("type", "event", "is_active")


class SMTPAccountResource(resources.ModelResource):
    class Meta:
        model = SMTPAccount
class NotifyTemplateResource(resources.ModelResource):
    class Meta:
        model = NotifyTemplate
