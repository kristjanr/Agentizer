from django.contrib import admin

from .models import Guide


class GuideAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email')


admin.site.register(Guide, GuideAdmin)
