from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
# Create your models here.
class UserManager(models.Manager):
	def register(self, postData):
		errors = []
		email_taken = User.objects.filter(email = postData['email'])
		if email_taken:
			errors.append("Email is already in use. Please sign in or use a different email address")
		if len(postData['email']) < 1:
			errors.append('Email cannot be blank')
		elif not re.match(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', postData['email']):
			errors.append('email invalid')
		if len(postData['password']) < 1: 
			errors.append('Password cannot be empty')
		if not re.match(r'^(?:(?=.*[a-z])(?:(?=.*[A-Z])(?=.*[\d\W])|(?=.*\W)(?=.*\d))|(?=.*\W)(?=.*[A-Z])(?=.*\d)).{8,32}$', postData['password']):
			errors.append('Password must be at least 8 characters, have atleast one capital letter, one number, and one special character')
		elif postData['confirm_password'] != postData['password']:
			errors.append('The passwords you entered do not match')
		if len(postData['first_name']) < 1:
			errors.append('First Name cannot be blank')
		if len(postData['last_name']) < 1:
			errors.append('Last Name cannot be blank')
		if errors == []:
			encrypt_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
			User.objects.create(first_name = postData['first_name'], last_name = postData['last_name'], email = postData['email'], password = encrypt_pw)
			user_valid = User.objects.get(email = postData['email'])
			return ["valid", user_valid]
		else: 
			return ["invalid", errors]

	def login(self, postData):
		errors = []
		if len(postData['email']) < 1:
			errors.append('Email cannot be blank')
		if not re.match(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', postData['email']):
			errors.append('email invalid')
		if len(postData['password']) < 1: 
			errors.append('Password cannot be empty')
		if errors == []:
			user = User.objects.get(email = postData['email'])
			hashed = user.password
			if bcrypt.hashpw(postData['password'].encode(), hashed.encode()) == hashed:
				return ["valid", user]
			else: 
				errors.append('Invalid Password, please try again!')
				return ["invalid", errors]
		else:
			return ["invalid", errors]

class BookManager(models.Manager):
	def create_book(self, postData, id):
		errors = []
		author = postData['existing_author']
		if postData['title'] < 1:
			errors.append("Title cannot be empty")
		book_exists = Book.objects.filter(title= postData['title'])
		if book_exists:
			errors.append("This book already exists please find it on the homepage to make a review")
		if postData['existing_author'] == "none":
			author = postData['new_author']
			if len(postData['new_author']) < 1:
				errors.append("Please select an author or create a new one")
		if len(postData['review']) < 1:
			errors.append("Review field cannot be empty")
		if errors == []:
			Book.objects.create(title = postData['title'], author = author)
			user = User.objects.get(id= id)
			book = Book.objects.get(title= postData['title'])
			Review.objects.create(review = postData['review'], stars= postData['stars'], user= user, book= book)
			return ["valid", book]
		else: 
			return ["invalid", errors]

	def create_review(self, postData, bookid, userid):
		errors = []
		if len(postData['review']) < 1:
			errors.append("Review field cannot be empty")
		if errors == []:
			user = User.objects.get(id= userid)
			book = Book.objects.get(id= bookid)
			Review.objects.create(review = postData['review'], stars= postData['stars'], user= user, book= book)	
			return ["valid", book]
		else:
			return ["invalid", errors]



class User(models.Model):
	first_name = models.CharField(max_length = 100)
	last_name = models.CharField(max_length = 100)
	email = models.CharField(max_length = 100)
	password = models.CharField(max_length = 250)
	created_on = models.DateTimeField(auto_now_add = True)
	objects = UserManager()

class Book(models.Model):
	title = models.CharField(max_length = 100)
	author = models.CharField(max_length = 100)
	created_on = models.DateTimeField(auto_now_add = True)
	objects = BookManager()


class Review(models.Model):
	review = models.CharField(max_length = 1000)
	stars = models.CharField(max_length = 1)
	created_on = models.DateTimeField(auto_now_add = True)
	user = models.ForeignKey('User')
	book = models.ForeignKey('Book')











