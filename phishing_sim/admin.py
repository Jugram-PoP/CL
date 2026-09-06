from django.contrib import admin
from .models import Scenario, Attempt

class ScenarioAdmin(admin.ModelAdmin):
    list_display = ("subject", "sender", "is_phishing", "order")
    list_filter = ("is_phishing",)
    search_fields = ("subject", "sender")

admin.site.register(Scenario, ScenarioAdmin)
admin.site.register(Attempt)