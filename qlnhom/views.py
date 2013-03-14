from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponse,Http404
from django.utils import simplejson as json


@login_required
def index(request):
    return render_to_response('index.html', context_instance=RequestContext(request))


def json_lookup(request, queryset, field, limit=10, login_required=False, **kwargs):
    """
    Method to lookup a model field and return a array. Intended for use
    in AJAX widgets.
    """
    if login_required and request.user.is_anonymous():
        return redirect_to_login(request.path)
    if request.GET:
        if not 'q' in request.GET:
            raise Http404
        else:
            search = request.GET['q']
            obj_list = []
            lookup = {
                '%s__istartswith' % field: search,
            }
            for obj in queryset.filter(**lookup)[:limit]:
                obj_list.append(dict({"id": obj.pk, field: getattr(obj, field)}.items() + {val: getattr(obj, val)
                                for val in kwargs.get('field_extract') if 'field_extract' in kwargs.iterkeys()}.items()))
            response = json.dumps(obj_list)
            response = request.GET.get('callback', '') + '({"total":%d,"data":'%len(obj_list) + response + '})'
        return HttpResponse(response, mimetype='application/json')
    else:
        raise Http404