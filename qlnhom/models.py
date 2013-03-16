# encoding: utf-8

from django.db import models
from django.contrib.auth.models import User
import datetime

YEAR_CHOICES = []
for i in range(2000, datetime.datetime.now().year + 1):
    YEAR_CHOICES.append((i, i))

Loai_Nhom_Choice = (
    (0, 'Public'),
    (1, 'Private'),
)


class MonHoc(models.Model):
    ten_mon = models.CharField('Tên môn học', max_length=50)
    gioi_thieu = models.CharField('Giới thiệu về nhóm', max_length=500)
    nam_hoc = models.IntegerField('Năm học', max_length=4, choices=YEAR_CHOICES, default=datetime.datetime.now().year)

    def __unicode__(self):
        return self.ten_mon

    class Meta:
        verbose_name = "Môn học"
        verbose_name_plural = "Danh sách môn học"


class Nhom(models.Model):
    ten_nhom = models.CharField('Tên nhóm', max_length=50)
    mon_hoc = models.ForeignKey('MonHoc', verbose_name='Tên Môn Học')
    max_sl = models.SmallIntegerField("Số lương")
    gioi_thieu_nhom = models.CharField('Giới thiệu về nhóm', max_length=500)
    loai_nhom = models.SmallIntegerField('Loại nhóm', choices=Loai_Nhom_Choice, default=0)
    dsthanhvien = models.ManyToManyField(User, through='ThanhVienNhom', verbose_name='Danh sách thành viên')

    def is_full_member(self):
        return self.dsthanhvien.count() >= self.max_sl

    def __unicode__(self):
        return self.ten_nhom

    class Meta:
        verbose_name = "Nhóm"
        verbose_name_plural = "Danh sách nhóm"


class ThanhVienNhom(models.Model):
    user = models.ForeignKey(User, verbose_name='Tên thành viên')
    nhom = models.ForeignKey('Nhom', verbose_name='Nhóm tham gia')
    ngay_tham_gia = models.DateField(auto_now_add=True)
    acitve = models.BooleanField('Kích hoạt', default=False)
    nhom_truong = models.BooleanField('Nhóm trưởng', default=False)

    class Meta:
        verbose_name = "Thành viên"
        verbose_name_plural = "Danh sách thành viên"
        unique_together = ('user', 'nhom')

    def __unicode__(self):
        return self.user.username

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.user.nhom_set.all().filter(mon_hoc_id=self.nhom.mon_hoc):
            raise ValidationError(u"Môn học %s bạn %s đã có nhóm" % (self.nhom.mon_hoc, self.user))