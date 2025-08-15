# insurance/admin.py

from django.contrib import admin
from .models import InsuranceBenefit, InsurancePlan, InsuranceFAQ, TrustSeal
from adminsortable2.admin import SortableAdminMixin

@admin.register(InsuranceBenefit)
class InsuranceBenefitAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title',)
    # Adicionando o novo campo ao formulário
    fields = ('title', 'description', 'long_description', 'icon_class')

@admin.register(InsurancePlan)
class InsurancePlanAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'price_info', 'is_popular')

@admin.register(InsuranceFAQ)
class InsuranceFAQAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('question',)

@admin.register(TrustSeal)
class TrustSealAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('name',)