from django.contrib import admin
from bookmarks.models import Bookmark, Link

class BookmarkInline(admin.TabularInline):
    model = Bookmark
    extra = 3

class BookmarkAdmin(admin.ModelAdmin):
#    fieldsets = [
#        (None,               {'fields': ['question']}),
#        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
#    ]
#    inlines = [ChoiceInline]
#    list_display = ('question', 'pub_date', 'was_published_recently')
#    list_filter = ['pub_date']
#    search_fields = ['question']
#    date_hierarchy = 'pub_date'
    pass

class LinkAdmin(admin.ModelAdmin):
    inlines = [BookmarkInline]


admin.site.register(Bookmark, BookmarkAdmin)
admin.site.register(Link    , LinkAdmin )