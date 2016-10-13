from django.shortcuts import render
from django.views.generic import UpdateView
from securedpi_profile.models import SecuredpiProfile
from django.urls import reverse


class EditProfileView(UpdateView):
    """Define edit profile class."""
    model = SecuredpiProfile
    fields = [
        'first_name',
        'last_name',
        'address',
        'phone_number'
    ]

    # def __init__(self, *args, **kwargs):
    #     super(EditProfileView, self).__init__(*args, **kwargs)
    #     import pdb; pdb.set_trace()
    #     self.fields['first_name'].widget.attrs['class'] = 'form-control'

    def get_success_url(self):
        """Set redirection after updating the profile."""
        url = reverse('profile')
        return url
