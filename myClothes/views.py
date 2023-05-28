from django.shortcuts import render, redirect, get_object_or_404
from subscribe.models import Post
from .forms import ClothingItemForm, CreatePostForm
from .models import Subcategory, Category, Image, ClothingItem, Outfit, Recommendation
from django.contrib.sessions.backends.db import SessionStore


def add_clothing_item(request):
    """
    Добавляет новый предмет одежды.

    Args:
        request (HttpRequest): HTTP-запрос.

    Returns:
        HttpResponse: HTTP-ответ.

    """
    if request.method == 'POST':
        form = ClothingItemForm(request.POST, request.FILES)
        if form.is_valid():
            clothing_item = form.save(commit=False)
            clothing_item.user = request.user

            category, _ = Category.objects.get_or_create(name=clothing_item.category.name)
            subcategory, _ = Subcategory.objects.get_or_create(category=category, name=clothing_item.subcategory.name)

            clothing_item.category = category
            clothing_item.subcategory = subcategory
            clothing_item.save()

            for image in request.FILES.getlist('image'):
                img = Image.objects.create(image=image)
                clothing_item.images.add(img)

            form.save_m2m()

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


def all_clothes(request):
    """
    Отображает все предметы одежды.

    Args:
        request (HttpRequest): HTTP-запрос.

    Returns:
        HttpResponse: HTTP-ответ.

    """
    clothing_items = ClothingItem.objects.filter(user=request.user).order_by('category__name', 'subcategory__name')
    recommendations = Recommendation.objects.filter(
        category__in=clothing_items.values('category'),
        subcategory__in=clothing_items.values('subcategory')
    )
    return render(request, 'allClothes.html', {'clothing_items': clothing_items, 'recommendations': recommendations})


def edit_clothing_item(request, id):
    """
    Редактирует предмет одежды.

    Args:
        request (HttpRequest): HTTP-запрос.
        id (int): Идентификатор предмета одежды.

    Returns:
        HttpResponse: HTTP-ответ.

    """
    clothing_item = ClothingItem.objects.get(id=id)
    if request.method == 'POST':
        form = ClothingItemForm(request.POST, request.FILES, instance=clothing_item)
        if form.is_valid():
            clothing_item = form.save(commit=False)
            clothing_item.user = request.user

            category, _ = Category.objects.get_or_create(name=clothing_item.category.name)

            subcategory = clothing_item.subcategory
            if subcategory is None:
                subcategory = None
            else:
                subcategory, _ = Subcategory.objects.get_or_create(category=category, name=subcategory.name)

            clothing_item.category = category
            clothing_item.subcategory = subcategory

            clothing_item.images.clear()
            for image in request.FILES.getlist('image'):
                img = Image.objects.create(image=image)
                clothing_item.images.add(img)

            clothing_item.save()
            form.save_m2m()

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


def delete_clothing_item(request, id):
    """
    Удаляет предмет одежды.

    Args:
        request (HttpRequest): HTTP-запрос.
        id (int): Идентификатор предмета одежды.

    Returns:
        HttpResponse: HTTP-ответ.

    """
    clothing_item = get_object_or_404(ClothingItem, id=id)
    clothing_item.delete()
    return redirect('all_clothes')


def create_outfit(request):
    """
    Создает новый комплект одежды.

    Args:
        request (HttpRequest): HTTP-запрос.

    Returns:
        HttpResponse: HTTP-ответ.

    """
    user = request.user
    clothing_items = ClothingItem.objects.filter(user=user)

    if request.method == 'POST':
        outfit_name = request.POST.get('outfit_name')
        selected_items = request.POST.getlist('selected_items')
        outfit = Outfit.objects.create(user=user, name=outfit_name)
        outfit.items.set(selected_items)
        return redirect('outfits')

    context = {
        'clothing_items': clothing_items,
    }
    return render(request, 'createOutfit.html', context)


def outfits(request):
    """
    Отображает все комплекты одежды.

    Args:
        request (HttpRequest): HTTP-запрос.

    Returns:
        HttpResponse: HTTP-ответ.

    """
    user = request.user
    outfits = Outfit.objects.filter(user=user)

    context = {
        'outfits': outfits,
    }
    return render(request, 'allOutfits.html', context)


def create_post(request):
    """
    Создает новый пост.

    Args:
        request (HttpRequest): HTTP-запрос.

    Returns:
        HttpResponse: HTTP-ответ.

    """
    user = request.user
    if request.method == 'POST':
        outfit_id = request.POST.get('outfit_id')
        title = request.POST.get('title')
        text = request.POST.get('text')
        outfit = get_object_or_404(Outfit, pk=outfit_id)
        post = Post.objects.create(user=user, outfit=outfit, title=title, text=text)

        for item in outfit.items.all():
            for image in item.images.all():
                post.images.add(image)

        return redirect('subscription')
    else:
        form = CreatePostForm()

    context = {
        'form': form,
    }
    return render(request, 'subscription.html', context)



