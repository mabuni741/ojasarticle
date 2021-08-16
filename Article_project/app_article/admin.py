from django.contrib import admin

# Register your models here.
from .models import ArticleModel, ContactUs

admin.site.register(ArticleModel)

admin.site.register(ContactUs)
