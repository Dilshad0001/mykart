# Generated by Django 5.1.4 on 2025-04-20 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0017_user_user_email_alter_orderdetails_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='order_number',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]
