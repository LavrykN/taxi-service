from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    ManufacturerSearchForm,
    CarSearchForm,
    DriverSearchForm
)
from taxi.models import Manufacturer, Car


class FormsTests(TestCase):
    def test_driver_creation_form(self):
        form_data = {
            "username": "Sisun123",
            "password1": "qwe1234567",
            "password2": "qwe1234567",
            "first_name": "Anton",
            "last_name": "Sisun",
            "license_number": "ABC12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_search_fields(self):
        manufacturer = Manufacturer.objects.create(
            name="BAIC",
            country="China"
        )
        Car.objects.create(model="Arcfox Alpha-S", manufacturer=manufacturer)

        manufacturer_form = ManufacturerSearchForm(data={"name": "Ba"})
        car_form = CarSearchForm(data={"model": "Arc"})
        driver_form = DriverSearchForm(data={"username": "us"})

        self.assertTrue(manufacturer_form.is_valid())
        self.assertTrue(car_form.is_valid())
        self.assertTrue(driver_form.is_valid())

        self.assertEqual(manufacturer_form.cleaned_data["name"], "Ba")
        self.assertEqual(car_form.cleaned_data["model"], "Arc")
        self.assertEqual(driver_form.cleaned_data["username"], "us")
