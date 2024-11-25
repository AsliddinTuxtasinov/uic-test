from django.contrib import admin

from petrol_spy.models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):

    class Meta:
        list_display = ["id", "user", "price"]
