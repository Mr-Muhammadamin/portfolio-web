from django.contrib import admin
from django.utils.html import format_html
from .models import *

@admin.register(CostumUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email','username','is_staff')

@admin.register(AboutMe)
class AboutMeAdmin(admin.ModelAdmin):
    list_display = ('my_name','user')

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree','university','start_year','end_year')

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('position','company','start_year','end_year')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ('image', 'preview')
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px; height: auto;"/>', obj.image.url)
        return "No image"

    preview.short_description = 'Image Preview'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'client', 'service', 'project_type')
    inlines = [ProjectImageInline]

@admin.register(YoutubeVideo)
class YoutubeVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'create_at')
    search_fields = ('title', 'link')
