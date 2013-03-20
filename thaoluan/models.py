# encoding: utf8
from django.db import models
from django.contrib.auth.models import User
from qlnhom.models import Nhom


class ChuDe(models.Model):
    tieu_de = models.CharField('Tiêu đề', max_length=500)
    ngay_tao = models.DateTimeField('Ngày tạo', auto_now_add=True)
    nguoi_tao = models.ForeignKey(User, verbose_name='Người tạo')
    nhom = models.ForeignKey(Nhom, verbose_name='Nhóm')
    noi_dung = models.TextField('Nội dung')

    class Meta:
        verbose_name_plural = "Danh sách chủ đề"
        verbose_name = "Chủ đề"
        ordering = ['-ngay_tao']

    def __unicode__(self):
        return u"Thảo luận #%d - Nhóm %s" % (self.pk, self.nhom)


class BinhLuan(models.Model):
    chu_de = models.ForeignKey('ChuDe', verbose_name='Chủ đề')
    nguoi_gui = models.ForeignKey(User, verbose_name='Người gửi')
    ngay_gui = models.DateTimeField('Ngày gửi', auto_now_add=True)
    noi_dung = models.CharField('Nội dung', max_length=500)

    class Meta:
        verbose_name_plural = "Danh sách bình luận"
        verbose_name = "Bình luận"
        ordering = ['ngay_gui']

    def __unicode__(self):
        return u"Bình luận #%d - Chủ đề #%d" % (self.pk, self.chu_de_id)