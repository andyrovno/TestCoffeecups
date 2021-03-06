# -*- coding: utf-8 -*-
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from django.utils import simplejson
from django.http import HttpResponse

from testingproject.testapp.models import MyInfo, ReqsHistory
from forms import MyInfoForm


def main_page_info(request):
    myinfo = MyInfo.objects.filter()
    resp_dict = {'myinfo': myinfo, 'user': request.user}
    return direct_to_template(request, 'main_page.html',
                resp_dict)


def requests_log(request):
    try:
        prior = request.GET['pr'].encode('utf-8')
    except:
        prior = None
    if prior:
        first_ten_requests = \
                ReqsHistory.objects.filter(req_priority=\
                        int(prior)).order_by('timestamp')[: 10]
    else:
        first_ten_requests =\
                ReqsHistory.objects.filter().order_by('timestamp')[: 10]
    return direct_to_template(request, "reqs_log.html",
                {'requests': first_ten_requests}
            )


@login_required
def edit_my_info(request):
    try:
        my_info = MyInfo.objects.get(pk=1)
    except:
        my_info = None
    if request.method == 'POST':
        form = MyInfoForm(request.POST, request.FILES, instance=my_info,
                    auto_id=False)
        response_dict = {}
        if request.is_ajax():
            if form.is_valid():
                form.save()
                response_dict['message'] = 'Changes have been saved'
                response_dict['result'] = 'success'
            else:
                response_dict['result'] = 'error'
                response = {}
                for error in form.errors:
                    response[error] = form.errors[error][0]
                response_dict['response'] = response
            json = simplejson.dumps(response_dict, ensure_ascii=False)
            return HttpResponse(json, mimetype='application/json')
        else:
            if form.is_valid():
                form.save()
    else:
        form = MyInfoForm(instance=my_info)
        myphoto = my_info.my_photo
    return direct_to_template(request, 'edit_my_info.html',
                {'form': form, 'myphoto': myphoto})


def remove_log_object(request):
    results = {}
    if request.method == "POST" and request.is_ajax():
        if 'request_id' in request.POST and request.POST['request_id']:
            try:
                ReqsHistory.objects.get(pk=request.POST['request_id'].encode('utf-8')).delete()
                results['success'] = True
            except:
                results['success'] = False
            json = simplejson.dumps(results, ensure_ascii=False)
    return HttpResponse(json, mimetype='application/json')
