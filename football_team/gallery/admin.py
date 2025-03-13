from gallery.models import Image, Album
from django.contrib import admin
from imagekit.admin import AdminThumbnail
# Support adminsortable2 optionally
import importlib
if importlib.util.find_spec('adminsortable2', 'admin'):
    from adminsortable2.admin import SortableAdminMixin
else:
    # Mock up class for mixin
    class SortableAdminMixin:
        mock = True


class ImageAdmin(admin.ModelAdmin):
    admin_thumbnail = AdminThumbnail(image_field='data_thumbnail', template='gallery/admin/thumbnail.html')
    list_display = ('title', 'admin_thumbnail', 'date_taken', 'date_uploaded')
    list_filter = ('image_albums',)
    list_per_page = 25
    readonly_fields = ('admin_thumbnail',)
    ordering = ('date_uploaded', )


class AlbumAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('order', 'title')
    list_display_links = ('title',)
    if hasattr(SortableAdminMixin, 'mock'):
        list_editable = ('order',)
        list_display = ('title', 'order')
    filter_horizontal = ('images',)
    raw_id_fields = ('highlight',)

    def delete_queryset(self, request, queryset):
        # Удаляем файлы для каждой записи
        for obj in queryset:
            obj.delete()
        # Вызываем родительский метод для завершения удаления
        super().delete_queryset(request, queryset)


admin.site.register(Image, ImageAdmin)
admin.site.register(Album, AlbumAdmin)


