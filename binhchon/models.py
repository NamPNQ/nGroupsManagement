from django.db import models
from django.contrib.auth.models import User
from qlnhom.models import Nhom


class BinhChon(models.Model):
    tieu_de = models.CharField(max_length=200)
    nhom = models.ForeignKey(Nhom)
    nguoi_tao = models.ForeignKey(User)
    ngay_tao = models.DateTimeField()


class NoiDungBinhChon(models.Model):
    binh_chon = models.ForeignKey('BinhChon')
    noi_dung = models.CharField(max_length=200)


class UserVote(models.Model):
    binh_chon = models.ForeignKey('BinhChon')
    noi_dung = models.ForeignKey('NoiDungBinhChon')
    user_id = models.ForeignKey(User)