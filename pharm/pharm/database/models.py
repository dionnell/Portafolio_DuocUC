# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models
from django.contrib.auth.models import AbstractUser


digito_v = [('0','0'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('k','k')]
genero = [('M','Masculino'),('F','Femenino')]
inscripcion_fam = [('si','Si'),('no','No')]

class User (AbstractUser):
    is_medical = models.BooleanField(default=False)
    is_pharma = models.BooleanField(default=False)
    
    

class DetallePrescripcion(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    id_pres = models.ForeignKey('Prescripcion', models.DO_NOTHING, db_column='id_pres')
    id_med = models.ForeignKey('Medicamento', models.DO_NOTHING, db_column='id_med')
    descripcion = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    

    class Meta:
        managed = False
        db_table = 'detalle_prescripcion'
        
    def __str__ (self):
        return '{}'.format(self.id_detalle)
    


class EntregaMedicamento(models.Model):
    id_entrega = models.AutoField(primary_key=True)
    id_pres = models.ForeignKey('Prescripcion', models.DO_NOTHING, db_column='id_pres')
    rut_func = models.ForeignKey('Funcionario', models.DO_NOTHING, db_column='rut_func')
    retiro = models.CharField(max_length=100)
    fecha_ent = models.DateTimeField(db_column='fecha_ent')

    class Meta:
        managed = False
        db_table = 'entrega_medicamento'

    def __str__ (self):
        return '{}'.format(self.id_entrega)


class Funcionario(models.Model):
    rut_func = models.IntegerField(primary_key=True)
    dv = models.CharField(max_length=1)
    pri_nombre = models.CharField(max_length=50)
    seg_nombre = models.CharField(max_length=50)
    ape_paterno = models.CharField(max_length=50)
    ape_materno = models.CharField(max_length=50)
    user_func =  models.CharField(max_length=50)
    contra = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'funcionario'
    def __str__ (self):
        return '{}'.format(self.rut_func)


class Medicamento(models.Model):
    id_med = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    detalle = models.CharField(max_length=100)
    gramaje = models.CharField(max_length=10)
    stock = models.BigIntegerField()
    fabricante = models.CharField(max_length=100)
    componentes = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'medicamento'

    def __str__ (self):
        return '{}'.format(self.nombre)


class Medico(models.Model):
    rut_medico = models.IntegerField(primary_key=True)
    dv = models.CharField(max_length=1)
    pri_nombre = models.CharField(max_length=50)
    seg_nombre = models.CharField(max_length=50)
    ape_paterno = models.CharField(max_length=50)
    ape_materno = models.CharField(max_length=50)
    especialidad = models.CharField(max_length=50)
    user_medic = models.CharField(max_length=50)
    contra = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'medico'
    def __str__ (self):
        return '{}'.format(self.rut_medico)


class Paciente(models.Model):
    rut_pac = models.IntegerField(primary_key=True, help_text="ingresar rut sin puntos")
    dv = models.CharField(max_length=1, choices=digito_v)
    pri_nombre = models.CharField(max_length=50)
    seg_nombre = models.CharField(max_length=50)
    ape_paterno = models.CharField(max_length=50)
    ape_materno = models.CharField(max_length=50)
    edad = models.IntegerField()
    sexo = models.CharField(max_length=1, choices=genero)
    telefono = models.IntegerField()
    email = models.CharField(max_length=100)
    inscripcion_fam = models.CharField(max_length=50, choices=inscripcion_fam)

    class Meta:
        managed = False
        db_table = 'paciente'
    def __str__ (self):
        return '{}'.format(self.rut_pac)
    


class Prescripcion(models.Model):
    id_pres = models.AutoField(primary_key=True)
    rut_medico = models.ForeignKey(Medico, models.DO_NOTHING, db_column='rut_medico')
    rut_pac = models.ForeignKey(Paciente, models.DO_NOTHING, db_column='rut_pac')
    fecha_pres = models.DateTimeField(db_column='fecha_pres')

    class Meta:
        managed = False
        db_table = 'prescripcion'
    def __str__ (self):
        return '{}'.format(self.id_pres)


class ReservaMedicamento(models.Model):
    id_reserva = models.AutoField(primary_key=True)
    id_entrega = models.ForeignKey(EntregaMedicamento, models.DO_NOTHING, db_column='id_entrega')
    detalle = models.CharField(max_length=100)
    fecha_res = models.DateTimeField(db_column='fecha_res')

    class Meta:
        managed = False
        db_table = 'reserva_medicamento'


class Merma(models.Model):
    merma_id = models.AutoField(primary_key=True)
    id_med = models.ForeignKey('Medicamento', models.DO_NOTHING, db_column='id_med')
    fecha = models.DateTimeField(db_column='fecha')
    cantidad = models.IntegerField()
    detalle = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'merma'


class DetalleEntrega(models.Model):
    id_det_ent = models.IntegerField(primary_key=True)
    id_entrega = models.ForeignKey('EntregaMedicamento', models.DO_NOTHING, db_column='id_entrega')
    retiro = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'detalle_entrega'