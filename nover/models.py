from django.db import models

# Create your models here.

class BookName(models.Model):
    bookname = models.CharField(max_length = 20)
    bookauthor = models.CharField(max_length = 20,null = True,blank = True)
    def __str__(self):
        return self.bookname
    
class BookSpider(models.Model):
    bookname = models.ForeignKey(BookName,on_delete = models.CASCADE,null = True)
    spider_id = models.IntegerField(default=0)
    bookspider = models.CharField(max_length = 10000)
    def __str__(self):
        return self.bookspider

class Content(models.Model):
    bookspider = models.ForeignKey(BookSpider,on_delete = models.CASCADE,null = True)
    content = models.CharField(max_length = 50000,null = True)
    def __str__(self):
        return self.content

class Poll(models.Model):
    name = models.CharField(max_length=20, unique=True)
    poll_num = models.IntegerField(default=0)
    def __str__(self):
        return self.poll_num
