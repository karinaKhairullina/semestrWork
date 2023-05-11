from django.shortcuts import render, redirect, get_object_or_404
from .forms import ClothingItemForm
from .models import Subcategory, Category, Image, ClothingItem
from django.contrib.sessions.backends.db import SessionStore


# добавление одежды
def add_clothing_item(request):
    if request.method == 'POST':
        form = ClothingItemForm(request.POST, request.FILES)
        if form.is_valid():
            clothing_item = form.save(commit=False)
            clothing_item.user = request.user

            # Проверяем наличие категории и подкатегории в базе данных
            category, _ = Category.objects.get_or_create(name=clothing_item.category.name)
            subcategory, _ = Subcategory.objects.get_or_create(category=category, name=clothing_item.subcategory.name)

            clothing_item.category = category
            clothing_item.subcategory = subcategory
            clothing_item.save()

            # Сохраняем изображение и добавляем связь с clothing_item через ManyToManyField
            for image in request.FILES.getlist('image'):
                img = Image.objects.create(image=image)
                clothing_item.images.add(img)

            form.save_m2m()

            # сохраняем данные в сессию
            session = SessionStore()
            session.create()
            session_data = {
                'category': category.name,
                'subcategory': subcategory.name,
                'description': clothing_item.description,
                'images': [img.image.url for img in clothing_item.images.all()]
            }
            session['clothing_item_data'] = session_data
            session.save()

            return redirect('all_clothes')
    else:
        form = ClothingItemForm()
    return render(request, 'addClothes.html', {'form': form})


# вся одежда
def all_clothes(request):
    clothing_items = ClothingItem.objects.filter(user=request.user).order_by('category__name', 'subcategory__name')
    return render(request, 'allClothes.html', {'clothing_items': clothing_items, 'id': ''})



# Редактирование одежды

def edit_clothing_item(request, id):
    clothing_item = ClothingItem.objects.get(id=id)
    if request.method == 'POST':
        form = ClothingItemForm(request.POST, request.FILES, instance=clothing_item)
        if form.is_valid():
            clothing_item = form.save(commit=False)
            clothing_item.user = request.user

            # Проверяем наличие категории и подкатегории в базе данных
            category, _ = Category.objects.get_or_create(name=clothing_item.category.name)

            # Проверяем, выбрана ли подкатегория
            subcategory = clothing_item.subcategory
            if subcategory is None:
                subcategory = None
            else:
                subcategory, _ = Subcategory.objects.get_or_create(category=category, name=subcategory.name)

            clothing_item.category = category
            clothing_item.subcategory = subcategory

            # сохраняем изображения
            clothing_item.images.clear()
            for image in request.FILES.getlist('image'):
                img = Image.objects.create(image=image)
                clothing_item.images.add(img)

            clothing_item.save()
            form.save_m2m()

            # обновляем данные в сессии
            session = request.session
            session_data = {
                'category': category.name,
                'subcategory': subcategory.name if subcategory else None,
                'description': clothing_item.description,
                'images': [img.image.url for img in clothing_item.images.all()]
            }
            session['clothing_item_data'] = session_data
            session.save()

            return redirect('all_clothes')
    else:
        form = ClothingItemForm(instance=clothing_item)
    return render(request, 'addClothes.html', {'form': form})














