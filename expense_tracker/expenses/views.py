from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Income,ExpenseCategory,ExpenseDetails,ExpenseSummary
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest
from django.http import JsonResponse
from datetime import datetime,timedelta
from decimal import Decimal
from django.contrib.auth.hashers import make_password
from datetime import datetime
import json

from itertools import zip_longest


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists() :
           return render(request, 'signup.html', {'error_message': 'Username '})

        new_user = User.objects.create(username=username, email=email)
        hashed_password = make_password(password)

        new_user.password = hashed_password
        new_user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        
        

        return redirect('income')  # Redirect to the desired page after signup (e.g., home page)

    return render(request, 'signup.html')

def user_login(request):
    if request.method == 'POST':
        print("Request method is POST") 
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user with the provided username and password
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # If authentication is successful, log in the user
            login(request, user)
            return redirect('home')  
        else:
            # If authentication fails, render the login page again with an error message
            return render(request, 'login.html', {'error_message': 'Invalid username or password\n try again'})
    
    # If the request method is not POST, render the login page
    return render(request, 'login.html')




@login_required
def income(request):
    if request.method == 'POST':
        income_amount = request.POST.get('income')  # Corrected to 'income'
        if income_amount:
            new_income = Income(amount=income_amount, user=request.user)
            new_income.save() 

        return redirect('cat')  
    else:
        return render(request, 'income.html')


@login_required
def cat(request):
    categories = ExpenseCategory.objects.filter(user=request.user).values_list('category', flat=True).distinct() 
    user_income = Income.objects.get(user=request.user)
    savings_fixed_expense = user_income.amount * Decimal('0.2')
    if not ExpenseCategory.objects.filter(user=request.user, category='savings').exists():
        ExpenseCategory.objects.create(user=request.user, category='savings', fixed_expense=savings_fixed_expense)
    if not ExpenseCategory.objects.filter(user=request.user, category='miscellaneous').exists():
        ExpenseCategory.objects.create(user=request.user, category='miscellaneous',fixed_expense=0)
    if request.method == 'POST':
        category_name = request.POST.get('new-expense-category')
        fixed_expense = request.POST.get('fixed-expense')  


        if fixed_expense and fixed_expense.isdigit():fixed_expense = int(fixed_expense)
        else:fixed_expense = 0  
        ExpenseCategory.objects.create(
            user=request.user,
            category=category_name,
            fixed_expense=fixed_expense
        )
        
        return redirect('cat')  # Redirect to the same page after saving the category

      # Fetch categories for the current user
    return render(request, 'cat.html', {'categories': categories})


def home(request):
    return render(request, 'home.html')


