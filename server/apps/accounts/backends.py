from django.contrib.auth import get_user_model


class UsernameAuthentication:
    """
    Authenticate user with username
    """
    User = get_user_model()

    def authenticate(self, request, username, password):
        try:
            user = self.User.objects.get(username__iexact=username)
            if user.check_password(password):
                return user
            else:
                return None
        except (self.User.DoesNotExist, self.User.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        try:
            return self.User.objects.get(id=user_id)
        except self.User.DoesNotExist:
            return None
