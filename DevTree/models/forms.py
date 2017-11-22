from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth import authenticate
from DevSky.models.models import *

####################
""" Form Classes """
####################

class UserRegistrationForm( ModelForm ):
	username        = forms.CharField( widget = forms.TextInput())
	email           = forms.EmailField( widget = forms.TextInput())
	first_name      = forms.CharField( widget = forms.TextInput())
	last_name       = forms.CharField( widget = forms.TextInput())
	password        = forms.CharField( widget = forms.PasswordInput( render_value=False ))
	password1       = forms.CharField( widget = forms.PasswordInput( render_value=False ))

	class Meta:
			model = Developer
			exclude = ('user', 'favorites', 'languages', 'about', 'slug', 'rating', 'page_views')

	def clean(self):
			cleaned_data = super( UserRegistrationForm, self ).clean()

			# Verify username
			if 'username' in self.cleaned_data:
					email = self.cleaned_data.get('email')
					username = self.cleaned_data.get('username')

					# Verify username is unique
					username_is_not_unique = User.objects.filter( username=cleaned_data['username'] )
					if username_is_not_unique:
							self._errors['username'] = self.error_class(['That username is already taken.'])


			# Verify email
			if 'email' in self.cleaned_data:
					email = self.cleaned_data.get('email')
					username = self.cleaned_data.get('username')

					# Verify email is unique
					email_is_not_unique = User.objects.filter(email=email).exclude(username=username).count()
					if email_is_not_unique:
							self._errors['email'] = self.error_class(['That email address is already in use.'])

			# Verify that the two passwords matched
			if 'password' in self.cleaned_data and 'password1' in self.cleaned_data and self.cleaned_data['password'] != self.cleaned_data['password1']:
					self._errors['password1'] = self.error_class(['Your passwords did not match.'])


			return cleaned_data

class LoginForm( forms.Form ):
	username        = forms.CharField( widget=forms.TextInput(attrs={'autofocus':'autofocus'}) )
	password        = forms.CharField( widget=forms.PasswordInput( render_value=False, attrs={'autocomplete':'off',}) )

	def clean(self):
			username = self.cleaned_data.get('username')
			password = self.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if not user or not user.is_active:
					self._errors['username'] = self.error_class(['Incorrect username or password.'])
					self._errors['password'] = self.error_class(['Incorrect username or password.'])
			return self.cleaned_data

class EditProfileForm( forms.Form ):
	#images         = forms._________
	languages       = forms.CharField( widget=forms.TextInput(attrs={'autocomplete':'off'}) )
	about           = forms.CharField( widget=forms.Textarea(attrs={'autocomplete':'off'}) )

class EditProjectForm( forms.Form ):
	#title                   = forms.CharField( widget=forms.TextInput(attrs={'autocomplete':'off', 'autofocus':'autofocus' }) )
	languages               = forms.CharField( widget=forms.TextInput(attrs={'autocomplete':'off'}) )
	quick_description       = forms.CharField( widget=forms.TextInput(attrs={'autocomplete':'off'}) )
	full_description        = forms.CharField( widget=forms.Textarea(attrs={'autocomplete':'off'}) )
	#lf_developer            = forms.CharField( widget=forms.Textarea(attrs={'autocomplete':'off'}) )
	developers              = forms.CharField( widget=forms.TextInput(attrs={'autocomplete':'off'}) )

""" In the switch project owner view, add switchOwnerForm = SwitchProjectOwner( this_project = ThisPorject )
	being the object referring to the project """
class SwitchProjectOwner( forms.Form ):
		def __init__( self, *args, **kwargs ):
				this_project = kwargs.pop("this_project")
				super( SwitchProjectOwner, self ).__init__( *args, **kwargs )
				self.fields['new_owner'] = forms.ModelChoiceField( queryset = this_project.developers )

class CreateProjectForm( ModelForm ):
	title                   = forms.CharField( widget=forms.TextInput(attrs={'autocomplete':'off', 'autofocus':'autofocus' }) )
	languages               = forms.CharField( widget=forms.TextInput(attrs={'autocomplete':'off'}) )
	quick_description       = forms.CharField( max_length=140, widget=forms.Textarea(attrs={'autocomplete':'off'}) )
	full_description        = forms.CharField( widget=forms.Textarea(attrs={'autocomplete':'off'}) )
	developers              = forms.CharField( widget=forms.TextInput(attrs={'autocomplete':'off'}) )

	class Meta:
			model = Project
			exclude = ('owner', 'lf_developer', 'rating', 'date', 'slug', 'page_views', 'num_rating' )

class SearchField( forms.Form ):
	query                   = forms.CharField( widget=forms.TextInput(attrs={'autocomplete':'off'}) )

	def clean(self):
			query = self.cleaned_data.get('query')

			return self.cleaned_data