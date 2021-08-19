import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError


@pytest.mark.django_db
def test_user_creation():
    from django.contrib.auth import get_user_model

    User = get_user_model()

    with pytest.raises(ValidationError) as err:
        user = User(email="username", username="username")
        user.full_clean()

    assert "email" in err.value.message_dict

    user = User.objects.create_user(username="username", email="user@eMail.com", password="password")

    assert user.email == "user@email.com", "Email has to be normalized"
    assert user.is_active, "User is active."

    assert not user.is_superuser, "User is not superuser."
    assert not user.is_staff, "User is not staff."

    with pytest.raises(IntegrityError) as err:
        User.objects.create_user("username", "password")

    assert err.match("UNIQUE constraint failed: auth_user.username")
