from django.contrib import admin
from .models import *
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.

class CustomUserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    add_fieldsets = (
        (None, {
            'fields': ('email', 'username','first_name','last_name', 'is_user', 'is_employer', 'password1', 'password2')
        }),
        ('Permissions', {
            'fields': ('is_superuser', 'is_staff')
        })
    )
    fieldsets = (
        (None, {
            'fields': ('email', 'username','first_name','last_name', 'is_user', 'is_employer', 'password')
        }),
        ('Permissions', {
            'fields': ('is_superuser', 'is_staff')
        })
    )
    list_display = ['email', 'username','first_name','last_name', 'is_user', 'is_employer','is_superuser']
    search_fields = ('email', 'username')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)

class AboutAdmin(admin.ModelAdmin):
    list_display = ['status','updated_date', 'created_date']
    list_filter = ['status']

    # def has_add_permission(self, request):
    #     return False
    # def has_delete_permission(self, request, obj=None):
    #     return False

admin.site.register(About, AboutAdmin)

class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['fullname','updated_date', 'created_date']
    list_filter = ['fullname']

admin.site.register(Testimonial, TestimonialAdmin)

class TeamAdmin(admin.ModelAdmin):
    list_display = ['fullname','updated_date', 'created_date']
    list_filter = ['fullname']

admin.site.register(Team, TeamAdmin)

class TermAdmin(admin.ModelAdmin):
    list_display = ['title','updated_date', 'created_date']
    list_filter = ['title']

admin.site.register(Term, TermAdmin)

class TagAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_filter = ['title']

admin.site.register(Tag, TagAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ['title','slug','updated_date', 'created_date']
    list_filter = ['title']
    search_fields = ['title','slug','tags', 'overview']
    prepopulated_fields = {'slug':('title',)} 
    list_editable = ['slug']

admin.site.register(Post, PostAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_filter = ['title']

admin.site.register(Category, CategoryAdmin)

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['user']
    list_filter = ['user']

admin.site.register(Employee, EmployeeAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['user']
    list_filter = ['user']

admin.site.register(Comment, CommentAdmin)

class ContactFormMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'note', 'status', 'create_at']
    list_filter = ['name']
    search_fields = ['status', 'email', 'name']

admin.site.register(ContactFormMessage, ContactFormMessageAdmin)

class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['status', 'email', 'create_at']
    list_filter = ['status']
    search_fields = ['status', 'email']

admin.site.register(ContactInfo, ContactInfoAdmin)


class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_filter = ['title']

admin.site.register(JobCategory, JobCategoryAdmin)

class CountryAdmin(admin.ModelAdmin):
    list_display = ['country']
    list_filter = ['country']

admin.site.register(Country, CountryAdmin)

class JobAdmin(admin.ModelAdmin):
    list_display = ['jobtitle','type', 'create_at', 'slug', 'country']
    list_filter = ['jobtitle']
    search_fields = ['jobtitle','city']
    list_editable = ['slug']
    prepopulated_fields = {'slug':('jobtitle',)} 

admin.site.register(Job, JobAdmin)


class EmployerAdmin(admin.ModelAdmin):
    list_display = ['user','companyname','city','create_at']
    list_display_links = ['user','city']
    list_filter = ['user','companyname']
    search_fields = ['companyname','city']

admin.site.register(Employer, EmployerAdmin)


class SettingAdmin(admin.ModelAdmin):
    list_display = ['websitename','update_at','create_at']

admin.site.register(Setting, SettingAdmin)


class AdminAdmin(admin.ModelAdmin):
    list_display = ['admin']

admin.site.register(Admin, AdminAdmin)

class SubscribeAdmin(admin.ModelAdmin):
    list_display = ['email', 'timestamp']
    list_filter = ['email']

admin.site.register(Subscribe, SubscribeAdmin)

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['employee', 'timestamp']
    list_filter = ['employee']

admin.site.register(Application, ApplicationAdmin)

class SocialAdmin(admin.ModelAdmin):
    list_display = ['email', 'created_date']
    list_filter = ['email']

admin.site.register(Social, SocialAdmin)

class IntroAdmin(admin.ModelAdmin):
    list_display = ['overview', 'timestamp']
    list_filter = ['overview']

admin.site.register(Intro, IntroAdmin)