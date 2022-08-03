from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    autocomplete_fields = ('genre',)


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    autocomplete_fields = ('person',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    search_fields = ('name', 'description', 'id',)


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline,)
    list_display = (
        'title',
        'type',
        'creation_date',
        'rating',
        'get_genres'
    )
    list_filter = ('type',)
    search_fields = ('title', 'description', 'id')
    list_prefetch_related = ('genres','persons')

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(
            *self.list_prefetch_related
        )

    @admin.display(description=_('genre'))
    def get_genres(self, obj):
        return ','.join([genre.name for genre in obj.genres.all()])


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ('full_name', 'id', )
