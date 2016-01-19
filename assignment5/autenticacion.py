# -*- coding: utf-8 -*-
"""
Autores: XXX
Grupo YYY

Este código es fruto ÚNICAMENTE del trabajo de sus miembros. Declaramos no 
haber colaborado de ninguna manera con otros grupos, haber compartido el ćodigo 
con otros ni haberlo obtenido de una fuente externa.
"""

from bottle import run, post
# Resto de importaciones
import pymongo
from bottle import request, route, run, template, response, static_file
from pymongo import MongoClient 
from bson.son import SON
from bson.code import Code

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

@route('/signup', method='GET')
def signup_view():
	return template('signup');

@post('/signup')
def signup():
	username = request.forms.get('username')
	password = request.forms.get('password')
	password2 = request.forms.get('password2')	

	if password != password2:
		return template('signup-fail', message="Password doesn't match");

	result = db.users.find({ "_id": username })

	if result.count() > 0:
		return template('signup-fail', message="Username is already registered on our database");

	# Valid user. Insert it on the database.
	User = {
		"_id" : username,
		"name": request.forms.get('name'),
		"country" : request.forms.get('country'),
		"email": request.forms.get('email'),
		"password" : password
	} 

	db.users.insert_one(User);
	return template('welcome', user=User);

@post('/change_password')
def change_password():
    pass
            

@post('/login')
def login():
    pass


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
    pass
    
    
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
    pass
        

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
