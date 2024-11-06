from django.contrib import admin
from .models import Folder, UserPass, PassKey


# Register your models here.
class FolderAdmin(admin.ModelAdmin):
    # Fields to display
    list_display = ("name", "user_id")
    list_display_links = ("name",)


class UserPassAdmin(admin.ModelAdmin):
    list_display = ("name", "username", "password", "uri", "folder", "note", "user_id")
    list_display_links = ("name",)


class PassKeyAdmin(admin.ModelAdmin):
    list_display = ("user_id", "salt", "enc_key")
    list_display_links = ("user_id",)


# Initialize admin items...
admin.site.register(Folder, FolderAdmin)
admin.site.register(UserPass, UserPassAdmin)
admin.site.register(PassKey, PassKeyAdmin)
