from django.contrib import admin

from .models import Subscription, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'role', 'first_name', 'last_name')
    search_fields = ('email', 'username', 'role', 'first_name', 'last_name')
    list_filter = ('username',)
    empty_value_display = '-пусто-'


class SubAdmin(admin.ModelAdmin):
    list_display = ('author', 'sub')
    empty_value_display = '-пусто-'


admin.site.register(Subscription, SubAdmin)
admin.site.register(User, UserAdmin)
