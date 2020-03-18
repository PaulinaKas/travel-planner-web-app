from django.test import TestCase
from weather_app.models import List, City, Schedule
from django.core.exceptions import ValidationError

class CityModelTest(TestCase):

    def test_default_cities(self):
        city = City()
        self.assertEqual(city.name,'')

    def test_city_is_related_to_list(self):
        list_ = List.objects.create()
        city = City(name = 'City',
                    list = list_,
                    )
        city.save()
        self.assertIn(city, list_.city_set.all())

    def test_can_save_the_same_city_to_different_list(self):
        list_first = List.objects.create()
        list_second = List.objects.create()
        City.objects.create(name = 'City',
                            list = list_first)
        city = City(name = 'City',
                    list = list_second)
        city.full_clean()


class ListModelTest(TestCase):

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), '/lists/%d/' % (list_.id,))

    def test_cannot_save_empty_list(self):
        list_ = List.objects.create()
        city = City(list=list_, name='')
        with self.assertRaises(ValidationError):
            city.save()
            city.full_clean()

    def test_save_and_retrieve_cities(self):
        list_ = List()
        list_.save()

        first_city = City()
        first_city.name = 'First city'
        first_city.list = list_
        first_city.save()

        second_city = City()
        second_city.name = 'Second city'
        second_city.list = list_
        second_city.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_cities = City.objects.all()
        self.assertEqual(saved_cities.count(), 2)

        first_saved_city = saved_cities[0]
        second_saved_city = saved_cities[1]
        self.assertEqual(first_saved_city.name, 'First city')
        self.assertEqual(first_saved_city.list, list_)
        self.assertEqual(second_saved_city.name, 'Second city')
        self.assertEqual(second_saved_city.list, list_)

class ScheduleModelTest(TestCase):

    def test_default_schedules(self):
        schedule = Schedule()
        self.assertEqual(schedule.text,'')
