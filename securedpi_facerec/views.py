from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from django.urls import reverse
from .models import Photo


@method_decorator(login_required, name='dispatch')
class PhotoView(TemplateView):
    template_name = 'securedpi_facerec/photos.html'
    model = Photo
    context_object_name = 'photos'

    def get_context_data(self, **kwargs):
        context = super(PhotoView, self).get_context_data(**kwargs)
        context['MEDIA_ROOT'] = settings.MEDIA_ROOT
        return context

    def get_queryset(self):
        return Photo.objects.filter(user=self.request.user)


# @method_decorator(login_required, name='dispatch')
# class AlbumView(ListView):
#     template_name = 'imager_images/albums.html'
#     model = Album
#     context_object_name = 'albums'
#
#     def get_queryset(self):
#         return Album.objects.filter(user=self.request.user)
#
#     def get_context_data(self, **kwargs):
#         context = super(AlbumView, self).get_context_data(**kwargs)
#         context['MEDIA_ROOT'] = settings.MEDIA_ROOT
#         return context
#
#
# @method_decorator(login_required, name='dispatch')
# class AlbumDetailView(DetailView):
#     template_name = 'imager_images/album-detail.html'
#     model = Album
#     context_object_name = 'album'
#
#     def get_queryset(self):
#         return Album.objects.filter(user=self.request.user, id=self.kwargs['pk'])
#
#
# @method_decorator(login_required, name='dispatch')
# class PhotoDetailView(DetailView):
#     template_name = 'imager_images/photo_detail.html'
#     model = Photo
#     context_object_name = 'photo'
#
#     def get_queryset(self):
#         return Photo.objects.filter(user=self.request.user, id=self.kwargs['pk'])
#
#
# @method_decorator(login_required, name='dispatch')
# class UploadPhotoView(CreateView):
#     template_name = 'imager_images/upload_photo.html'
#     model = Photo
#     fields = ['title', 'description', 'published', 'image']
#
#     def get_success_url(self):
#         self.object.user = self.request.user
#         self.object.save()
#         return reverse('photo_detail', args=(self.object.pk,))
#
#
# @method_decorator(login_required, name='dispatch')
# class AddAlbumView(CreateView):
#     template_name = 'imager_images/add_album.html'
#     model = Album
#     fields = ['title', 'description', 'published', 'cover', 'photos']
#
#     def get_context_data(self, **kwargs):
#         context = super(AddAlbumView, self).get_context_data(**kwargs)
#         context['form'].fields['photos'].queryset = Photo.objects.filter(user=self.request.user)
#         context['form'].fields['cover'].queryset = Photo.objects.filter(user=self.request.user)
#         return context
#
#     def get_success_url(self):
#         self.object.user = self.request.user
#         self.object.save()
#         return reverse('album_detail', args=(self.object.pk,))
#
#
# @method_decorator(login_required, name='dispatch')
# class EditPhotoView(UpdateView):
#     template_name = 'imager_images/edit_photo.html'
#     model = Photo
#     fields = ['title', 'description', 'published']
#
#     def get_success_url(self):
#         return reverse('photo_detail', args=(self.object.pk,))
#
#
# @method_decorator(login_required, name='dispatch')
# class EditAlbumView(UpdateView):
#     template_name = 'imager_images/edit_album.html'
#     model = Album
#     fields = ['title', 'description', 'published', 'cover', 'photos']
#
#     def get_success_url(self):
#         return reverse('album_detail', args=(self.object.pk))
