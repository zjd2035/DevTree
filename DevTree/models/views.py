####################
""" Imports """
####################

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from DevSky.models.models import *
from DevSky.models.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q

####################
""" Views """
####################

def Index( request ):
	""" Create page-specific variables """
	project_new			= Project.objects.all().order_by("-date")
	project_pop			= Project.objects.all().order_by("-page_views")
	project_rat			= Project.objects.all().order_by("rating__percent", "rating__thumb_up")
	ratings 			= ProjectRating.objects.all()

	""" Create the Generic Context """
	context = { 'project_new'		:project_new,
				'project_pop'		:project_pop,
				'project_rat'		:project_rat,
				'ratings'			:ratings }

	if request.user.is_authenticated(): # User Authenticated
		""" Create current user variables """
		current_user 		= request.user.developer
		cu_favorites 		= current_user.favorites.all()
		cu_projects 		= Project.objects.filter( developers = current_user )
		cu_messages_sent 	= Message.objects.filter( author = current_user )
		cu_messages_rec 	= Message.objects.filter( receiver = current_user )	

		""" Add authenticated user variables to context """
		context['current_user']			= current_user
		context['cu_favorites']			= cu_favorites
		context['cu_projects']			= cu_projects
		context['cu_messages_sent']		= cu_messages_sent
		context['cu_messages_rec']		= cu_messages_rec

	else: # User Not Authenticated
		""" Create variables for unauthenticated user """
		loginform		= LoginForm()
		current_user	= None

		""" Login attempt """
		if request.method == 'POST' and 'login_submission' in request.POST:
			loginform = LoginForm( request.POST )

			if loginform.is_valid():

				""" Variables from login input """
				username = loginform.cleaned_data['username']
				password = loginform.cleaned_data['password']

				""" Attempt to authenticate user """
				user = authenticate( username=username, password=password )

				if user is not None: # Authentication Succeeded
					login( request, user )
					return HttpResponseRedirect('/')

		context['loginform']		= loginform
		context['current_user']		= current_user

	return render_to_response('index.html', context, context_instance=RequestContext(request))

def DeveloperPage( request, slug ):
	""" Create page-specific variables """
	user_profile 	= Developer.objects.get(slug=slug)
	up_projects 	= Project.objects.filter( developers = user_profile )
	up_rating 		= user_profile.rating
	up_about 		= user_profile.about
	up_views 		= user_profile.page_views
	up_fname		= user_profile.user.first_name
	up_lname		= user_profile.user.last_name
	up_comments		= DeveloperComment.objects.filter( developer = user_profile )

	# Convert user's languages to a string
	language_list = []
	for language in user_profile.languages.all():
		language_list.append( language.name )
	up_languages = ', '.join( language_list )

	""" Create the generic context """
	context = { 'user_profile'		:user_profile,
				'up_projects'		:up_projects,
				'up_rating'			:up_rating,
				'up_about'			:up_about,
				'up_views'			:up_views,
				'up_fname'			:up_fname,
				'up_lname'			:up_lname,
				'up_comments'		:up_comments,
				'up_languages'		:up_languages }

	if request.user.is_authenticated(): # User Authenticated
		""" Create current user variables """
		current_user 		= request.user.developer
		cu_projects 		= Project.objects.filter( developers = current_user )
		cu_favorites 		= current_user.favorites.all()
		cu_messages_sent	= None
		cu_messages_rec		= None

		if request.method == 'POST' and 'profile_edited' in request.POST:
			editprofileform = EditProfileForm( request.POST )

			if editprofileform.is_valid():
				""" Update variables from form input """
				user_profile.about 	= editprofileform.cleaned_data['about']

				""" Save the user and developer objects without language update """
				user_profile.save()

				""" Remove old language relationships """
				for language in user_profile.languages.all():
					user_profile.languages.remove( language )


				""" Add the languages from form input """
				languages_str = editprofileform.cleaned_data['languages']
				languages_str = languages_str.replace( " ", "" )
				languages_str = languages_str.split( "," )
				for language in languages_str:
					this_language = Language.objects.get_or_create( name = language )[0]
					user_profile.languages.add( this_language )

				""" Save the finalized developer object """
				user_profile.save()

				return HttpResponseRedirect(reverse('developer_page', args=(slug,)))

		""" Add context keys for Authenticated User """
		context['current_user']		= current_user
		context['cu_projects']		= cu_projects
		context['cu_favorites']		= cu_favorites
		context['cu_messages_sent']	= cu_messages_sent
		context['cu_messages_rec']	= cu_messages_rec

		""" Allow editing if current_user is viewing own profile """
		if current_user == user_profile:
			editprofileform = EditProfileForm()
			context['editprofileform'] = editprofileform

		return render_to_response('developer.html', context, context_instance=RequestContext(request))
	
	else: # User Not Authenticated
		""" Create variables for unauthenticated user """
		loginform		= LoginForm()
		current_user	= None

		""" Login attempt """
		if request.method == 'POST' and 'login_submission' in request.POST:
			loginform = LoginForm( request.POST )

			if loginform.is_valid():

				""" Variables from login input """
				username = loginform.cleaned_data['username']
				password = loginform.cleaned_data['password']

				""" Attempt to authenticate user """
				user = authenticate( username=username, password=password )

				if user is not None: # Authentication Succeeded
					login( request, user )
					return HttpResponseRedirect(reverse('developer_page', args=(slug,)))

		""" Add context variables independent of authentication """
		context['loginform']		= loginform
		context['current_user']		= current_user

		return render_to_response('developer.html', context, context_instance=RequestContext(request))


