from django.test import TestCase
from weather_app.forms import CityForm, ScheduleForm, EMPTY_CITY_ERROR
from weather_app.models import City, List, Schedule

class CityFormTest(TestCase):

    def test_form_renders_CityForm_field_input(self):
        form = CityForm()

        self.assertIn('placeholder="Enter a city"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())


    def test_form_validation_for_blank_cities(self):
        form = CityForm(data={'name': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['name'], [EMPTY_CITY_ERROR])


    def test_form_save_handles_saving_to_a_list(self):
        list_ = List.objects.create()
        form = CityForm(data={'name': 'City'})
        new_city = form.save(for_list=list_)
        self.assertEqual(new_city, City.objects.first())
        self.assertEqual(new_city.name, 'City')
        self.assertEqual(new_city.list, list_)

class ScheduleFormTest(TestCase):

    def test_form_renders_ScheduleForm_field_input(self):
        form = ScheduleForm()

        self.assertIn('placeholder="Add your travel schedule"', form.as_p())
        self.assertIn('class="input"', form.as_p())
