from django.contrib import admin

from models import Promise, Profile


class PromiseAdmin(admin.ModelAdmin):
    list_display = ('creator', 'text', 'status', 'deadline', 'supporters')
    list_filter = ('creator', 'status')
    search_fields = ['creator__user', 'text']
    ordering = ('-id',)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ['user__username']

admin.site.register(Promise, PromiseAdmin)
admin.site.register(Profile, ProfileAdmin)
