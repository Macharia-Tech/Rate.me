from django import forms
from .models import Profile,Project,Rating

class NewProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['editor','profile','pub_date']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }
        
class NewProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        exclude=['editor']
        widgets={
            'tags':forms.CheckboxSelectMultiple(),
        }
class NewRatingForm(forms.ModelForm):
    class Meta:
        model=Rating
        exclude=['editor','project']
        widgets={
            
            'tags':forms.CheckboxSelectMultiple
        }