from django.shortcuts import render
from django.views.generic import TemplateView
from securedpi_locks.models import Lock
from securedpi_locks.serializers import LockSerializer
from rest_framework import generics
# from django.contrib.auth.models import User
from rest_framework import permissions
from securedpi_locks.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import detail_route
import requests
import json


class DashboardView(TemplateView):
    """Establish class for Dashboard page view."""
    template_name = 'securedpi_locks/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        current_user = self.request.user
        locks_by_created_date = current_user.locks.order_by('-date_created')
        context['locks'] = locks_by_created_date
        return context


class LockViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides 'list', 'create', 'retrieve',
    'update' and 'destroy' actions.
    Additionally we also provide an extra 'highlight' action.
    """
    queryset = Lock.objects.all()
    serializer_class = LockSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        lock = self.get_object()
        return Response(lock.highlighted)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


def manual_unlock(request):
    if request.method == 'GET':
        data = json.dumps({'action': 'unlock'})
        headers = {'content-type': 'application/json'}
        response = requests.post('http://52.43.75.183:5000', data=data, headers=headers)
    return render(request, 'securedpi_locks/lock_details.html')


def manual_lock(request):
    if request.method == 'GET':
        data = json.dumps({'action': 'lock'})
        headers = {'content-type': 'application/json'}
        response = requests.post('http://52.43.75.183:5000', data=data, headers=headers)
    return render(request, 'securedpi_locks/lock_details.html')


def update_status(request):
    if request.method == 'GET':
        auth = ('user3', 'user3password')
        data = json.dumps({
            'status': 'unlocked',
            'title': 'lock 1',
            'description': 'snack room',
            'location': 'Code Fellows',
            'raspberry_pi_id': 'sgfh48756%$'})
        headers = {'content-type': 'application/json'}
        response = requests.put('http://localhost:8000/api/locks/4/', auth=auth, data=data, headers=headers)
        #import pdb; pdb.set_trace()
    return render(request, 'securedpi_locks/dashboard.html')
