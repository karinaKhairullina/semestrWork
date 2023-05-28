from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('add_clothes/', views.add_clothing_item, name='add_clothes'),
    path('all_clothes/', views.all_clothes, name='all_clothes'),
    path('edit_clothing_item/<int:id>/', views.edit_clothing_item, name='edit_clothing_item'),
    path('allOutfits/', views.outfits, name='outfits'),
    path('createOutfit/', views.create_outfit, name='create_outfit'),
    path('create-post/', views.create_post, name='create_post'),
    path('clothing_item/delete/<int:id>/', views.delete_clothing_item, name='delete_clothing_item'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



