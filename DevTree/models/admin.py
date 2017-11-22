from django.contrib import admin
from DevSky.models.models import *

class DeveloperAdmin(admin.ModelAdmin):
	#Fields for creating Developer object
	fields = ['user', 'about', 'rating']

	#Fields to display for developer
	#list_display = ('username',)


class ProjectAdmin(admin.ModelAdmin):
	#Fields for creating a Project
	fields = ['title', 'languages', 'quick_description', 'full_description', 'owner', 'developers', 'rating' ]

	#Fields to display for project
	list_display = ('title', 'owner', 'quick_description')

	#Search fields
	search_fields = ['title', 'owner']

admin.site.register(Developer, DeveloperAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(DeveloperRating)
admin.site.register(ProjectRating)
admin.site.register(DeveloperComment)
admin.site.register(ProjectComment)