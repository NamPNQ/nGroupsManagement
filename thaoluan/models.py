from django.db import models
from django.contrib.auth.models import User
from qlnhom.models import Nhom


class ChuDe(models.Model):
    tieu_de = models.CharField(max_length=500)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    nguoi_tao = models.ForeignKey(User)
    nhom = models.ForeignKey(Nhom)
    noi_dung = models.TextField()


class BinhLuan(models.Model):
    chu_de = models.ForeignKey('ChuDe')
    nguoi_gui = models.ForeignKey(User)
    ngay_gui = models.DateTimeField()
    noi_dung = models.CharField(max_length=500)
