from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Snack
from django.urls import reverse

# Create your tests here.

class SnackTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="tester", email="tester@email.com", password="tester")

        self.snack = Snack.objects.create(title="Yuengeling", purchaser=self.user, description="good beer")

    def string_representation(self):
        self.assertEqual(str(self.snack), 'Yuengeling')
    
    def test_snack_content(self):
        self.assertEqual(f"{self.snack.title}", 'Yuengeling')
        self.assertEqual(f"{self.snack.purchaser}", "tester")
        self.assertEqual(f"{self.snack.description}", "good beer")

    def test_thing_detail_view(self):
        response = self.client.get(reverse("snack_detail", args="1"))
        no_response = self.client.get("/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Purchaser: tester")
        self.assertTemplateUsed(response, "snack_detail.html")

    def test_snack_list_view(self):
        response = self.client.get(reverse('snack_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Yuengeling")
        self.assertTemplateUsed(response, 'snack_list.html')

    def test_snack_create_view(self):
        response = self.client.post(
            reverse("snack_create"),
            {
                'title': 'Oatmeal',
                'purchaser': self.user.id,
                'description': 'good for breakfast'
            },
            follow=True
        )
        self.assertRedirects(response, reverse('snack_create', args=[self.id]))
        self.assertContains(response, "Oatmeal")

    def test_snack_update_view_redirect(self):
        response = self.client.post(
            reverse("snack_update", args="1"),
            {"title": "updated title", "purchaser": self.user.id, "description": "updated description"},
        )

        self.assertRedirects(
            response, reverse("snack_detail", args="1"), target_status_code=200
        )

    def test_snack_update_bad_url(self):
        response = self.client.post(
                   reverse("snack_update", args="9"),
            {"title": "updated title", "purchaser": self.user.id, "description": "updated description"},
        )

        self.assertEqual(response.status_code, 404)

    def test_snack_delete(self):
        response = self.client.get(reverse('snack_delete', args="1"))
        self.assertEqual(response.status_code, 200)

    def test_model(self):
        snack = Snack.objects.create(title="Oatmeal", purchaser=self.user)
        self.assertEqual(snack.title, "Oatmeal")