from django.contrib.auth.backends import ModelBackend
from .models import Author

class AuthorBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            author = Author.objects.get(username=username)
            if author.password == password:  # You should hash passwords in a real application
                return author
        except Author.DoesNotExist:
            pass

    def get_user(self, user_id):
        try:
            return Author.objects.get(pk=user_id)
        except Author.DoesNotExist:
            return None

