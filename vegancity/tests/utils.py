from vegancity.models import User


def get_user():
    user, _ = User.objects.get_or_create(username="Moby")
    return user
