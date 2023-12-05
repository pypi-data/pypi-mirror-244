import django_filters
from django import forms
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from blog.models import Blog
from dynamic_listing.filters import FilterSet


class BlogsFilter(FilterSet):
    filterset_types = {
        "q": "search",
    }
    fields_map = {
        "top_left": ['q'],
        "top_right": ['created_at'],
        "top_body": [],
        "side": []
    }
    q = django_filters.CharFilter(
        widget=forms.TextInput(attrs={
            "placeholder": _("Search Users")
        }),
        method='search', label=_("Search"))

    created_at = django_filters.DateFromToRangeFilter()

    id_range = django_filters.RangeFilter(field_name='id', label=_("ID Range"))

    class Meta:
        model = Blog
        fields = ('q', 'id_range',  'author', 'category', 'tags', 'created_at')

    def search(self, queryset, name, value):
        return queryset.filter(Q(title__icontains=value) | Q(content__icontains=value))


class BlogsFilter2(django_filters.FilterSet):
    id_range = django_filters.RangeFilter(field_name='id', label=_("ID Range"))

    class Meta:
        model = Blog
        fields = ('id_range',)
