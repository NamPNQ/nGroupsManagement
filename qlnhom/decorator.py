__author__ = 'nampnq'
# encoding: utf8


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
            from django.http import HttpResponseBadRequest
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
            from django.http import HttpResponseBadRequest
            return HttpResponseBadRequest()

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def user_in_group_required(f):
    def wrap(request, *args, **kwargs):
        if request and ('nhomid' in kwargs):
            from qlnhom.models import Nhom
            n = Nhom.objects.filter(pk=kwargs['nhomid']).all()
            if n and (request.user in n[0].dsthanhvien.all()):
                return f(request, *args, **kwargs)
            else:
                data = {
                    'html': "<div class='alert alert-error'>"
                            "<button type='button' class='close' data-dismiss='alert'>&times;</button>"
                            "<strong>Thông báo: </strong>Bạn chưa tham gia nhóm này !</div>"
                }
                return HttpResponse(json.dumps(data), mimetype='application/json')
        else:
            from django.http import HttpResponseBadRequest
            return  HttpResponseBadRequest()

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap