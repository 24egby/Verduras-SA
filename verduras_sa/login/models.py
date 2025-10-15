from django.db import models
from django.contrib.auth.models import User
import gerente.models as MG 

class Rol(models.Model):
    id = models.AutoField(primary_key=True)
    rol = models.CharField(max_length=50)
    class Meta:
        db_table = 'roles'     
        managed = False      
    def __str__(self):
        return self.rol

class UsuarioRol(models.Model):
    id = models.AutoField(primary_key=True)
    idUserAuth = models.ForeignKey(User, on_delete=models.CASCADE, db_column='idUserAuth')
    idRol = models.ForeignKey(Rol, on_delete=models.CASCADE, db_column='idRol')
    idInsta = models.ForeignKey(MG.Instalacion, on_delete=models.CASCADE, db_column='idInsta', null=True)
    class Meta:
        db_table = 'users'
        managed = False