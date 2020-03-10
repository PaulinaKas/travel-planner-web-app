from django import forms
from .models import City, TravelPlan

class CityForm(forms.models.ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {
            'name': forms.fields.TextInput(attrs={
                    'class' : 'input',
                    'placeholder' : 'City Name',
                }),
            }

class PlanForm(forms.models.ModelForm):
    class Meta:
        model = TravelPlan
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                    'class' : 'input',
                    'placeholder' : 'Add your travel plan',
                }),
            }
