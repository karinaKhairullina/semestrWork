from django.contrib import admin
from django.urls import path, include
from .views import home_view, QA_view, termsUse_view,subscribe
from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("authorization.urls")),
    path("", include("myClothes.urls")),
    path("", include("fashionShows.urls")),
    path("", include("subscribe.urls")),
    path("home/", home_view, name="home"),
    path('Q&A/', QA_view, name="Q&A"),
    path('termsUse/', termsUse_view, name="termsUse"),
    path('subscribe/<int:user_id>/', subscribe, name='subscribe'),
    path('', include('social_django.urls', namespace='social')),
]

urlpatterns += doc_urls
