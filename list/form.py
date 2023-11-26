from django import forms
from .timebox_models import *

class CreateNewItem(forms.Form): #the form name. Inherit from form. #Field are the same in the database. Create the attributes
    name = forms.CharField(label="Name", max_length=200,) #string label field
    # check = forms.BooleanField(required=False) #checklist button. #default required is True. If it's true, the checklist button must be on check
    #                                            # in order for the form to submitted. If it False, the checklist button is optional

class ChangeListName(forms.Form):
   name = forms.CharField(label="Name", max_length=200,)

class CreateNewList(forms.Form):
    name  = forms.CharField(label="Name", max_length=200,)

class CreateQuarterlyGoal(forms.ModelForm):
    class Meta:
        model = Quarterly_goal
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'style':''}),
        } # name label is a text input label

class CreateMonthlyGoal(forms.ModelForm):
    class Meta:
        model = Monthly_goal
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'style':''}),
        } # name label is a text input label

class CreateWeeklyGoal(forms.ModelForm):
    class Meta:
        model = Weekly_goal
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'style':''}),
        } # name label is a text input label
