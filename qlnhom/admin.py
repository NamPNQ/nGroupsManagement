from django.contrib import admin
from qlnhom.models import MonHoc, Nhom, ThanhVienNhom


class NhomInline(admin.StackedInline):
    model = Nhom
    extra = 3


class ThanhvienInline(admin.StackedInline):
    model = ThanhVienNhom
    extra = 3


class MonHocAdmin(admin.ModelAdmin):
    inlines = [NhomInline]


class NhomAdmin(admin.ModelAdmin):
    inlines = [ThanhvienInline]

admin.site.register(MonHoc, MonHocAdmin)
admin.site.register(Nhom,NhomAdmin)