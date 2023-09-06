import datetime
from django import forms
from .models import *
from my_account.models import User
from .custom_widget import DateInput
from utils.dairyapp.decideshift import getShift
from django.utils.translation import gettext_lazy as _



class CreateFatForm(forms.ModelForm):

    # fat_rate = forms.FloatField(widget=forms.NumberInput(attrs={"class": "form-control","placeholder":"enter your email"}))
    dairy = forms.ModelChoiceField(queryset=None,widget=forms.Select(attrs={"class":"form-control","maxlength":6}))
    # foo_select = forms.ModelMultipleChoiceField(queryset=None)

    def __init__(self,request,*args, **kwargs):
        super().__init__(*args, **kwargs)
        print("------------")
        self.fields["dairy"].queryset = Dairy.objects.filter(user=request.user)
    class Meta:
        model = FatRate
        fields = ["fat_rate","dairy"]

        widgets ={
            # 'country':CountrySelectWidget(attrs={"class": "form-select"}),
            'fat_rate':forms.NumberInput(attrs={"class": "form-control","placeholder":"enter fat rate"}),
            # 'dairy':forms.ChoiceField(widget=forms.ModelChoiceIterator())
            # 'username':forms.TextInput(attrs={"class": "form-control","placeholder":"enter your name","minlength":3})
            #'password':forms.PasswordInput(attrs={"class": "form-control"})
        }

    def clean_fat_rate(self):
        fat_rate = self.cleaned_data['fat_rate']
        if fat_rate < 0:
            raise forms.ValidationError(_('fat rate should be positive'))
        
        return fat_rate
    

class CreateDairyForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(required=False,queryset=User.objects.filter(is_active=True),widget=forms.SelectMultiple(attrs={"class": "form-control dairy-member-select"}))
    class Meta:
        model = Dairy
        fields = ["name","location","members"]

        widgets = {
            'name':forms.TextInput(attrs={"class": "form-control","placeholder":"enter dairy name","maxlength":200}),
            'location':forms.TextInput(attrs={"class": "form-control","placeholder":"enter dairy location"}),
            # 'members': forms.ModelMultipleChoiceField(queryset=User.objects.filter(is_active=True),widget=forms.SelectMultiple(attrs={"class": "form-control"}))
        }

import datetime
class CreateMilkRecordForm(forms.ModelForm):
    shiftinfo = getShift()
    # if 
    user = forms.ModelChoiceField(queryset=None,widget=forms.Select(attrs={"class":"form-select"}))
    dairy = forms.ModelChoiceField(queryset=None,initial=2,widget=forms.Select(attrs={"class":"form-select"}))
    date = forms.DateField(initial=datetime.datetime.now(),widget=DateInput(attrs={"class":"form-control date-picker","placeholder":"dd-mm-yyyy"},format="%Y-%m-%d"))
    shift = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-select"}),initial=shiftinfo,choices=MilkRecord.shift_choices)
    # input_formats=['%Y%m%d']
    class Meta:
        model = MilkRecord
        fields = ["shift","dairy","user","milk_weight","milk_fat","date"]

        widgets = {
            # 'shift':forms.Select(attrs={"class":"form-select"}),
            'milk_weight':forms.NumberInput(attrs={"class":"form-control"}),
            'milk_fat':forms.NumberInput(attrs={"class":"form-control","min":"0"}),
        }
    def __init__(self,dairy,*args, **kwargs):
        super().__init__(*args, **kwargs)
        print("------------")
        self.fields["user"].queryset = dairy.members.all()
        self.fields["dairy"].queryset = Dairy.objects.filter(id=dairy.id)
        print("last of init")
    
    def clean_milk_fat(self):
        value = float(self.cleaned_data['milk_fat'])
        lower_bound = 0
        upper_bound = 20
        
        if  (lower_bound <= value <=upper_bound):
            return self.cleaned_data['milk_fat']
        
        raise forms.ValidationError(_("Milk fat should be between %(low_range)d and %(high_range)d") % {'low_range':0,'high_range':20})