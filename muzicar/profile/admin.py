from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from profile.models import User, Instrument, Region, Interest, Genre
 
 
class UserCreationForm(UserCreationForm):
    class Meta:
        model = User

class UserChangeForm(UserChangeForm):
    class Meta:
        model = User

class UserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm


admin.site.register(User, UserAdmin)
admin.site.register(Instrument)
admin.site.register(Genre)
admin.site.register(Interest)
admin.site.register(Region)