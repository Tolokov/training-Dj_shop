from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Shop import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('blog/', views.BlogView.as_view(), name='blog'),
    path('<int:post_id>/', views.SinglePostVies.as_view(), name='single_post'),
    # path('blog/<int:post_id>/', views.SinglePostVies.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


