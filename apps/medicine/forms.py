from django import forms 
from apps.medicine.models import Medicine, Category, Unit, Type, Leaf
from system.middleware.thread_local import _thread_local
from apps.supplier.models import Supplier

class MedicinAddForm(forms.ModelForm):
    name = forms.CharField(required=True)
    generic_name = forms.CharField(required=False)
    strength = forms.CharField(required=True)
    shelf = forms.CharField(required=True)
    details = forms.CharField(required=False)
    # batch = forms.CharField(required=True)
    # expire_date = forms.DateField(required=False)  
    # price =  forms.DecimalField(required=False)
    # supplier_price = forms.DecimalField(required=True)
    status = forms.CharField(required=False)
    
    supplier_name = forms.ModelChoiceField(queryset=Supplier.objects.all(), required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    # unit = forms.ModelChoiceField(queryset=Unit.objects.all(), required=False)
    # type = forms.ModelChoiceField(queryset=Type.objects.all(), required=False)
    # leaf = forms.ModelChoiceField(queryset=Leaf.objects.all(), required=False)
    class Meta:
        model = Medicine
        fields = ['name', 'generic_name', 'status', 'strength', 'shelf', 'details', 'supplier_name', 'category']  

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None) 
        super(MedicinAddForm, self).__init__(*args, **kwargs)
        if not self.instance.pk: 
            self.fields['status'].initial = '1'

    def clean(self):
        cleaned_data = super().clean()
        user_instance = getattr(_thread_local, 'user', None)
        if user_instance:
            self.instance.admin_id = user_instance 
        else:
            self.instance.admin_id = None 

        # print('user instance : ', user_instance)
        # print('clean data : ', self.instance.admin_id)
        return cleaned_data

class CategoryForm(forms.ModelForm):
    name = forms.CharField(required=True)
    status = forms.CharField(required=False) 

    class Meta:
        model = Category
        fields = ['name', 'status']  

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CategoryForm, self).__init__(*args, **kwargs)
        if not self.instance.pk: 
            self.fields['status'].initial = '1'

    def clean(self):
        cleaned_data = super().clean()
        user_instance = getattr(_thread_local, 'user', None)
        if user_instance:
            self.instance.admin_id = user_instance 
        else:
            self.instance.admin_id = None 

        # print('user instance : ', user_instance)
        # print('clean data : ', self.instance.admin_id)
        return cleaned_data
    
class UnitForm(forms.ModelForm):
    name = forms.CharField(required=True)
    unit_value = forms.IntegerField(required=True)
    status = forms.CharField(required=False) 

    class Meta:
        model = Unit
        fields = ['name', 'unit_value', 'status']  

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UnitForm, self).__init__(*args, **kwargs)
        if not self.instance.pk: 
            self.fields['status'].initial = '1'

    def clean(self):
        cleaned_data = super().clean()
        user_instance = getattr(_thread_local, 'user', None)
        if user_instance:
            self.instance.admin_id = user_instance 
        else:
            self.instance.admin_id = None 

        # print('user instance : ', user_instance)
        # print('clean data : ', self.instance.admin_id)
        return cleaned_data
    
class TypeForm(forms.ModelForm):
    name = forms.CharField(required=True)
    status = forms.CharField(required=False) 

    class Meta:
        model = Type
        fields = ['name', 'status']  

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(TypeForm, self).__init__(*args, **kwargs)
        if not self.instance.pk: 
            self.fields['status'].initial = '1'

    def clean(self):
        cleaned_data = super().clean()
        user_instance = getattr(_thread_local, 'user', None)
        if user_instance:
            self.instance.admin_id = user_instance 
        else:
            self.instance.admin_id = None 

        # print('user instance : ', user_instance)
        # print('clean data : ', self.instance.admin_id)
        return cleaned_data
    
class LeafForm(forms.ModelForm):
    name = forms.CharField(required=True)
    quantity = forms.IntegerField(required=True)
    status = forms.CharField(required=False) 
    class Meta:
        model = Leaf
        fields = ['name', 'quantity', 'status']  

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(LeafForm, self).__init__(*args, **kwargs)
        if not self.instance.pk: 
            self.fields['status'].initial = '1'

    def clean(self):
        cleaned_data = super().clean()
        user_instance = getattr(_thread_local, 'user', None)
        if user_instance:
            self.instance.admin_id = user_instance 
        else:
            self.instance.admin_id = None 

        # print('user instance : ', user_instance)
        # print('clean data : ', self.instance.admin_id)
        return cleaned_data
