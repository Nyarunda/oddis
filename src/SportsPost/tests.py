from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from .models import Question
# Create your tests here.

User = get_user_model()

class SportsModelTestCase(TestCase):
	def setUp(self):
		new_user = User.objects.create(username='Ezraoououjon')

	def test_post_item(self):
		obj = Question.objects.create(
				user=User.objects.first(),
				content='Some random info'
			)
		self.assertTrue(obj.content == "Some random info")
		self.assertTrue(obj.id ==1)
		absolute_url = reverse("postsports:detail", kwargs={"pk": 1})
		self.assertEqual(obj.get_absolute_url(), absolute_url)