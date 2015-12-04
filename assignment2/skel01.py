# -*- coding: utf-8 -*-
"""
Autores: XXX
Grupo YYY

Este código es fruto ÚNICAMENTE del trabajo de sus miembros. Declaramos no haber
colaborado de ninguna manera con otros grupos, haber compartido el ćodigo con
otros ni haberlo obtenido de una fuente externa.
"""

dbName = 'giw';

from bottle import post, get, request, route, run, template, static_file
import pymongo
import json
from pymongo import MongoClient # install MongoClient
from pymongo import ReturnDocument

client = MongoClient()
db = client['giw']
users = db['users']

#####################################
########## ASSETS ROUTING ###########
#####################################

@route('/views/<filepath:path>')
def file_stac(filepath):
    return static_file(filepath, root="./views")

@route('/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='static/')

@route('/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='static/')

@route('/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='static/')

@route('/<filename:re:.*\.(eot|ttf|woff|svg)>')
def fonts(filename):
    return static_file(filename, root='static/')

# ¡MUY IMPORTANTE!
# Todas las inserciones se deben realizar en la colección 'users' dentro de la
# base de datos 'giw'.

@get('/')
def registerUser():
	return template('register_user');

@post('/add_user')
def add_user_post():
	
	try:
		userID = str(request.forms.get('_id'));
		users.insert({
			'_id' : str(request.forms.get('_id')),
			'country': str(request.forms.get('country')),
			'zip': str(request.forms.get('zip')),
			'email': str(request.forms.get('email')),
			'gender': str(request.forms.get('gender')),
			'likes': str(request.forms.get('likes')).split(','), # Create array of strings.
			'password': str(request.forms.get('password')), 
			'year': str(request.forms.get('year'))
		});
		return template('result', message="[ Good ] The user was created :-)")

	except pymongo.errors.DuplicateKeyError, e:
		if (pymongo.errors.DuplicateKeyError):
			print "This user already exists!"

	# User exists already on the database. 
	return template('result', message="[ BAD ] Your user exists on our database")

# Display user profile.
@get('/<userID>')
def registerUser(userID):
	cursor = db.users.find({
		'_id' : userID
	});
	user = cursor[0]
	return template('profile', user=user);

@route('/edit')
def editUser_info_view():
	userID = str(request.forms.get('_id'));
	cursor = db.users.find({
		'_id' : userID
	});

	if (cursor.count() == 0):
		return "No user with that name"
	else:
		user = cursor[0] # python dictionary from a user
		return template('change_email', user=user);

@post('/change_email')
def change_email():

	_id 	= request.forms.get('_id')
	email 	= str(request.forms.get('email'))

	try:
		updatedUser = users.find_one_and_update(
			{'_id':_id},
			{'$set' : {'email':email}},
			return_document=ReturnDocument.AFTER
		);
		return template('profile', user=updatedUser);
	except ValueError:
		print "Email coudln't change"
		print ValueError

	# User exists already on the database. 
	return template('result', message="[ BAD ] Your user exists on our database")

@post('/insert_or_update')
def insert_or_update():
    pass


@post('/delete')
def delete_id():

	_id = str(request.forms.get('_id'));

	deleted = users.find_one_and_delete({'_id': _id});
	
	if deleted != None:
		return template('result', message="User deleted successfully!");
	
	return template('result', message="User doesn't exist!");

@post('/delete_year')
def delete_year():
    pass

@route('/*')
def error():
	return "Not found"

run(host='127.0.0.1', port=3000);