"""def SearchResults( request ):"""

def ProjectPage( request, slug ):
	""" Create page-specific variables """
	project_profile		= Project.objects.get( slug = slug )
	pp_title			= project_profile.title
	pp_quick			= project_profile.quick_description
	pp_full				= project_profile.full_description
	pp_owner			= project_profile.owner
	pp_rating			= project_profile.rating
	pp_views			= project_profile.page_views
	pp_comments			= ProjectComment.objects.filter( project = project_profile )

	# Convert project's languages to a string
	language_list = []
	for language in project_profile.languages.all():
		language_list.append( language.name )
	pp_languages = ', '.join( language_list )

	developer_list = []
	developer_edit_list = []
	for developer in project_profile.developers.all():
		developer_list.append( "<a href='/developer/" + developer.user.username + "'>" + developer.user.username + "</a>" )
		developer_edit_list.append( developer.user.username )
	pp_developers = ', '.join( developer_list )
	pp_edit_developers = ', '.join( developer_edit_list )

	""" Create the generic context """
	context = { 'project_profile'	:project_profile,
				'pp_title'			:pp_title,
				'pp_quick'			:pp_quick,
				'pp_full'			:pp_full,
				'pp_owner'			:pp_owner,
				'pp_rating'			:pp_rating,
				'pp_views'			:pp_views,
				'pp_comments'		:pp_comments,
				'pp_languages'		:pp_languages,
				'pp_developers'		:pp_developers,
				'pp_edit_developers':pp_edit_developers }

	if request.user.is_authenticated(): # User Authenticated
		""" Create current user variables """
		current_user 		= request.user.developer
		cu_projects 		= Project.objects.filter( developers = current_user )
		cu_favorites 		= current_user.favorites.all()
		cu_messages_sent	= None
		cu_messages_rec		= None

		if request.method == 'POST' and 'project_edited' in request.POST:
			editprojectform = EditProjectForm( request.POST )

			if editprojectform.is_valid():
				""" Update variables from form input """
				quick_description = editprojectform.cleaned_data['quick_description']
				full_description = editprojectform.cleaned_data['full_description']

				project_profile.quick_description = quick_description
				project_profile.full_description = full_description
				project_profile.save()

				""" Remove old language relationships """
				for language in project_profile.languages.all():
					project_profile.languages.remove( language )

				""" Add the languages from form input """
				languages_str = editprojectform.cleaned_data['languages']
				languages_str = languages_str.replace( " ", "" )
				languages_str = languages_str.split( "," )
				for language in languages_str:
					this_language = Language.objects.get_or_create( name = language )[0]
					project_profile.languages.add( this_language )

				""" Remove old developer relationships """
				for developer in project_profile.developers.all():
					project_profile.developers.remove( developer )

				""" Add the developers from form input """
				developers_str = editprojectform.cleaned_data['developers']
				developers_str = developers_str.replace( " ", "" )
				developers_str = developers_str.split( "," )
				for developer in developers_str:
					this_developer = Developer.objects.get( user__username = developer )
					project_profile.developers.add( this_developer )

				""" Save the finalized developer object """
				project_profile.save()

				return HttpResponseRedirect(reverse('project_page', args=(slug,)))

		""" Add context keys for Authenticated User """
		context['current_user']		= current_user
		context['cu_projects']		= cu_projects
		context['cu_favorites']		= cu_favorites
		context['cu_messages_sent']	= cu_messages_sent
		context['cu_messages_rec']	= cu_messages_rec

		""" Allow editing if current_user is viewing project they own """
		if current_user == project_profile.owner:
			editprojectform = EditProjectForm()
			context['editprojectform'] = editprojectform

		return render_to_response('project.html', context, context_instance=RequestContext(request))
	
	else: # User Not Authenticated
		""" Create variables for unauthenticated user """
		loginform		= LoginForm()
		current_user	= None

		""" Login attempt """
		if request.method == 'POST' and 'login_submission' in request.POST:
			loginform = LoginForm( request.POST )

			if loginform.is_valid():

				""" Variables from login input """
				username = loginform.cleaned_data['username']
				password = loginform.cleaned_data['password']

				""" Attempt to authenticate user """
				user = authenticate( username=username, password=password )

				if user is not None: # Authentication Succeeded
					login( request, user )
					return HttpResponseRedirect(reverse('project_page', args=(slug,)))

		""" Add context variables independent of authentication """
		context['loginform']		= loginform
		context['current_user']		= current_user

		return render_to_response('project.html', context, context_instance=RequestContext(request))

