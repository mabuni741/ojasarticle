# Generated by Django 3.2 on 2021-04-28 09:30

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app_article', '0004_alter_token_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=100)),
                ('message', models.TextField(blank=True, max_length=1000, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='token',
            name='token',
            field=models.UUIDField(default=uuid.UUID('9185504a-8b58-4e29-ba2a-8663cd64e49b'), editable=False),
        ),
    ]