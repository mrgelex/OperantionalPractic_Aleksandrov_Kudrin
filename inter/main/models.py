from django.db import models

class Devices(models.Model):
    id_device=models.IntegerField(max_length=3, primary_key=True)
    serial=models.IntegerField(max_length=10)
    IMEI=models.IntegerField(max_length=16)
    name=models.CharField(max_length=20)
    type=models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'DEVICES'

    def __str__(self):
        return self.name

class Evet(models.Model):
    id_log=models.IntegerField(primary_key=True)
    id_device=models.IntegerField()
    date_local=models.DateField()
    time_local=models.TimeField()
    status=models.IntegerField(max_length=5)
    depth=models.IntegerField(max_length=3)
    power=models.IntegerField(max_length=3)

    class Meta:
        managed = False
        db_table = 'LOG_EVENT'

class Time(models.Model):
    id_log=models.IntegerField(primary_key=True)
    id_device=models.IntegerField()
    date_local=models.DateField()
    time_local=models.TimeField()
    status=models.IntegerField(max_length=5)
    depth=models.IntegerField(max_length=3)
    power=models.IntegerField(max_length=3)

    class Meta:
        managed = False
        db_table = 'LOG_TIME'