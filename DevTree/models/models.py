####################
"""
Author: Zack Downs
Email: zack.downs17@yahoo.com
Date: July 2014
File: myproject-models.py
Description: Object definitions for myproject's OODBMS
"""
####################

from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import datetime

####################
""" Objects """
####################

class Language(models.Model):
	name 				= models.TextField()

	def __str__(self):
		return self.name

class DeveloperRating(models.Model):
	thumb_up			= models.IntegerField()
	thumb_down			= models.IntegerField()
	percent				= models.IntegerField()

	def __str__(self):
		return "<div class='rat_up'>" + str( self.thumb_up ) + "</div><div class='rat_down'>" + str( self.thumb_down ) + "</div>"

class Developer(models.Model):
	user 				= models.OneToOneField( User )
	#image field
	about				= models.TextField( blank=True )
	rating 				= models.OneToOneField( 'DeveloperRating' )
	languages			= models.ManyToManyField( 'Language', related_name='developer_language', blank=True )
	favorites			= models.ManyToManyField( 'Project', related_name='favorites', blank=True )
	slug				= models.SlugField( unique=True )
	page_views 			= models.IntegerField()


	# Overwritten save function to create custom slug
	def save( self, *args, **kwargs ):
		self.slug = slugify( self.user.username )
		super( Developer, self ).save( *args, **kwargs )


	# Return username
	def __str__(self):
		return self.user.username


class DeveloperComment(models.Model):
	content				= models.TextField()
	author				= models.ForeignKey( 'Developer', related_name='author' )
	developer			= models.ForeignKey( 'Developer' )
	date				= models.DateTimeField( 'date' )

	def __str__(self):
		return self.content


class ProjectRating(models.Model):
	thumb_up			= models.IntegerField()
	thumb_down			= models.IntegerField()
	percent				= models.IntegerField()

	def __str__(self):
		return "<div class='rat_up'>" + str( self.thumb_up ) + "</div><div class='rat_down'>" + str( self.thumb_down ) + "</div>"


class Project(models.Model):
	title 				= models.CharField( max_length = 140 )
	languages			= models.ManyToManyField( 'Language', related_name='project_language', blank=True )
	quick_description 	= models.CharField( max_length = 255 )
	full_description 	= models.TextField()
	owner				= models.ForeignKey( 'Developer', related_name='owner' )
	developers 			= models.ManyToManyField( 'Developer', related_name='developers', blank=True )
	#lf_developer 		= models.
	rating				= models.OneToOneField( 'ProjectRating' )
	date 				= models.DateTimeField( 'date' )
	slug				= models.SlugField( unique=True )
	page_views 			= models.IntegerField()

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs ):
		self.slug = slugify( self.title ) + '_' + slugify( self.owner )
		self.date = datetime.datetime.today()
		super(Project, self).save()


class ProjectImages(models.Model):
	project				= models.ForeignKey( 'Project' )
	#image				= models.ImageField(upload_to = 'project_images/', default = 'project_images/none/none.jpg')


class ProjectComment(models.Model):
	content 			= models.TextField()
	author 				= models.ForeignKey( 'Developer' )
	project 			= models.ForeignKey( 'Project' )
	date            	= models.DateTimeField( 'date' )

	def __str__(self):
		return self.content


class Message(models.Model):
	content 			= models.TextField()
	author 				= models.ForeignKey( 'Developer', related_name='message_author' )
	receiver 			= models.ForeignKey( 'Developer' )
	date				= models.DateTimeField( 'date' )

	def __str__(self):
		return self.content


class Application(models.Model):
	applicant 			= models.ForeignKey( 'Developer' )
	project 			= models.ForeignKey( 'Project' )
	language 			= models.TextField()
	comment				= models.TextField()
	date				= models.DateTimeField( 'date' )

	def __str__(self):
		return self.applicant