from django.test import TestCase
from django.utils.html import escape
from django.shortcuts import get_object_or_404
from django.urls import resolve, reverse
from django.core.exceptions import ValidationError
from unittest import skip

from weather_app.forms import CityForm, ScheduleForm, EMPTY_CITY_ERROR
from weather_app.models import City, List, Schedule


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


    def test_home_page_uses_city_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], CityForm)


class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'name': 'New city'})
        self.assertEqual(City.objects.count(), 1)
        new_city = City.objects.first()
        self.assertEqual(new_city.name, 'New city')


    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'name': 'New city'})
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))


    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post('/lists/new', data={'name': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')


    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post('/lists/new', data={'name': ''})
        self.assertContains(response, escape(EMPTY_CITY_ERROR))


    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post('/lists/new', data={'name': ''})
        self.assertIsInstance(response.context['form'], CityForm)


    def test_invalid_cities_arent_saved(self):
        self.client.post('/lists/new', data={'name': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(City.objects.count(), 0)



class ViewListTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertTemplateUsed(response, 'list.html')


    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)


    def test_displays_city_form(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertIsInstance(response.context['form'], CityForm)
        self.assertContains(response, 'name="name"')


    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(
            '/lists/%d/' % (list_.id,),
            data={'name': ''}
        )


    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(City.objects.count(), 0)


    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')


    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], CityForm)


    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_CITY_ERROR))


    def test_displays_only_cities_for_that_list(self):
        correct_list = List.objects.create()
        Schedule.objects.create()
        City.objects.create(name = 'London',
                            list = correct_list)

        Schedule.objects.create()
        City.objects.create(name = 'Warsaw',
                            list = correct_list)

        other_list = List.objects.create()
        Schedule.objects.create()
        City.objects.create(name = 'Taiwan',
                            list = other_list)

        Schedule.objects.create()
        City.objects.create(name = 'Moscow',
                            list = other_list)


        response = self.client.get('/lists/%d/' % (correct_list.id,))

        self.assertContains(response, 'London')
        self.assertContains(response, 'Warsaw')
        self.assertNotContains(response, 'Taiwan')
        self.assertNotContains(response, 'Moscow')

    def test_cannot_save_empty_city(self):
        list_ = List.objects.create()
        city = City()
        city.name = ''
        city.list = list_
        with self.assertRaises(ValidationError):
            city.save()
            city.full_clean()

    def test_redirects_after_POST_city(self):
        list_ = List.objects.create()
        schedule = Schedule.objects.create()
        response = self.client.post('/lists/%d/' % (list_.id,),
                                    data={'name': 'London'})

        self.assertRedirects(response, '/lists/%d/' % (list_.id,))


class AddScheduleTest(TestCase):

    def test_add_not_empty_schedule(self):
        list_ = List.objects.create()
        city = City.objects.create(list = list_,
                                   name = 'London',)
        schedule = Schedule.objects.create()
        self.client.get('/lists/%d/' % (list_.id,))
        self.assertEqual(schedule.text, '')

        self.client.post(reverse('add_schedule',
                                 kwargs={'schedule_id': schedule.id,
                                         'list_id': list_.id,}
                                 ),
                         data = {'text': 'Some schedule'})
        self.assertNotEqual(schedule.text, 'Some schedule')


class DeleteCityTest(TestCase):

    def test_delete_added_cities(self):
        list_ = List.objects.create()
        city = City.objects.create(list = list_,
                                   name = 'City',)
        Schedule.objects.create()
        self.client.get('/lists/%d/' % (list_.id,))
        self.assertEqual(City.objects.all().count(), 1)

        self.client.post(reverse('delete_city', kwargs={'city_id': city.id,
                                                        'list_id': list_.id,
                                                        }))
        self.assertEqual(City.objects.all().count(), 0)
