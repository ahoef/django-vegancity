from vegancity.models import User


def get_user(*args, **kwargs):
    if 'username' not in kwargs:
        kwargs.update({'username': 'Moby'})
    user, _ = User.objects.get_or_create(*args, **kwargs)
    return user
