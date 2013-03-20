# encoding: utf-8
from django.core.exceptions import ValidationError
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.utils import simplejson as json
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from qlnhom.decorator import *


@login_required
def index(request):
    return render_to_response('index.html', context_instance=RequestContext(request))


def _ds_nhom_data(request, nhoms):
    data = {
        "html": render_to_string(
            "_ds_nhom_ajax.html",
            RequestContext(request, {
                "nhoms": nhoms
            })
        )
    }
    return data


@login_required
@require_POST
def listgroup(request):
    if request.is_ajax():
        if not 'id' in request.POST:
            raise Http404
        else:
            from qlnhom.models import Nhom

            mon_hoc_id = request.POST['id']
            g = Nhom.objects.filter(mon_hoc_id=mon_hoc_id)
            response = json.dumps(_ds_nhom_data(request, g))
            return HttpResponse(response, mimetype='application/json')
    else:
        raise Http404


@login_required
@ajax_required
def dsnhomjoined(request, **kwargs):
    data = {
        "html": render_to_string(
            "_dsnhom.html",
            RequestContext(request)
        )
    }
    return HttpResponse(json.dumps(data), mimetype="application/json")


@login_required
@ajax_required
def json_lookup(request, queryset, field, limit=10, **kwargs):
    """
    Method to lookup a model field and return a array. Intended for use
    in AJAX widgets.
    """
    if request.GET:
        if (not 'q' in request.GET) or (not 'callback' in request.GET):
            raise Http404
        else:
            search = request.GET['q']
            obj_list = []
            lookup = {
                '%s__istartswith' % field: search,
            }
            for obj in queryset.filter(**lookup)[:limit]:
                obj_list.append(dict({"id": obj.pk, field: getattr(obj, field)}.items() + {val: getattr(obj, val)
                                                                                           for val in
                                                                                           kwargs.get('field_extract')
                                                                                           if
                                                                                           'field_extract' in kwargs.iterkeys()}.items()))
            response = json.dumps(obj_list)
            response = request.GET.get('callback', '') + '({"total":%d,"data":' % len(obj_list) + response + '})'
        return HttpResponse(response, mimetype='application/json')
    else:
        raise Http404


@login_required
@ajax_required
def jointogroup(request, **kwargs):
    from qlnhom.models import Nhom, ThanhVienNhom

    nhom = Nhom.objects.get(pk=kwargs['nhomid'])
    response = u"<div class='alert'><button type='button' class='close' data-dismiss='alert'>&times;</button>" \
               u"<strong>Thông báo: </strong>Bạn đã tham gia nhóm thành công</div>" \
               u"<script>$('a[href$=\"%s\"]')" \
               u".html('<i class=\"icon-remove\"></i> Bỏ nhóm')" \
               u".attr('data-method','POST')" \
               u".attr('data-target','#deleteModal')" \
               u".removeClass('btn-info ajax').addClass('btn-warning ajax-modal')" \
               u".attr('href','%s')</script>" % (request.get_full_path(), nhom.get_absolute_url() + "/out")

    join = ThanhVienNhom(user=request.user, nhom=nhom)
    try:
        join.full_clean()
        join.save()
    except ValidationError as e:
        response = ""
        for message in e.messages:
            response += u"<div class='alert alert-error'>" \
                        u"<button type='button' class='close' data-dismiss='alert'>&times;</button>" \
                        u"<strong>Lỗi: </strong> %s </div>" % message
    data = {
        "html": response
    }
    return HttpResponse(json.dumps(data), mimetype="application/json")


@login_required
@ajax_required
@user_in_group_required
def nhom(request, **kwargs):
    from qlnhom.models import Nhom
    if request.method == "GET":
        nhom = Nhom.objects.get(pk=kwargs['nhomid'])
        data = {
            'html': render_to_string('_nhom_detail.html', RequestContext(request, {'nhom': nhom}))
        }
        return HttpResponse(json.dumps(data), mimetype='application/json')
    else:
        return HttpResponseBadRequest()


@login_required
def monhoc(request, **kwargs):
    pass


