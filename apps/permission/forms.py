from django import forms
from apps.permission.models import Role
from django.utils.text import slugify

class RoleAddForm(forms.ModelForm):
    name = forms.CharField(required=True)
    status = forms.CharField(max_length=8, required=False)
    
    class Meta:
        model = Role
        fields = ['name', 'status']
    def __init__(self, *args, **kwargs):
        super(RoleAddForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['status'].required = True
        