# -*- coding: utf-8 -*-
"""
Autores: XXX
Grupo YYY

Este código es fruto ÚNICAMENTE del trabajo de sus miembros. Declaramos no 
haber colaborado de ninguna manera con otros grupos, haber compartido el ćodigo 
con otros ni haberlo obtenido de una fuente externa.
""" 

from bottle import run, post, get
# Resto de importaciones
import pymongo
from bottle import request, route, run, template, response, static_file
from pymongo import MongoClient 
from bson.son import SON
from bson.code import Code
import random
import string
import hashlib
from passlib.hash import sha256_crypt

client 	= MongoClient()
db 		= client['giw']


"""
User Schema

	User = {
		"_id" : username,
		"name": name,
		"country" : country,
		"email": email,
		"password" : password
	} 

"""


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

##############
# APARTADO A #
##############

# Returns the hash
def encryptPass(password):
	return sha256_crypt.encrypt(password)

def validPassword(password, hash):
	return sha256_crypt.verify(password, hash);

@get('/signup')
def signup_view():
	return template('signup_login', signup=True);

@post('/signup')
def signup():

	username = request.forms.get('username')
	password = request.forms.get('password')
	password2 = request.forms.get('password2')	

	if password != password2:
		return template('result', message="Password doesn't match");

	result = db.users.find({ "_id": username })

	if result.count() > 0:
		return template('result', message="Username is already registered on our database");

	# Valid user to this point. Insert it on the database.

	encryptedPassword = encryptPass(password);

	User = {
		"_id" : username,
		"name": request.forms.get('name'),
		"country" : request.forms.get('country'),
		"email": request.forms.get('email'),
		"password" : encryptedPassword
	}  

	db.users.insert_one(User);
	return template('welcome', user=User);
 
@get('/change_password')
def signup_view():
	return template('change_password');

@post('/change_password')
def change_password():
 	
	username 	= request.forms.get('username')
	oldPassword = request.forms.get('oldpassword')
	newPassword = request.forms.get('newpassword')

	user = db.users.find_one({ 
		"_id" : username 
	});

	if not user: # Username doesn't exists
		return template('result', message='Usuario o contraseña incorrectos');
 
	if not validPassword(oldPassword, user['password']): # Old password doesnt match
		return template('result', message='Usuario o contraseña incorrectos');

	newPasswordEncrypted = encryptPass(newPassword);
	db.users.update_one(
		{ "_id" : username }, 
		{ "$set": { "password" : newPasswordEncrypted }
	});

	return template('result', message='Congratulations!! Password modified!!');

@get('/login')
def login_view(): 
	return template('signup_login', signup=False);

@post('/login')
def login():
	
	username = request.forms.get('username')
	password = request.forms.get('password')

	user = db.users.find_one({ 
		"_id" : username 
	});

	if not user: # Username doesn't exists
		return template('result', message='Usuario o contraseña incorrectos');
 
	if not validPassword(password, user['password']): # Old password doesnt match
	 	return template('result', message='Usuario o contraseña incorrectos');

	return template('welcome', user=user);

##############
# APARTADO B #
##############


def gen_secret():
    # Genera una cadena aleatoria de 16 caracteres a escoger entre las 26 
    # letras mayúsculas del inglés y los dígitos 2, 3, 4, 5, 6 y 7. 
    #
    # Ejemplo:
    # >>> gen_secret()
    # '7ZVVBSKR22ATNU26'
	 
    return random_char(16);
    
    
def gen_gauth_url(app_name, username, secret):
    # Genera la URL para insertar una cuenta en Google Authenticator
    #
    # Ejemplo:
    # >>> gen_gauth_url( 'GIW_grupoX', 'pepe_lopez', 'JBSWY3DPEHPK3PXP')
    # 'otpauth://totp/pepe_lopez?secret=JBSWY3DPEHPK3PXP&issuer=GIW_grupoX
    #    
    # Formato de la URL:
    # otpauth://totp/<ETIQUETA>?secret=<SECRETO>&issuer=<NOMBRE_APLICACION_WEB>
    #
    # Más información en: 
    #   https://github.com/google/google-authenticator/wiki/Key-Uri-Format
	
	gauth_url = "otpauth://totp/%s?secret=%s&issuer=%s" % (username, secret, app_name)
	return gauth_url;
        

def gen_qrcode_url(gauth_url):
    # Genera la URL para generar el código QR que representa 'gauth_url'
    # Información de la API: http://goqr.me/api/doc/create-qr-code/
    #
    # Ejemplo:
    # >>> gen_qrcode_url('otpauth://totp/pepe_lopez?secret=JBSWY3DPEHPK3PXP&issuer=GIW_grupoX')
    # 'http://api.qrserver.com/v1/create-qr-code/?data=otpauth%3A%2F%2Ftotp%2Fpepe_lopez%3Fsecret%3DJBSWY3DPEHPK3PXP%26issuer%3DGIW_grupoX'
    pass
    
@post('/signup_totp')
def signup_totp():
    pass
        
        
@post('/login_totp')        
def login_totp():
    pass

    
if __name__ == "__main__":
    run(host='localhost',port=8080,debug=True)

###############################################################################
################# Funciones auxiliares a partir de este punto #################
###############################################################################

def random_char(n):
	chars = string.ascii_uppercase + "1234567890"
	return ''.join(random.choice(chars) for x in range(n))
	
