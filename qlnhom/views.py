# encoding: utf-8
from django.core.exceptions import ValidationError
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.utils import simplejson as json
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string


def ajax_required(f):
    """
    AJAX request required decorator
    use it in your views:

    @ajax_required
    def my_view(request):
        ....

    """

    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def check_user_exists_group_in_subject(f):
    def wrap(**kwargs):
        if ('user' in kwargs) and ('mon_hoc_id' in kwargs):
            if not kwargs['user'].nhom_set.all().filter(mon_hoc_id=kwargs['mon_hoc_id']):
                return f(**kwargs)
            else:
                msg = u"<div class='alert alert-error'>" \
                      u"<button type='button' class='close'" \
                      u" data-dismiss='alert'>&times;</button>" \
                      u"<strong>Lỗi: </strong> Môn học này bạn" \
                      u" đã có nhóm rồi. Không thể tạo thêm </div>"
                return {'message': msg}
        else:
            return HttpResponseBadRequest

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


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
               u".html('<i class=\"icon-remove\"></i> Rời khỏi nhóm')" \
               u".attr('data-method','POST')" \
               u".attr('data-target','#deleteModal')" \
               u".removeClass('btn-info ajax').addClass('btn-danger ajax-modal')" \
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
def nhom(request, **kwargs):
    pass


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
        return RequestContext(request, {'form': form,
                                        'method_get':
                                        kwargs['request'].method == 'GET'})

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
            nhom = Nhom.objects.get(pk=kwargs['monhocid'])
            context = resquestForm(user=request.user, mon_hoc_id=nhom.mon_hoc, form=form, request=request)
            #response = render_to_string("_taonhom.html", context)
        else:
            #response = render_to_string("_taonhom.html", RequestContext(request, {'form': form,
            #                                                                      'method_get': request.method == 'GET'
            #}))
            context = RequestContext(request, {'form': form,
                                               'method_get': request.method == 'GET'})

    if request.method == 'POST':
        Form = TaoNhomForm(request.POST)
        if Form.is_valid():
            context = saveForm(user=request.user, mon_hoc_id=Form.cleaned_data['mon_hoc'], form=Form, request=request)
            #response = render_to_string("_taonhom.html", context)
        else:
            context = RequestContext(request, {'form': Form})
            #response = render_to_string("_taonhom.html", )
    data = {
        'html': render_to_string("_taonhom.html", context)
    }
    return HttpResponse(json.dumps(data), mimetype='application/json')


@login_required
@require_POST
@ajax_required
def outgroup(request, **kwargs):
    from qlnhom.models import Nhom, ThanhVienNhom

    nhom = Nhom.objects.get(pk=kwargs['nhomid'])
    if request.user in nhom.dsthanhvien.all():
        membership = ThanhVienNhom.objects.filter(user=request.user, nhom=nhom)
        membership.delete()
        response = u"<div class='alert alert-success'>" \
                   u"<button type='button' class='close' data-dismiss='alert'>&times;</button>" \
                   u"<strong>Thông báo: </strong>Bạn đã rời khỏi nhóm thành công</div>" \
                   u"<script>$('a[href$=\"%s\"]')" \
                   u".html('<i class=\"icon-plus\"></i> Tham gia')" \
                   u".attr('data-method','GET')" \
                   u".removeAttr('data-target')" \
                   u".removeClass('btn-danger ajax-modal').addClass('btn-info ajax')" \
                   u".attr('href','%s')</script>" % (request.get_full_path(), nhom.get_absolute_url() + "/join")

    else:
        response = "<div class='alert alert-error'>" \
                   "<button type='button' class='close' data-dismiss='alert'>&times;</button>" \
                   "<strong>Thông báo: </strong>Bạn chưa tham gia nhóm này !</div>"
    data = {
        "html": response
    }
    return HttpResponse(json.dumps(data), mimetype="application/json")