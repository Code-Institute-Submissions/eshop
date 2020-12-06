from django.db import models

# Create your models here.

# to have a listing table in database


class Listing(models.Model):
    # fields / attributes of this table
    title = models.CharField(blank=False, max_length=255)
    SKU = models.CharField(blank=False, max_length=255)
    description = models.TextField(blank=False)

    # toString function -- allow us to state the string rep of class
    def __str__(self):
        return self.title
