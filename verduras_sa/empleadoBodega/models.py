from django.db import models

class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    producto = models.CharField(max_length=100)
    class Meta:
        db_table = 'productos'
        managed = False
    def __str__(self):
        return self.producto