def expense(request):
    categories = ExpenseCategory.objects.filter(user=request.user).values_list('category', flat=True).distinct()
    categories_with_zero_expense = ExpenseCategory.objects.filter(user=request.user, fixed_expense=0).values_list('category', flat=True).distinct()
    month_year_date = datetime.now().date()
    month_year_date = month_year_date.replace(day=1)
    expenses = ExpenseDetails.objects.filter(user=request.user, month_year=month_year_date).exclude(category='remaining')
    total_expense_amount = sum(expense.cat_expense for expense in expenses.exclude(category__in=['remaining', 'savings']))
    remaining_category = ExpenseDetails.objects.filter(user=request.user, category='remaining', month_year=month_year_date).first()
    
    if remaining_category is None :
        
        try:
            user_income = Income.objects.get(user=request.user).amount
        except Income.DoesNotExist:
            user_income = 0

        fixed_expenses_sum = ExpenseCategory.objects.filter(user=request.user).aggregate(Sum('fixed_expense'))['fixed_expense__sum'] or 0
        remaining_fixed_expense = user_income - fixed_expenses_sum
        # Create a new ExpenseCategory object for remaining expenses
        ExpenseCategory.objects.create(user=request.user, category='remaining', fixed_expense=remaining_fixed_expense)

    
    if request.method == 'POST' and request.POST.get('action') == 'Add':
        # Function to handle form submission

        print("inside the add")
        def handle_form_submission():
            month_year = request.POST.get('month_year')
            if not month_year:
                return HttpResponseBadRequest("Month and year are required.")

            try:
                submitted_date = datetime.strptime(month_year, '%Y-%m-%d').date()
                month_year_date = submitted_date.replace(day=1)
                
            except ValueError:
                return HttpResponseBadRequest("Invalid month and year format.")

            
            # for ExpenseSummary
            expenseso = ExpenseDetails.objects.filter(user=request.user, month_year=month_year_date).exclude(category__in=['remaining', 'savings'])
            summary = ExpenseSummary.objects.filter(user=request.user, month_year=month_year_date).first()
            if summary is None:
                total_expense_amount = sum(expense.cat_expense for expense in expenseso.exclude(category__in=['remaining', 'savings']))
                ExpenseSummary.objects.create(user=request.user,  month_year=month_year_date, total=total_expense_amount)
            else:
                summary.total=sum(expense.cat_expense for expense in expenseso.exclude(category__in=['remaining', 'savings']))
            expense_summary = ExpenseSummary.objects.filter(user=request.user, month_year=month_year_date, status=1).first()
            if expense_summary:
                print("statuss is one")
                message = 'The given month expense editing is closed so enter the month to get report  '
                return render(request, 'chart.html', {'message': message})
            
            amount = request.POST.get('amount')
            category = request.POST.get('category')
            if not (amount and category):
                return HttpResponseBadRequest("Amount and category are required.")

            amount = Decimal(amount)

            # Get ExpenseDetails objects for the specified category and month/year
            expense_details = ExpenseDetails.objects.filter(user=request.user, category=category, month_year=month_year_date)
            
            
            expenses = ExpenseDetails.objects.filter(user=request.user, month_year=month_year_date).exclude(category='remaining')
            
            if not expense_details.exists():
                for categorye in categories:
                    fixed_expense_value = ExpenseCategory.objects.filter(user=request.user, category=categorye).values_list('fixed_expense', flat=True).first()
                    ExpenseDetails.objects.create( user=request.user, category=categorye, month_year=month_year_date, cat_expense=fixed_expense_value if fixed_expense_value is not None else 0)
            expense_details = ExpenseDetails.objects.filter(user=request.user, category=category, month_year=month_year_date)
            expense_detail = expense_details.first()  
            expense_detail.cat_expense += amount
            expense_detail.save()
               


            try:
                remaining_category = ExpenseDetails.objects.filter(user=request.user, category='remaining', month_year=month_year_date).first()
                remaining_category.cat_expense -= amount
                remaining_category.save()
            except ExpenseDetails.DoesNotExist:
                print("The 'remaining' category does not exist.")

            total_expense_amount = sum(expense.cat_expense for expense in expenses.exclude(category__in=['remaining', 'savings']))
            return render(request, 'expense.html', {'expenses': expenses,'month_year_date':month_year_date,'categories_with_zero_expense': categories_with_zero_expense,  'total_expense_amount': total_expense_amount, 'remaining_category':remaining_category})

        
        return handle_form_submission()

    elif request.method == 'POST' and request.POST.get('action') == 'close':
        
        print("inside the close")
        month_year = request.POST.get('month_year')
        print(month_year)
        if not month_year:
            return HttpResponseBadRequest("Month and year are requiredf.")
        submitted_date = datetime.strptime(month_year, '%Y-%m-%d').date()
        month_year_date = submitted_date.replace(day=1)
        expense_summary = ExpenseSummary.objects.filter(user=request.user, month_year=month_year_date).first()
        if expense_summary:
            expense_summary.status = 1  # Assuming '1' represents closed status
            expense_summary.save()
          
        
        # Retrieve remaining amount from ExpenseDetails for the given user and month
        remaining_expense = ExpenseDetails.objects.filter(user=request.user, month_year=month_year_date, category='remaining').first()
        if remaining_expense:
            remaining_amount = remaining_expense.cat_expense
            if remaining_amount > 0:
                # Retrieve Income object for the current user
                try:
                    income = Income.objects.get(user=request.user)
                    half_remaining_amount = remaining_amount / 2
                    # Add one half to savings
                    save_expense = ExpenseDetails.objects.filter(user=request.user, month_year=month_year_date, category='savings').first()
                    save_expense.cat_expense += half_remaining_amount
                    save_expense.save()
                    # Add the other half to emergency
                    income.emergency += half_remaining_amount
                    income.save()
                    remaining_expense.cat_expense=0
                    remaining_expense.save()
                    
                except Income.DoesNotExist:
                    # Handle the case where the Income object does not exist
                    pass
            return redirect(reverse('expense'))  # Redirect to chart page upon successful closure
        else:
            return HttpResponseBadRequest("Expense summary not found for the given month and year.")



    return render(request, 'expense.html', {'expenses': expenses,'month_year_date':month_year_date,'categories_with_zero_expense': categories_with_zero_expense,  'total_expense_amount': total_expense_amount, 'remaining_category':remaining_category})


    

def divider(request):
    return render(request, 'divider.html')



from itertools import zip_longest

from decimal import Decimal

def bar(request):
    current_date = datetime.now().date().replace(day=1)
    months = []
    data = []

    for i in range(1, 6):  # Fetch data for the past 5 months
        month = current_date - timedelta(days=30*i)
        expense_data = ExpenseSummary.objects.filter(user=request.user, month_year__year=month.year, month_year__month=month.month).first()

        months.append(month.strftime('%B %Y'))
        total = expense_data.total if expense_data else Decimal('0')  # Ensure total is Decimal
        data.append(str(total))  # Convert Decimal to string
    
    # Zip the lists
    zipped_data = list(zip(months[::-1], data[::-1]))  # Reverse data list before zipping
    print(zipped_data)
    zipped_data_json = json.dumps(zipped_data)
    
    return render(request, 'bar.html', {'zipped_data_json': zipped_data_json})


import logging

def chart(request):
    if request.method == 'POST':
        selected_date_str = request.POST.get('date')
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d')
        given_date = selected_date.replace(day=1)
        logging.debug(f"Selected date: {selected_date}")  # Add this line for debugging
        try:
            expenses = ExpenseDetails.objects.filter(user=request.user,  month_year=given_date)
            if expenses.exists():
                categories = expenses.values_list('category', flat=True).distinct()
                expense_amounts = [expenses.filter(category=category).aggregate(total=Sum('cat_expense'))['total'] or 0 for category in categories]
                data = list(zip_longest(categories, expense_amounts, fillvalue=''))
                return render(request, 'chart.html', {'data': data})
            else:
                message = f"The data for {selected_date.strftime('%B %Y')} doesn't exist."
                return render(request, 'chart.html', {'message': message})
        except Exception as e:
            print("except")
            return render(request, 'chart.html', {'error_message': str(e)})
                
    return render(request, 'chart.html')



def header(request):
    return render(request, 'header.html')

def tourm(request):
    return render(request, 'tourm.html')