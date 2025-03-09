
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Professor, Module, ModuleInstance, Rating

User = get_user_model()  # 获取自定义用户模
if not admin.site.is_registered(User):  # ✅ 只在未注册时才注册
    @admin.register(User)
    class CustomUserAdmin(UserAdmin):
        model = User
        list_display = ("username", "email", "is_staff", "is_active")
        search_fields = ("username", "email")
        ordering = ("username",)

admin.site.register(Professor)
admin.site.register(Module)
admin.site.register(ModuleInstance)
admin.site.register(Rating)
