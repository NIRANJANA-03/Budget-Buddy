from django.contrib import admin
from .models import *

admin.site.register(Income)
admin.site.register(ExpenseCategory)
admin.site.register(ExpenseDetails)
admin.site.register(ExpenseSummary)
admin.site.register(TDetails)
admin.site.register(Tcat)
admin.site.register(DEvent)
admin.site.register(CatEvent)