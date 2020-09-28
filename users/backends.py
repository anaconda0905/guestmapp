from users.models import User


def authenticate(username=None, password=None):
    if '@' in username:
        kwargs = {'email': username}
    else:
        kwargs = {'username': username}
    try:
        user = User.objects.get(**kwargs)
        if user.check_password(password):
            # print(user.username)
            return user
    except User.DoesNotExist:
        return None


class EmailOrUsernameModelBackend(object):
    def authenticate(self, username=None, password=None):
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                # print(user.username)
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
