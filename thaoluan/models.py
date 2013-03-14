from django.db import models
from django.contrib.auth.models import User
from qlnhom.models import Nhom

# Create your models here.
class ChuDe(models.Model):
    tieu_de = models.CharField(max_length=500)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    nguoi_tao_id = models.ForeignKey(User)
    nhom_id = models.ForeignKey(Nhom)
    noi_dung = models.TextField()

class BinhLuan(models.Model):
    chu_de_id = models.ForeignKey('ChuDe')
    nguoi_gui_id = models.ForeignKey(User)
    ngay_gui = models.DateTimeField()
    noi_dung = models.CharField(max_length=500)
