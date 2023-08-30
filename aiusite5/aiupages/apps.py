from django.apps import AppConfig

class AiupagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'aiupages'

class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        import users.signals