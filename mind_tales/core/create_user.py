import os
from django.contrib.auth import get_user_model


User = get_user_model()

ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin@mail.com')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'asddsa')

if not User.objects.filter(email=ADMIN_USERNAME).exists():
    user = User.objects.create_user(username=ADMIN_USERNAME, password=ADMIN_PASSWORD)
    user.is_superuser = True
    user.is_staff = True
    user.save()

    print('ADMIN USER CREATED!')
