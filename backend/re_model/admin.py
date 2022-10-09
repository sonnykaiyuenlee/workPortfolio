from django.contrib import admin

from .components.sources import (
    get_monthly_payment,
    get_debt_schedule,
    combine_debt_schedules
    )

from .models import (
    Portfolio,
    Project,
    Assumption,
    Loan,
    Unit,
    UseLineItem,
    ExpenseLineItem
    )

# Register your models here.
@admin.register(Portfolio)
class PortfolioModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_projects')

    @admin.display(description="Projects")
    def get_projects(self, obj):
        return len(Project.objects.filter(portfolio=obj.id))

@admin.register(Project)
class ProjectModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'portfolio', 'combine_debt_schedules')

    @admin.display(description="Annual Debt Service")
    def combine_debt_schedules(self, obj):
        annual_debt_service = combine_debt_schedules(obj.id)
        return f"${round(annual_debt_service,0)}"

@admin.register(Assumption)
class AssumptionModelAdmin(admin.ModelAdmin):
    list_display = ('project', 'vacancy_rate', 'income_trend', 'expense_trend')

@admin.register(Loan)
class LoanModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'payment', 'debt_schedule')

    @admin.display(description="Monthly Payment")
    def payment(self, obj):
        pmt = get_monthly_payment(obj.id)
        return f'${round(pmt,0)}'

    @admin.display(description="Debt Schedule Shape")
    def debt_schedule(self, obj):
        ds = get_debt_schedule(obj.id)
        return ds.shape

@admin.register(Unit)
class UnitModelAdmin(admin.ModelAdmin):
    list_display = ('project', 'count', 'rent', 'beds', 'baths', 'sqft', 'description')

@admin.register(UseLineItem)
class UseLineItemModelAdmin(admin.ModelAdmin):
    list_display = ('project', 'name', 'amount', 'tax_treatment')

@admin.register(ExpenseLineItem)
class ExpenseLineItemModelAdmin(admin.ModelAdmin):
    list_display = ('project', 'name', 'amount')
