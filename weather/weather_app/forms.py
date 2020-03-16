from django import forms
from .models import City

EMPTY_CITY_ERROR = "You can't have an empty city name in your travel schedule"

class CityForm(forms.models.ModelForm):

    class Meta:
        model = City
        fields = ('name',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a city',
                'class': 'form-control input-lg',
            }),
        }
        error_messages = {
            'name': {'required': EMPTY_CITY_ERROR}
        }


    def save(self, for_list):
        self.instance.list = for_list
        return super().save()

# class PlanForm(forms.models.ModelForm):
#     class Meta:
#         model = TravelPlan
#         fields = ['text']
#         widgets = {
#             'text': forms.Textarea(attrs={
#                     'class' : 'input',
#                     'placeholder' : 'Add your travel plan',
#                 }),
#             }
