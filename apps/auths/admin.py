from django.contrib import admin
from auths.models import CustomUser, UserHobbies

# Register your models here.


@admin.register(CustomUser)
class MainUser(admin.ModelAdmin):
    pass


@admin.register(UserHobbies)
class MainUser(admin.ModelAdmin):
    pass
