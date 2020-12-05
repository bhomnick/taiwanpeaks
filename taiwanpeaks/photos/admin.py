from copy import deepcopy

from django import forms
from django.contrib import admin
from django.db import models

from django_object_actions import DjangoObjectActions
from sorl.thumbnail.admin import AdminImageMixin

from .models import Photo


class PhotoAdminForm(forms.ModelForm):
    add_from_flickr = forms.BooleanField(required=False, help_text="Check this box to add this photo from Flickr.")

    class Meta:
        model = Photo
        fields = '__all__'


CHANGE_FIELDSETS = (
    ('Image', {
        'fields': ['image', 'description', 'tags', 'flickr_id']
    }),
    ('Attribution', {
        'fields': ['attr_author', 'attr_title', 'attr_link', 'attr_license', 'attr_version'],
        'description': 'At a minimum provide an author or title and license. This will be filled in automatically if adding from Flickr.'
    })
)
ADD_FIELDSETS = deepcopy(CHANGE_FIELDSETS)
ADD_FIELDSETS[0][1]['fields'] += ['add_from_flickr']


@admin.register(Photo)
class PhotoAdmin(DjangoObjectActions, AdminImageMixin, admin.ModelAdmin):
    list_display = ['id', 'attr_title', 'description', 'tag_list', 'modified', 'get_preview']
    list_filter = ['tags__name']
    search_fields = ['attr_title', 'tags__name']
    change_actions = ['update_from_flickr']
    form = PhotoAdminForm
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 2})}
    }

    def get_fieldsets(self, request, obj=None):
        if obj:
            return CHANGE_FIELDSETS
        return ADD_FIELDSETS

    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get('add_from_flickr'):
            obj.update_from_flickr()
        super().save_model(request, obj, form, change)

    def get_preview(self, obj):
        return obj.thumbnail_preview
    get_preview.short_description = 'Image preview'
    get_preview.allow_tags = True

    def update_from_flickr(self, request, obj):
        obj.update_from_flickr()

    def tag_list(self, obj):
        return ', '.join([t.name for t in obj.tags.all()])
    tag_list.short_description = 'Tags'
