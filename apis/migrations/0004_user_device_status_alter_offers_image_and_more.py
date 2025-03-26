# Generated by Django 5.1.7 on 2025-03-21 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0003_borrow_expense_inventory_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='device_status',
            field=models.CharField(choices=[('1', 'ANDROID'), ('2', 'WEB'), ('3', 'IOS')], default='', max_length=45),
        ),
        migrations.AlterField(
            model_name='offers',
            name='image',
            field=models.ImageField(blank=True, upload_to='offer'),
        ),
        migrations.AlterField(
            model_name='user',
            name='fcm_token',
            field=models.TextField(blank=True, default='', max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='sign_in_token',
            field=models.CharField(blank=True, default='', max_length=40, null=True),
        ),
    ]
