import os
import django
from django.test import TestCase
import semWork
from semWork import wsgi, celery, asgi

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'semWork.settings')
django.setup()

from django.core.files.uploadedfile import SimpleUploadedFile
from myClothes.forms import ClothingItemForm, CreatePostForm, CommentForm, SearchForm
from myClothes.models import Category, Subcategory, ClothingItem, Recommendation
from authorization.models import User


class ClothingItemFormTest(TestCase):
    def test_valid_category(self):
        category = Category.objects.create(name='TestCategory')
        subcategory = Subcategory.objects.create(name='TestSubcategory', category=category)
        image_path = os.path.join('media', 'clothing_images', 'куртка.jpeg')
        image_content = open(image_path, 'rb').read()
        image = SimpleUploadedFile('куртка.jpeg', image_content, content_type='image/jpeg')

        form_data = {
            'category': category.pk,
            'subcategory': subcategory.pk,
            'description': 'Test description',
            'image': image,
        }
        form = ClothingItemForm(data=form_data, files={'image': image})
        self.assertTrue(form.fields['category'].required)
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        category = Category.objects.create(name='TestCategory')
        subcategory = Subcategory.objects.create(name='TestSubcategory', category=category)
        image_path = os.path.join('media', 'clothing_images', 'куртка.jpeg')
        image_content = open(image_path, 'rb').read()
        image = SimpleUploadedFile('куртка.jpeg', image_content, content_type='image/jpeg')

        form_data = {
            'image': image,
            'category': category,
            'subcategory': subcategory,
            'description': '',
        }
        form = ClothingItemForm(data=form_data, files={'image': image})
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)

    def test_empty_image(self):
        category = Category.objects.create(name='TestCategory')
        subcategory = Subcategory.objects.create(name='TestSubcategory', category=category)

        form_data = {
            'image': None,
            'category': category,
            'subcategory': subcategory,
            'description': 'Test description',
        }
        form = ClothingItemForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('image', form.errors)


class CreatePostFormTest(TestCase):
    def test_valid_data(self):
        form_data = {
            'outfit_id': 1,
            'text': 'Test text',
        }
        form = CreatePostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form_data = {
            'outfit_id': None,
            'text': '',
        }
        form = CreatePostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('outfit_id', form.errors)
        self.assertIn('text', form.errors)


class CommentFormTest(TestCase):
    def test_valid_data(self):
        form_data = {
            'post_id': 1,
            'text': 'Test comment',
        }
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form_data = {
            'post_id': None,
            'text': '',
        }
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('post_id', form.errors)
        self.assertIn('text', form.errors)


class SearchFormTest(TestCase):
    def test_valid_data(self):
        form_data = {
            'username': 'testuser',
        }
        form = SearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form_data = {
            'username': '',
        }
        form = SearchForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)


class ClothingItemFormInitTest(TestCase):
    def test_form_init(self):
        form = ClothingItemForm()
        self.assertIn('subcategory', form.fields)
        self.assertTrue(form.fields['subcategory'].required)
        self.assertIn('onchange', form.fields['category'].widget.attrs)


class ClothingItemFormCategoryChangeTest(TestCase):
    def test_category_change(self):
        category = Category.objects.create(name='TestCategory')
        subcategory1 = Subcategory.objects.create(name='Subcategory1', category=category)
        subcategory2 = Subcategory.objects.create(name='Subcategory2', category=category)
        form_data = {
            'category': category.pk,
        }
        form = ClothingItemForm(data=form_data)
        self.assertEqual(list(form.fields['subcategory'].queryset), [subcategory1, subcategory2])


class ClothingItemFormCategoryChangeInvalidTest(TestCase):
    def test_category_change_invalid(self):
        form_data = {
            'category': 'invalid_category',
        }
        form = ClothingItemForm(data=form_data)
        self.assertEqual(form.fields['subcategory'].widget.attrs.get('disabled'), 'disabled')


class CreatePostFormFieldsTest(TestCase):
    def test_form_fields(self):
        form = CreatePostForm()
        self.assertIn('outfit_id', form.fields)
        self.assertIn('text', form.fields)


class CommentFormFieldsTest(TestCase):
    def test_form_fields(self):
        form = CommentForm()
        self.assertIn('post_id', form.fields)
        self.assertIn('text', form.fields)


class SearchFormFieldsTest(TestCase):
    def test_form_fields(self):
        form = SearchForm()
        self.assertIn('username', form.fields)


class CategoryModelTest(TestCase):
    def test_category_model(self):
        category = Category.objects.create(name='Test Category')
        self.assertEqual(str(category), 'Test Category')


class SubcategoryModelTest(TestCase):
    def test_subcategory_model(self):
        category = Category.objects.create(name='Test Category')
        subcategory = Subcategory.objects.create(category=category, name='Test Subcategory')
        self.assertEqual(str(subcategory), 'Test Subcategory')


class ClothingItemModelTest(TestCase):
    def test_clothing_item_model(self):
        user = User.objects.create(username='testuser', email='testclothing@example.com')
        category = Category.objects.create(name='Test Category')
        subcategory = Subcategory.objects.create(category=category, name='Test Subcategory')
        clothing_item = ClothingItem.objects.create(user=user, category=category, subcategory=subcategory, description='Test Description')
        self.assertEqual(str(clothing_item), 'Test Description')


class RecommendationModelTest(TestCase):
    def test_recommendation_model(self):
        category = Category.objects.create(name='Test Category')
        subcategory = Subcategory.objects.create(category=category, name='Test Subcategory')
        recommendation = Recommendation.objects.create(category=category, subcategory=subcategory, description='Test Description')
        self.assertEqual(str(recommendation), 'Test Description')

class ViewTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name='Test category')
        subcategory = Subcategory.objects.create(category=category,name='Test subcategory')
        self.user = User.objects.create(username='TestUser', password='testpassword', email='11@gmail.com')
        self.clothing_item = ClothingItem.objects.create(user=self.user,subcategory=subcategory, description='Test item',category=category)


    def test_add_clothing_item(self):
        self.client.force_login(self.user)
        response = self.client.get('/add_clothes/')
        self.assertEqual(response.status_code, 200)

    def test_all_clothes(self):
        self.client.force_login(self.user)
        response = self.client.get('/all_clothes/')
        self.assertEqual(response.status_code, 200)

    def test_edit_clothing_item(self):
        response = self.client.get(f'/edit_clothing_item/{self.clothing_item.id}/')
        self.assertEqual(response.status_code, 200)

    def test_create_outfit(self):
        self.client.force_login(self.user)
        response = self.client.get('/createOutfit/')
        self.assertEqual(response.status_code, 200)

    def test_outfits(self):
        self.client.force_login(self.user)
        response = self.client.get('/allOutfits/')
        self.assertEqual(response.status_code, 200)

