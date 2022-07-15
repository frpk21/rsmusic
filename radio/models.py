from django.contrib.contenttypes.fields import GenericForeignKey

from django.db import models

from generales.models import ClaseModelo

from django.contrib.auth.models import User

from datetime import date

import os

from datetime import datetime, timedelta

from django.dispatch import receiver

from django.db.models.signals import post_save, post_delete, pre_delete

from ordenacion.models import Contrato, Contra1

from inspector.models import Emisoras, Sedes


class Pautero(ClaseModelo):
    sede = models.ForeignKey(Sedes, on_delete=models.CASCADE, default=1, null=False, blank=False)
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    fecha = models.DateField(blank=False, null=False, auto_now_add=True)
    hora = models.TimeField(blank=False, null=False, auto_now_add=True)
    orden = models.ForeignKey(Contra1, on_delete=models.CASCADE)
    emitido = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.emisora)
   
    def save(self):
        super(Pautero,self).save()

    class Meta:
        verbose_name_plural = "Pauta de Emisoras"

class Generos(ClaseModelo):
    nombre = models.CharField(blank=False, null=False, max_length=100, default="")

    def __str__(self):
        return '{}'.format(self.nombre)
   
    def save(self):
        self.nombre = self.nombre.upper()
        super(Generos,self).save()

    class Meta:
        verbose_name_plural = "Generos"

class Rsmusic(ClaseModelo):
    sede = models.ForeignKey(Sedes, on_delete=models.CASCADE, default=1, null=False, blank=False)
    nombre = models.CharField(blank=False, null=False, max_length=100, default="")
    interprete = models.CharField(blank=False, null=False, max_length=100, default="")
    autor = models.CharField(blank=False, null=False, max_length=100, default="")
    ano = models.IntegerField(default=0, blank=True, null=True)
    likes = models.IntegerField(default=0, blank=True, null=True)
    genero = models.ForeignKey(Generos, on_delete=models.CASCADE)
    tiempo = models.CharField(blank=False, null=False, max_length=8, default="")
    tiempo_ms = models.IntegerField(default=0, blank=True, null=True)
    arc_audio = models.FileField(upload_to="rsmusic/", blank=True, null=True, default='')
    ultimo_prg = models.DateField(blank=True, null=True)

    def __str__(self):
        return '{}-{}'.format(self.nombre, self.interprete)
   
    #def save(self):
    #    self.nombre = self.nombre.upper()
    #    self.interprete = self.interprete.upper()
    #    self.autor = self.autor.upper()
    #    super(Rsmusic,self).save()
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.nombre = self.nombre.upper()
        self.interprete = self.interprete.upper()
        self.autor = self.autor.upper()
        super(Rsmusic,self).save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name_plural = "rsmusicas"

class Listas(ClaseModelo):
    sede = models.ForeignKey(Sedes, on_delete=models.DO_NOTHING, default=1, null=False, blank=False)
    rsmusic = models.ForeignKey(Rsmusic, on_delete=models.DO_NOTHING, default=0, null=False, blank=False)
    nombre = models.CharField(blank=False, null=False, max_length=100, default="")
    fecha = models.DateField(blank=False, null=False, auto_now_add=True)
    hora = models.TimeField(blank=False, null=False, auto_now_add=True)

    def __str__(self):
        return '{}-{}-{}'.format(self.sede.nombre_sede, self.fecha, self.hora)
   
    def save(self):
        self.nombre = self.nombre.upper()
        super(Listas,self).save()

    class Meta:
        verbose_name_plural = "Listas"

class Programas(ClaseModelo):
    sede = models.ForeignKey(Sedes, on_delete=models.CASCADE, null=False, blank=False)
    nombre = models.CharField(blank=False, null=False, max_length=100, default="")
    hora1 = models.TimeField(blank=False, null=False, auto_now_add=True)
    hora2 = models.TimeField(blank=False, null=False, auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.sede.nombre_sede, self.nombre)
   
    def save(self):
        self.nombre = self.nombre.upper()
        super(Programas,self).save()

    class Meta:
        verbose_name_plural = "Programas"

class Programas1(ClaseModelo):
    programa = models.ForeignKey(Programas, on_delete=models.DO_NOTHING, default=1, null=False, blank=False)
    genero = models.ForeignKey(Generos, on_delete=models.CASCADE)

    def __str__(self):
        return '{}-{}'.format(self.programa.nombre, self.genero.nombre)
   
    def save(self):
        super(Programas,self).save()

    class Meta:
        verbose_name_plural = "Programas1"

class Formats(ClaseModelo):
    sede = models.ForeignKey(Sedes, on_delete=models.DO_NOTHING, default=1, null=False, blank=False)
    boton = models.CharField(blank=False, null=False, max_length=10, default="")
    nombre = models.CharField(blank=False, null=False, max_length=100, default="")
    archivo = models.CharField(blank=False, null=False, max_length=200, default="")

    def __str__(self):
        return '{}-{}'.format(self.sede.nombre_sede, self.nombre)
   
    def save(self):
        self.nombre = self.nombre.upper()
        super(Formats,self).save()

    class Meta:
        verbose_name_plural = "Formats"