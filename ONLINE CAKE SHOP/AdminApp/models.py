from django.db import models

# Create your models here.
class Category(models.Model):
    cat_name = models.CharField(max_length = 20)

    class Meta:
        db_table = "Category"

    def __str__(self):
        return self.cat_name

class Cake(models.Model):
    cname = models.CharField(max_length = 20)
    price = models.FloatField(default = 200)
    description = models.CharField(max_length=200)
    image_url = models.ImageField(default = "abc.jpg",
                         upload_to = "Images")
    category = models.ForeignKey(Category,on_delete = models.CASCADE)

    class Meta:
        db_table = "Cake"
