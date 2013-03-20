# Create your views here.
from django.utils import simplejson as json
from django.http import HttpResponse
from django.template.loader import render_to_string
from qlnhom.decorator import *
from django.template import RequestContext

@ajax_required
@user_in_group_required
def thaoluannhom(request, **kwargs):
    from qlnhom.models import Nhom
    nhom = Nhom.objects.get(pk=kwargs['nhomid'])
    data = {
        'html': render_to_string('_nhom_thao_luan.html', RequestContext(request, {'nhom': nhom}))
    }
    return  HttpResponse(json.dumps(data), mimetype='application/json')


@ajax_required
@user_in_group_required
def thaoluanchitiet(request, **kwargs):
    from thaoluan.models import ChuDe
    chude = ChuDe.objects.get(pk=kwargs['thaoluanid'])
    data = {
        'html': render_to_string('_nhom_thao_luan_chitiet.html', RequestContext(request, {'chude': chude}))
    }
    return  HttpResponse(json.dumps(data), mimetype='application/json')