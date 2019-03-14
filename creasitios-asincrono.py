#Realizamos las importaciones pertinentes
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


@receiver(user_logged_in)
class Command(BaseCommand):
	
	def add_arguments(self, parser):
		#Indicamos que evamos a introducir un parametro al comando, el cual será el nombre de nuestro usuario
		parser.add_argument('user',type=str)
		 
	def handle(self, *args, **options):
		#Activamos el idioma que queremos que utilice en nuestro sitio
		activate('es')
		#Guardamos el parametro de usuario que hemos pasado anteriormente en una variable
		usr=options['user']
		#Introducimos una lista con todos los permisos genericos que tendrá dicho usuario
		permisos=['Can add boostrap3 panel body plugin','Can change boostrap3 panel body plugin','Can add boostrap3 panel plugin','Can change boostrap3 panel plugin','Can add article','Can change article','Can delete article','Can add cms plugin','Can change cms plugin','Can delete cms plugin','Can add placeholder','Can change placeholder','Can delete placeholder','Can use Structure mode','Can add placeholder reference','Can change placeholder reference','Can add content type','Can change content type','Can delete content type']
	
		usuario=LDAPBackend().populate_user(usr)
		#Comprobamos si el usuario existe o no en LDAP
		if usuario is None:
			self.stdout.write(self.style.SUCCESS('No existe el usuario en LDAP.'))
		else:
			#Asignamos los permisos al usuario
			for ele in permisos:
				per=Permission.objects.get(name=str(ele))
				usuario.user_permissions.add(per)
			usuario.save()
			#Comprobamos si existe la página del usuario	
			try:
				Page.objects.get(created_by=usuario)

			except Page.DoesNotExist:
				#Creamos un Page User
				api.create_page_user(created_by=usuario,user=usuario,can_add_page=True)
				#Creamos el blog del usuario
				blog=NewsBlogConfig()
				blog.app_title=usuario.username
				blog.namespace=usuario.username
				blog.save()
				#Creamos la pagina del usuario.
				pagina=api.create_page(title=usuario.username,language='es',template=TEMPLATE_INHERITANCE_MAGIC,parent=None,created_by=usuario,apphook='NewsBlogApp',apphook_namespace=usuario.username) 
				#Asignamos los permisos que tendra el usuario sobre su pagina.
				api.assign_user_to_page(pagina,usuario,can_add=True,can_change=True,can_delete=True)
				#Publicamos la pagina
				pagina.publish('es')
				self.stdout.write(self.style.SUCCESS('Creacion de usuario finalizada con sus respectivos añadidos.'))

			else:
				self.stdout.write(self.style.SUCCESS('El usuario ya tiene páginas en su propiedad.'))

	print "Usuario conectado"
#user_logged_in.connect(creasitios(user))