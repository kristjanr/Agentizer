from django.contrib import admin

from .models import Guide, Profile


class GuideAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name')


admin.site.register(Guide, GuideAdmin)
admin.site.register(Profile, ProfileAdmin)
