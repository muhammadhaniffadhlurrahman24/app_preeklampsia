"""Create initial admin user.

This data migration creates a superuser with the credentials requested by
the user if it does not already exist.
"""
from django.db import migrations


def create_admin_user(apps, schema_editor):
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        username = 'admin@gmail.com'
        password = 'admin123321'
        email = 'admin@gmail.com'

        if not User.objects.filter(username=username).exists():
            # create_superuser will set is_staff/is_superuser appropriately
            User.objects.create_superuser(username=username, email=email, password=password, first_name='Admin')
    except Exception:
        # Don't let a failure here break migrations; surface in logs when run.
        import sys
        print('Failed to create admin user', file=sys.stderr)


def remove_admin_user(apps, schema_editor):
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        username = 'admin@gmail.com'
        User.objects.filter(username=username).delete()
    except Exception:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('screening', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_admin_user, remove_admin_user),
    ]
