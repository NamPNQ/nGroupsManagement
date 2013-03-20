__author__ = 'nampnq'
from django.contrib import admin
from thaoluan.models import ChuDe, BinhLuan


class BinhLuanInline(admin.StackedInline):
    model = BinhLuan
    extra = 3


class ChuDeAdmin(admin.ModelAdmin):
    inlines = [BinhLuanInline]

admin.site.register(ChuDe, ChuDeAdmin)