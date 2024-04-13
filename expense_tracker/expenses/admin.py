from django.contrib import admin
from .models import *

admin.site.register(Income)
admin.site.register(ExpenseCategory)
admin.site.register(ExpenseDetails)
admin.site.register(ExpenseSummary)
