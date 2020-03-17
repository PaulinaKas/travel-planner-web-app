from django import forms
from .models import City, Schedule

EMPTY_CITY_ERROR = "You can't have an empty city name in your travel schedule"

class CityForm(forms.models.ModelForm):

    class Meta:
        model = City
        fields = ('name',)
        widgets = {
            'name': forms.fields.TextInput(attrs={
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

class ScheduleForm(forms.models.ModelForm):
    class Meta:
        model = Schedule
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={
                    'class' : 'input',
                    'placeholder' : 'Add your travel schedule',
                }),
            }
