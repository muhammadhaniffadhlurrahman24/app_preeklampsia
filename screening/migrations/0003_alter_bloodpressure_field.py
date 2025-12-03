from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('screening', '0002_create_admin_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='screeningsubmission',
            name='blood_pressure_td1',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
    ]
