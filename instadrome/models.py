from django.db import models

# Create your models here.
class InstagrabGellifiqueGelColour(models.Model):
    taken_at = models.DateTimeField()
    username = models.CharField(max_length=100)
    code = models.CharField(unique=True, max_length=100)
    caption = models.TextField()
    like_count = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    media_type = models.IntegerField()
    products = models.CharField(max_length=255)
    created_dt = models.DateTimeField()
    updated_dt = models.DateTimeField(blank=True, null=True)
    code2 = models.CharField(max_length=100, blank=True, null=True)
    reposted_dt = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'instagrab_gellifique_gel_colour'
