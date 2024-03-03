from django.contrib import admin
from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message')  # Customize to display these fields in the admin list view

admin.site.register(Contact, ContactAdmin)