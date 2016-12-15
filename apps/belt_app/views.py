from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages, sessions
from .models import User, Book, Review

# Create your views here.
def index(request):
	if "id" not in request.session:
		request.session['id'] = ''
	return render(request, 'belt_app/index.html')

def register(request):
	if request.method == "POST":
		valid_fields = User.objects.register(request.POST)
		if valid_fields[0] == "valid":
			request.session['id'] = valid_fields[1].id
			return redirect('/homepage')
		else:
			for i in valid_fields[1]:
				messages.error(request, i)
			return redirect('/')

def login(request):
	valid_login = User.objects.login(request.POST)
	if valid_login[0] == "valid":
		request.session['id'] = valid_login[1].id
		return redirect('/homepage')
	else:
		for i in valid_login[1]:
			messages.error(request, i)
		return redirect('/')

def homepage(request):
	if request.session['id'] == '':
		return redirect('/')
	context = {
	'users': User.objects.all(),
	'books': Book.objects.all(),
	'reviews': Review.objects.all()
	}
	print request.session['id']
	return render(request, 'belt_app/homepage.html', context)

def user(request, id):
	user = User.objects.get(id = id)
	context = {
	'user': user,
	'reviews': Review.objects.filter(user = user),
	'books': Book.objects.all()
	}
	return render(request, 'belt_app/userpage.html', context)

def log_out(request):
	request.session.clear()
	return redirect('/')

def add_book_review(request):
	context = {
	'books': Book.objects.all()
	}
	return render(request, 'belt_app/add.html', context)

def process_book(request):
	new_book = Book.objects.create_book(request.POST, request.session['id'])
	if new_book[0] == "invalid":
		for i in new_book[1]:
			messages.error(request, i)
		return redirect('/homepage/add')
	else:
		return redirect('/homepage')

def go_to_book(request, id):
	book = Book.objects.get(id = id)
	context = {
	'book': book,
	'reviews': Review.objects.filter(book = book)

	}
	return render(request, 'belt_app/book.html', context)

def new_review(request, id):
	valid_review = Book.objects.create_review(request.POST, id, request.session['id'])
	if valid_review[0] == "invalid":
		for i in valid_review[1]:
			messages.error(request, i)
		return redirect('/homepage/'+id) 
	else: 
		return redirect('/homepage')




















