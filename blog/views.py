from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from blog.models import Blog


class BlogListView(LoginRequiredMixin, ListView):
    model = Blog


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog

    def get_object(self, queryset=None):
        queryset = super().get_object(queryset)
        queryset.view += 1
        queryset.save()
        return queryset

