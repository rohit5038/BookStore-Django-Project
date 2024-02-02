from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class book(models.Model):
    CAT = ((1,'Action'),(2,'Anime'),(3,'Science-Fiction'))
    name=models.CharField(max_length=50, verbose_name = "Book Name")
    price=models.FloatField()
    bdetails=models.CharField(max_length=1000, verbose_name = "Book Details")
    cat=models.IntegerField(verbose_name = "Category", choices = CAT)
    is_active=models.BooleanField(default=True, verbose_name = "Available")
    pimage=models.ImageField(upload_to='image')
    
class cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(book,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)
    
class order(models.Model):
    orderid = models.CharField(max_length = 50)
    uid = models.ForeignKey(User, on_delete = models.CASCADE, db_column = "uid")
    pid = models.ForeignKey(book, on_delete = models.CASCADE, db_column = "pid")
    qty = models.IntegerField(default = 1)
    
class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=50, verbose_name = "Customer Name")
    email=models.CharField(max_length=70, verbose_name = "Customer Email", default="")
    phone=models.CharField(max_length=70, verbose_name = "Customer No.", default="")
    desc=models.CharField(max_length=700, verbose_name = "Customer Query", default="")