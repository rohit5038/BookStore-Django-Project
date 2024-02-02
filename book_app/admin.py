from django.contrib import admin
from .models import book, Contact

# Register your models here.



class BookAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'price','bdetails','cat','is_active')
    list_filter=['cat','is_active']
    
admin.site.register(book,BookAdmin)
admin.site.register(Contact)