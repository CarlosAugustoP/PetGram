from django.apps import AppConfig


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

class UsersConfig(AppConfig):
    name = 'users'
    def ready(self):
        import users.signals