from django.contrib import admin
from .models import (
    Client,
    Salon,
    Staff,
    Service,
    Promo,
    Appointment,
    Feedback
)


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone')
    search_fields = ('name', 'phone')
    list_filter = ('name',)
    ordering = ('name',)



class SalonAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone')
    search_fields = ('name', 'address')
    list_filter = ('name',)
    ordering = ('name',)



class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'salon')
    search_fields = ('name',)
    list_filter = ('salon',)
    filter_horizontal = ('services',)  # Удобное поле для ManyToMany
    ordering = ('name',)



class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration')
    search_fields = ('name',)
    list_filter = ('price', 'duration')
    ordering = ('name',)



class PromoAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent')
    search_fields = ('code',)
    list_filter = ('discount_percent',)
    ordering = ('discount_percent',)



class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'service', 'staff', 'appointment_date', 'time')
    search_fields = ('client__name', 'service__name', 'staff__name')
    list_filter = ('appointment_date', 'staff', 'service')
    date_hierarchy = 'appointment_date'  # Иерархия по дате
    ordering = ('appointment_date', 'time')



class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('staff', 'client', 'created_at', 'preview_feedback')
    search_fields = ('staff__name', 'client__name', 'feedback')
    list_filter = ('created_at', 'staff')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)  # Поле auto_now_add=True нельзя редактировать

    def preview_feedback(self, obj):
        """Сокращённый показ отзыва (первые 50 символов)."""
        return obj.feedback[:50] + '...' if len(obj.feedback) > 50 else obj.feedback
    preview_feedback.short_description = 'Отзыв (фрагмент)'



# Регистрация моделей в админ‑панели
admin.site.register(Client, ClientAdmin)
admin.site.register(Salon, SalonAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Promo, PromoAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Feedback, FeedbackAdmin)
