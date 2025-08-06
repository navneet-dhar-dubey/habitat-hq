from django.contrib import admin
from .models import Society, User, Unit, Notice, Complaint
# Register your models here.

admin.site.register(Society)
admin.site.register(User)
admin.site.register(Unit)

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    # We are testing with ONLY these two settings.
    exclude = ('author',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)
        

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    """Admin configuration for the Complaint model."""
    list_display = ('title', 'raised_by', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'raised_by__society')
    search_fields = ('title', 'description', 'raised_by__email')
    list_editable = ('status',)
    date_hierarchy = 'created_at'

    readonly_fields = ('raised_by', 'created_at', 'updated_at')