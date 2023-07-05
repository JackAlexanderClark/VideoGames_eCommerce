from django.test import TestCase, Client
from django.urls import reverse
from shipping.models import Order
from django.contrib.auth.models import User

# Create your tests here.
class TestViews(TestCase):

    def setUp(self):
        # Set up method is called before each test
        self.client = Client()
        self.remove_game_item_url = reverse('remove_game_item', args=['some_id'])

    def test_remove_game_item_POST(self):

        # Create a test order
        test_order = Order.objects.create(
            order_id='some_id',
            quantity=10
            # add other necessary fields here
        )

        response = self.client.post(self.remove_game_item_url)

        # refresh the object from db
        test_order.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": True})
        self.assertEqual(test_order.quantity, 9)

    def test_remove_game_item_POST_zero_quantity(self):

        # Create a test order
        test_order = Order.objects.create(
            order_id='some_id',
            quantity=0
            # add other necessary fields here
        )

        response = self.client.post(self.remove_game_item_url)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"success": False})
