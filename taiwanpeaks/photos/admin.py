from django import forms
from django.contrib import admin

from django_object_actions import DjangoObjectActions
from sorl.thumbnail.admin import AdminImageMixin

from .models import Photo


class PhotoAdminForm(forms.ModelForm):
    add_from_flickr = forms.BooleanField(required=False)

    class Meta:
        model = Photo
        fields = '__all__'


@admin.register(Photo)
class PhotoAdmin(DjangoObjectActions, AdminImageMixin, admin.ModelAdmin):
    list_display = ['id', 'attr_title', 'description', 'tag_list', 'modified', 'get_preview']
    list_filter = ['tags__name']
    search_fields = ['attr_title', 'tags__name']
    change_actions = ['update_from_flickr']
    form = PhotoAdminForm

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj=obj)
        if obj:
            fields.remove('add_from_flickr')
        return fields

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
