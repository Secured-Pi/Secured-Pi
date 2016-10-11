from django.shortcuts import render
from django.views.generic import TemplateView
from securedpi_events.models import Event
from securedpi_locks.models import Lock
from securedpi.serializers import EventSerializer, LockSerializer
from rest_framework import generics
from rest_framework import permissions
from securedpi.permissions import IsOwnerOrReadOnly
# from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import detail_route
# import requests
# import json
# import uuid


class LockViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides 'list', 'create', 'retrieve',
    'update' and 'destroy' actions.
    Additionally we also provide an extra 'highlight' action.
    """
    queryset = Lock.objects.all()
    serializer_class = LockSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        lock = self.get_object()
        return Response(lock.highlighted)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EventViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides 'list', 'create', 'retrieve',
    'update' and 'destroy' actions.
    Additionally we also provide an extra 'highlight' action.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        event = self.get_object()
        return Response(lock.highlighted)

    def perform_create(self, serializer):
        serializer.save()
