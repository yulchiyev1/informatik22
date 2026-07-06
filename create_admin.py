import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'informatik22.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Profile

username = os.environ.get('ADMIN_USERNAME', 'admin')
email = os.environ.get('ADMIN_EMAIL', 'admin@informatik22.uz')
password = os.environ.get('ADMIN_PASSWORD', 'admin1234')

if not User.objects.filter(username=username).exists():
    print(f"Creating superuser {username}...")
    user = User.objects.create_superuser(username=username, email=email, password=password)
    # Ensure profile is approved
    profile, _ = Profile.objects.get_or_create(user=user)
    profile.is_approved = True
    profile.full_name = "Bosh O'qituvchi"
    profile.save()
    print("Superuser created successfully.")
else:
    print(f"Superuser {username} already exists.")
