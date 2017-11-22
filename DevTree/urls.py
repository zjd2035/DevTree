from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'myproject.views.home', name='home'),
	# url(r'^blog/', include('blog.urls')),

	url(r'^admin/', include(admin.site.urls)),

	# Index - Manages sign up/login or Main Page if already authenticated
	url(r'^$', 'DevSky.models.views.Index', name='index'),

	# Logout Request - Logs the User out of current session
	(r'^logout/$', 'DevSky.models.views.LogoutRequest'),

	# Create Project - Allows the user to create a new project
	(r'^create_project/$', 'DevSky.models.views.CreateProject'),

	# Project Page - Allows users to view or edit a project
	url(r'^project/(?P<slug>.*)/$', 'DevSky.models.views.ProjectPage', name='project_page'),

	# Developer - Shows the profile/settings of a developer
	url(r'^developer/(?P<slug>.*)/$', 'DevSky.models.views.DeveloperPage', name='developer_page'),

	# Registration - Presents the user registration form
	url(r'^developer_registration/$', 'DevSky.models.views.UserRegistration'),

	# Account Recovery - Go through security process to assist user in retreiving account info
	url(r'^account_recover/$', 'DevSky.models.views.AccountRecoveryPage'),
)
