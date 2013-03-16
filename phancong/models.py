# encoding: utf-8

from django.db import models
from django.contrib.auth.models import User
from qlnhom.models import Nhom


class PhanCong(models.Model):
    nhom = models.ForeignKey(Nhom, verbose_name='Tên nhóm')
    nguoi_tao = models.ForeignKey(User)


class NoiDungCongViec(models.Model):
    phan_cong = models.ForeignKey('PhanCong')
    ten_cong_viec = models.CharField(max_length=50)
    han_chot = models.DateTimeField()
    mo_ta = models.TextField()
    ghi_chu = models.CharField(max_length=500)


class PhanCongViec(models.Model):
    user = models.ForeignKey(User)
    cong_viec = models.ForeignKey('NoiDungCongViec')
