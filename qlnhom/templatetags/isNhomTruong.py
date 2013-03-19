__author__ = 'nampnq'
from django import template

register = template.Library()

@register.filter
def isNhomTruong(value, nhomid):
    from qlnhom.models import ThanhVienNhom
    m = ThanhVienNhom.objects.filter(user_id=value, nhom_id=nhomid)
    if m:
        return m.all()[0].nhom_truong
    else:
        return False