@login_required
@ajax_required
def taonhom(request, **kwargs):
    from django.forms.models import modelform_factory
    from qlnhom.models import Nhom

    TaoNhomForm = modelform_factory(Nhom, exclude=("dsthanhvien",))

    @check_user_exists_group_in_subject
    def resquestForm(**kwargs):
        kwargs['form'].fields["mon_hoc"].initial = kwargs['mon_hoc_id']
        return RequestContext(request, {'form': form})

    @check_user_exists_group_in_subject
    def saveForm(**kwargs):
        g = kwargs['form'].save()
        from qlnhom.models import ThanhVienNhom

        m = ThanhVienNhom(user=kwargs['user'], nhom_id=g.pk, nhom_truong=True)
        msg = u"<div class='alert alert-success'>" \
              u"<button type='button' class='close'" \
              u" data-dismiss='alert'>&times;</button>" \
              u"<strong>Thông báo: </strong>Tạo nhóm" \
              u" thành công</div>"
        m.save()
        msg += u"<div class='alert alert-success'>" \
               u"<button type='button' class='close' data-dismiss='alert'>&times;</button>" \
               u"<strong>Thông báo: </strong> Bạn trở thành nhóm trưởng </div>"
        return {'message': msg}
    if request.method == 'GET':
        form = TaoNhomForm()
        if 'monhocid' in kwargs:
            context = resquestForm(user=request.user, mon_hoc_id=kwargs['monhocid'], form=form)
        else:
            context = RequestContext(request, {'form': form})

    elif request.method == 'POST':
        form = TaoNhomForm(request.POST)
        if form.is_valid():
            context = saveForm(user=request.user, mon_hoc_id=form.cleaned_data['mon_hoc'], form=form)
        else:
            context = RequestContext(request, {'form': form})
    else:
        context = {"message": "<h3>Method not support<h3>"}
    data = {
        'html': render_to_string("_taonhom.html", context)
    }
    return HttpResponse(json.dumps(data), mimetype='application/json')


@login_required
@require_POST
@ajax_required
@user_in_group_required
def outgroup(request, **kwargs):
    from qlnhom.models import ThanhVienNhom
    membership = ThanhVienNhom.objects.filter(user=request.user, nhom=nhom)
    membership.delete()
    response = u"<div class='alert alert-success'>" \
               u"<button type='button' class='close' data-dismiss='alert'>&times;</button>" \
               u"<strong>Thông báo: </strong>Bạn đã rời khỏi nhóm thành công</div>" \
               u"<script>$('a[href$=\"%s\"]')" \
               u".html('<i class=\"icon-plus\"></i> Tham gia')" \
               u".attr('data-method','GET')" \
               u".removeAttr('data-target')" \
               u".removeClass('btn-warning ajax-modal').addClass('btn-info ajax')" \
               u".attr('href','%s')</script>" % (request.get_full_path(), nhom.get_absolute_url() + "/join")
    data = {
        "html": response
    }
    return HttpResponse(json.dumps(data), mimetype="application/json")


@login_required
@require_POST
@ajax_required
@user_in_group_required
def deletegroup(request, **kwargs):
    from qlnhom.models import ThanhVienNhom, Nhom
    m = ThanhVienNhom.objects.filter(user=request.user, nhom_id=kwargs['nhomid'])
    if (m and m.all()[0].nhom_truong) or request.user.is_staff:
        g = Nhom.objects.filter(pk=kwargs['nhomid']).all()
        if g:
            url = g[0].get_absolute_url()
            g[0].delete()
            response = "<div class='alert alert-success'>" \
                       "<button type='button' class='close' data-dismiss='alert'>&times;</button>" \
                       "<strong>Thông báo: </strong>Xóa nhóm thành công!</div>" \
                       "<script>$('a[href$=\"%s\"]').closest('tr')" \
                       ".remove()</script>" % (url + "/delete")
        else:
            response = "<div class='alert alert-error'>" \
                       "<button type='button' class='close' data-dismiss='alert'>&times;</button>" \
                       "<strong>Thông báo: </strong>Bạn đã gửi đi một yêu cầu không hợp lệ !</div>"

    else:
        response = "<div class='alert alert-error'>" \
                   "<button type='button' class='close' data-dismiss='alert'>&times;</button>" \
                   "<strong>Thông báo: </strong>Bạn đã gửi đi một yêu cầu không hợp lệ !</div>"
    data = {
        'html': response
    }
    return HttpResponse(json.dumps(data),mimetype='application/json')