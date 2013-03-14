from django.db import models
from django.contrib.auth.models import User
from qlnhom.models import Nhom

# Create your models here.
class BinhChon(models.Model):
    tieu_de = models.CharField(max_length=200)
    nhom_id = models.ForeignKey(Nhom)
    nguoi_tao = models.ForeignKey(User)
    ngay_tao = models.DateTimeField()

class NoiDungBinhChon(models.Model):
    binh_chon_id = models.ForeignKey('BinhChon')
    noi_dung = models.CharField(max_length=200)

class UserVote(models.Model):
    binh_chon_id = models.ForeignKey('BinhChon')
    noi_dung_id = models.ForeignKey('NoiDungBinhChon')
    user_id = models.ForeignKey(User)