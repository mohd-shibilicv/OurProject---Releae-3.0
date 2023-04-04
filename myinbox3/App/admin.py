from django.contrib import admin
from App.models import Customer

class CustomerAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'name', 'phone', 'email', 'subject', 'message', 'file')
    list_display = ['name', 'email', 'subject', 'created_at', 'situation']
    search_fields = ['name', 'email', 'subject']
    list_filter = ['status']
    list_per_page = 10

admin.site.register(Customer, CustomerAdmin)