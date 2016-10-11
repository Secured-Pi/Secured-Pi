from django.shortcuts import render
from django.views.generic import TemplateView
import requests
import json
import uuid


class DashboardView(TemplateView):
    """Establish class for Dashboard page view."""
    template_name = 'securedpi_locks/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        current_user = self.request.user
        locks_by_created_date = current_user.locks.order_by('-date_created')
        context['locks'] = locks_by_created_date
        return context


def manual_unlock(request):
    if request.method == 'GET':
        serial = '00000000cfef42b5'
        token = str(uuid.uuid4())
        data = json.dumps(
            {'action': 'unlock',
             'serial': serial,
             'token': token,
             'type': 'manual'
             }
            )
        headers = {'content-type': 'application/json'}
        response = requests.post('http://52.43.75.183:5000', data=data, headers=headers)
    return render(request, 'securedpi_locks/dashboard.html')


def manual_lock(request):
    if request.method == 'GET':
        serial = '00000000cfef42b5'
        token = str(uuid.uuid4())
        data = json.dumps(
            {'action': 'lock',
             'serial': serial,
             'token': 'token',
             'type': 'manual'
             }
            )
        headers = {'content-type': 'application/json'}
        response = requests.post('http://52.43.75.183:5000', data=data, headers=headers)
    return render(request, 'securedpi_locks/dashboard.html')


def update_status(request):
    if request.method == 'GET':
        auth = ('user3', 'user3password')
        data = json.dumps({
            'status': 'unlocked',
            'title': 'lock 1',
            'description': 'snack room',
            'location': 'Code Fellows',
            'serial': 'sgfh48756%$'})
        headers = {'content-type': 'application/json'}
        response = requests.put('http://localhost:8000/api/locks/4/', auth=auth, data=data, headers=headers)
        #import pdb; pdb.set_trace()
    return render(request, 'securedpi_locks/dashboard.html')
