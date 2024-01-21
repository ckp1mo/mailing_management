from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import BlogDetailView, BlogListView


app_name = BlogConfig.name

urlpatterns = [
    path('', cache_page(60)(BlogListView.as_view()), name='list_blog'),
    path('detail/<int:pk>', BlogDetailView.as_view(), name='detail_blog'),
]
