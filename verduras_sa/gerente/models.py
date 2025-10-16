from django.db import models

class Instalacion(models.Model):
    id = models.AutoField(primary_key=True)
    instalacion = models.CharField(max_length=100)
    dirrecion = models.CharField(max_length=200)
    tipoInsta = models.IntegerField()
    idAdmin = models.IntegerField(null=True, blank=True)
    idCoord = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'instalaciones'
        managed = False


class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    producto = models.CharField(max_length=100)
    class Meta:
        db_table = 'productos'
        managed = False
    def __str__(self):
        return self.producto
