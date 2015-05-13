from django.contrib import admin

from .models import HtmlHeaderFooter, HtmlBody, Html
from .forms import HtmlForm


class HtmlHeaderFooterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )


class HtmlBodyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )


class HtmlAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'view', 'attachment')
    form = HtmlForm


admin.site.register(HtmlHeaderFooter, HtmlHeaderFooterAdmin)
admin.site.register(HtmlBody, HtmlBodyAdmin)
admin.site.register(Html, HtmlAdmin)
