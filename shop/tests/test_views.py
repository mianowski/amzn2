import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Product
from ..serializers import ProductSerializer


# initialize the APIClient app
client = Client()


class GetAllProductsTest(TestCase):
    """ Test module for GET all products API """

    def setUp(self):
        Product.objects.create(
            name='book', price_in_dollars=1.23, barcode='09asd', description='Best book ever')

    def test_get_all_products(self):
        # get API response
        response = client.get(reverse('get_post_products'))
        # get data from db
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleProductTest(TestCase):
    """ Test module for GET single product API """

    def setUp(self):
        self.casper = Product.objects.create(
            name='Casper', age=3, breed='Bull Dog', color='Black')
        self.muffin = Product.objects.create(
            name='Muffin', age=1, breed='Gradane', color='Brown')
        self.rambo = Product.objects.create(
            name='Rambo', age=2, breed='Labrador', color='Black')
        self.ricky = Product.objects.create(
            name='Ricky', age=6, breed='Labrador', color='Brown')

    def test_get_valid_single_product(self):
        response = client.get(
            reverse('get_delete_update_product', kwargs={'pk': self.rambo.pk}))
        product = Product.objects.get(pk=self.rambo.pk)
        serializer = ProductSerializer(product)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_product(self):
        response = client.get(
            reverse('get_delete_update_product', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewProductTest(TestCase):
    """ Test module for inserting a new product """

    def setUp(self):
        self.valid_payload = {
            'name': 'Muffin',
            'age': 4,
            'breed': 'Pamerion',
            'color': 'White'
        }

        self.invalid_payload = {
            'name': '',
            'age': 4,
            'breed': 'Pamerion',
            'color': 'White'
        }

    def test_create_valid_product(self):
        response = client.post(
            reverse('get_post_products'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_product(self):
        response = client.post(
            reverse('get_post_products'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleProductTest(TestCase):
    """ Test module for updating an existing product record """

    def setUp(self):
        self.casper = Product.objects.create(
            name='Casper', age=3, breed='Bull Dog', color='Black')
        self.muffin = Product.objects.create(
            name='Muffy', age=1, breed='Gradane', color='Brown')
        self.valid_payload = {
            'name': 'Muffy',
            'age': 2,
            'breed': 'Labrador',
            'color': 'Black'
        }

        self.invalid_payload = {
            'name': '',
            'age': 4,
            'breed': 'Pamerion',
            'color': 'White'
        }

    def test_valid_update_product(self):
        response = client.put(
            reverse('get_delete_update_product',
                    kwargs={'pk': self.muffin.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_product(self):
        response = client.put(
            reverse('get_delete_update_product',
                    kwargs={'pk': self.muffin.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleProductTest(TestCase):
    """ Test module for deleting an existing product record """

    def setUp(self):
        self.casper = Product.objects.create(
            name='Casper', age=3, breed='Bull Dog', color='Black')
        self.muffin = Product.objects.create(
            name='Muffy', age=1, breed='Gradane', color='Brown')

    def test_valid_delete_product(self):
        response = client.delete(
            reverse('get_delete_update_product', kwargs={'pk': self.muffin.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_product(self):
        response = client.delete(
            reverse('get_delete_update_product', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
