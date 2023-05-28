from subscribe.forms import CommentForm, CreatePostForm, SearchForm
from django.test import TestCase
from authorization.models import User
from myClothes.models import Outfit, Image
from subscribe.models import Post


class CreatePostFormTest(TestCase):

    def test_form_valid(self):
        form_data = {
            'selected_images': [],
            'title': 'Test Post',
            'text': 'This is a test post.',
        }
        form = CreatePostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form_data = {
            'selected_images': [],
            'title': '',
            'text': 'This is a test post.',
        }
        form = CreatePostForm(data=form_data)
        self.assertFalse(form.is_valid())


class CommentFormTest(TestCase):

    def test_form_valid(self):
        form_data = {
            'post_id': 1,
            'text': 'This is a test comment.',
        }
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form_data = {
            'post_id': None,  # Missing post_id
            'text': '',  # Empty comment text
        }
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)


class SearchFormTest(TestCase):

    def test_form_valid(self):
        form_data = {
            'username': 'testuser',
        }
        form = SearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form_data = {
            'username': '',
        }
        form = SearchForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)


class PostModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='testuser')
        outfit = Outfit.objects.create(name='Test Outfit', user=user)
        image = Image.objects.create(image='куртка.jpeg')
        post = Post.objects.create(user=user, outfit=outfit, title='Test Post', text='This is a test post.')
        post.images.add(image)

    def test_str_representation(self):
        post = Post.objects.get(id=1)
        self.assertEqual(str(post), 'Test Post')

    def test_post_attributes(self):
        post = Post.objects.get(id=1)
        self.assertEqual(post.user.username, 'testuser')
        self.assertEqual(post.outfit.name, 'Test Outfit')
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.text, 'This is a test post.')
        self.assertEqual(post.images.count(), 1)