def CreateProject( request ):
	if request.user.is_authenticated(): # User Authenticated
		""" Create current user variables """
		current_user 		= request.user.developer
		cu_projects 		= None
		cu_favorites 		= None
		cu_messages_sent 	= None
		cu_messages_rec		= None

		""" Create the Generic Context """
		context = { 'current_user'		:current_user,
					'cu_projects'		:cu_projects,
					'cu_favorites'		:cu_favorites,
					'cu_messages_sent'	:cu_messages_sent,
					'cu_messages_rec'	:cu_messages_rec }

		""" Create page-specific variables """
		projectform = CreateProjectForm()
		
		if request.method == 'POST' and 'create_project' in request.POST:
			projectform = CreateProjectForm( request.POST )

			if projectform.is_valid():
				""" Variables from form input """
				title 				= projectform.cleaned_data['title']
				quick_description 	= projectform.cleaned_data['quick_description']
				full_description 	= projectform.cleaned_data['full_description']
				owner 				= current_user

				""" Create a new rating and view objects """
				new_rating = ProjectRating( thumb_up = 0, thumb_down = 0, percent = 0 )
				new_rating.save()
				page_views = 0

				""" Create the initial project, without languages or developers """
				this_project = Project.objects.create( title = title, quick_description = quick_description,
										full_description = full_description, owner = owner,
										rating = new_rating, page_views = page_views)
				this_project.save()

				""" Take the string input of the languages, and convert them to objects """
				languages_str = projectform.cleaned_data['languages']
				languages_str = languages_str.replace( " ", "" )
				languages_str = languages_str.split(',')
				for language in languages_str:
					this_language = Language.objects.get_or_create( name = language )[0]
					this_project.languages.add( this_language )

				""" Take the string input of the developer usernames, and convert them to objects """
				developers_str = projectform.cleaned_data['developers']
				developers_str = developers_str.replace( " ", "" )
				developers_str = developers_str.split(',')
				for dev in developers_str:
					this_developer = Developer.objects.get( user__email = dev )
					this_project.developers.add( this_developer )

				""" Save the finalized project (with languages and developers) """
				this_project.save()

				return HttpResponseRedirect(reverse('project_page', args=(this_project.slug,)))

		""" Add the projectform's current state to the context """
		context['projectform'] = projectform

		return render_to_response('create_project.html', context, context_instance=RequestContext(request))

	else: # User Not Authenticated
		messages.add_message( request, messages.INFO, "Can't create a project without a user account." )
		return HttpResponseRedirect('/')

def UserRegistration( request ):
	registerform = UserRegistrationForm()
	loginform = LoginForm()

	if request.method == 'POST' and 'register_submission' in request.POST:
		registerform = UserRegistrationForm( request.POST )

		if registerform.is_valid():

			""" Variables from form input """
			username 	= registerform.cleaned_data['username']
			email		= registerform.cleaned_data['email']
			password	= registerform.cleaned_data['password']
			first_name	= registerform.cleaned_data['first_name']
			last_name	= registerform.cleaned_data['last_name']

			""" Create default 'about' variable """
			about = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'

			""" Create and Save the Dser object """
			user = User.objects.create_user( username = username, password = password, email = email, first_name = first_name, last_name = last_name )
			user.save()

			""" Create a new Rating and View objects """
			new_rating = DeveloperRating( thumb_up = 0, thumb_down = 0, percent = 0 )
			new_rating.save()
			page_views = 0

			""" Create and Save the Developer object """
			developer = Developer( user = user, about = about, rating = new_rating, page_views = page_views )
			developer.save()

			""" Login the new user """ # Replace the auto-login with email-verification
			auto_login_user = authenticate( username = request.POST['username'],
											password = request.POST['password'])
			login( request, auto_login_user )

			""" Redirect new user to their profile """
			return HttpResponseRedirect(reverse('developer_page', args=(developer.slug,)))

	elif request.method == 'POST' and 'login_submission' in request.POST:
			loginform = LoginForm( request.POST )

			if loginform.is_valid():

				""" Variables from login input """
				username = loginform.cleaned_data['username']
				password = loginform.cleaned_data['password']

				""" Attempt to authenticate user """
				user = authenticate( username=username, password=password )

				if user is not None: # Authentication Succeeded
					login( request, user )
					return HttpResponseRedirect('/')
	
	context = { 'loginform'		: loginform,
				'registerform'	: registerform }

	return render_to_response('developer_registration.html', context, context_instance=RequestContext(request))

def AccountRecoveryPage( request ):
	context = {}

	return render_to_response('account_recover.html', context, context_instance=RequestContext(request))

def LogoutRequest( request ):
	if request.user.is_authenticated():
        # Logout the current user
		logout( request )

	return HttpResponseRedirect('/')