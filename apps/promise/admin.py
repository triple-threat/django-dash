# Promise.ly -- social commitment platform
#
# Copyright (C) 2012  Promise.ly authors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
