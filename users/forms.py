from allauth.account.forms import SignupForm
from django import forms

class CustomSignupForm(SignupForm):
    ROLE_CHOICES = (
        ('farmer', 'Farmer'),
        ('consumer', 'Consumer'),
    )

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
        label="Role"
    )
    first_name = forms.CharField(required=True, 
                                 max_length=30,
                                 widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'First Name'}),label="First Name")
    last_name = forms.CharField(required=True, 
                                max_length=30,
                                widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Last Name'}),label="Last Name")

    phone = forms.CharField(required=False, max_length=20)
    address = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':2,'id':'id_address','class': 'form-control'}))

    country = forms.CharField(required=False, widget=forms.TextInput(attrs={'id':'id_country','class': 'form-control'}))
    governorate = forms.CharField(required=False, widget=forms.TextInput(attrs={'id':'id_governorate','class': 'form-control'}))
    city_village = forms.CharField(required=False, widget=forms.TextInput(attrs={'id':'id_city_village','class': 'form-control'}))

    latitude = forms.DecimalField(widget=forms.HiddenInput(attrs={'id':'id_latitude'}), required=False)
    longitude = forms.DecimalField(widget=forms.HiddenInput(attrs={'id':'id_longitude'}), required=False)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.role = self.cleaned_data['role']  # make sure your CustomUser model has this field
        user.phone = self.cleaned_data['phone']
        user.address = self.cleaned_data['address']
        user.country = self.cleaned_data['country']
        user.governorate = self.cleaned_data['governorate']
        user.city_village = self.cleaned_data['city_village']
        user.latitude = self.cleaned_data['latitude']
        user.longitude = self.cleaned_data['longitude']
        user.save()
        return user
