#Realizamos las importaciones
from django.db import models
from cms.models.pagemodel import Page
from cms.models.permissionmodels import PageUser
from django.contrib.auth.models import Permission, User
from django.contrib.auth.signals import user_logged_in
from aldryn_newsblog.cms_appconfig import NewsBlogConfig
from django_auth_ldap.backend import LDAPBackend
from django.core.management.base import BaseCommand, CommandError
from cms import constants, api
from cms.constants import TEMPLATE_INHERITANCE_MAGIC
from django.utils.translation import activate
from django.dispatch import receiver

#Indicamos que vamos a utilizar la señal de cuando un usuario hace login
@receiver(user_logged_in)
#Definimos la funcion
def creasitios(sender,user,request,**kwargs):
	#Comprobamos que el usuario que se conecta no es el administrador, para evitar que se dispare el script en tal caso
	if user.username != "Administracion":
		#Indicamos que queremos utilizar el idioma español en la creacion
		activate('es')
		#Probamos a comprobar si ese usuario tiene una pagina o no
		try:
			Page.objects.get(created_by=user.username)
		#Si no la tiene pasamos a asignarle los permisos al usuario y crearle la página, ya que damos por supuesto que dicho usuario no existia
		except Page.DoesNotExist:
			#Indicamos la lista de permisos
			permisos=['Can add boostrap3 panel body plugin','Can change boostrap3 panel body plugin','Can add boostrap3 panel plugin','Can change boostrap3 panel plugin','Can add article','Can change article','Can delete article','Can add cms plugin','Can change cms plugin','Can delete cms plugin','Can add placeholder','Can change placeholder','Can delete placeholder','Can use Structure mode','Can add placeholder reference','Can change placeholder reference','Can add content type','Can change content type','Can delete content type']
			usuario=User.objects.get(username=user.username)
			#Le añadimos los permisos al usuario que estamos creando
			for ele in permisos:
				per=Permission.objects.get(name=str(ele))
				usuario.user_permissions.add(per)
			#Guardamos el usuario
			usuario.save()
			#Creamos el usuario de página
			api.create_page_user(created_by=usuario,user=usuario,can_add_page=True)
			#Creamos el blog y lo configuramos
			blog=NewsBlogConfig()
			blog.app_title=usuario.username
			blog.namespace=usuario.username
			#Guardamos el blog en nuestra base de datos
			blog.save()
			#Le creamos una página al usuario
			pagina=api.create_page(title=usuario.username,language='es',template=TEMPLATE_INHERITANCE_MAGIC,parent=None,created_by=usuario,apphook='NewsBlogApp',apphook_namespace=usuario.username) 
			#Se la asignamos
			api.assign_user_to_page(pagina,usuario,can_add=True,can_change=True,can_delete=True)
			#Publicamos la página para que sea visile por el resto de usuarios.
			pagina.publish('es')
