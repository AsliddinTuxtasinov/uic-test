from django.contrib import admin

from petrol_spy.models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ["user", "price", "created_at"]
