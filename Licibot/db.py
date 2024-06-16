MYSQL = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'licibot',
        'USER': 'licibotuser',
        'PASSWORD': 'Licibot_2.0',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

############################
## COMO CREE LA BBDD
## EN LA TERMINAL 
#CREATE DATABASE licibot;
#CREATE USER 'licibotuser'@'localhost' IDENTIFIED BY 'Licibot_2.0';
#GRANT ALL PRIVILEGES ON licibot.* TO 'licibotus'@'localhost';
#FLUSH PRIVILEGES;

### CONEXION BBDD PROYECTO  ##
## INSTALAR EXTENSION DE MYSQL EN VSC ##
## CREAR CONEXION CON LOS DATOS DE MYSQL ##

#####################################
## conexion pagina web
## USUARIOS 
## USER ADMIN
## CORREO admin@gmail.com   
## Licibot@ad1
