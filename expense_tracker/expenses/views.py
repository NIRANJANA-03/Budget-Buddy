from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Income,ExpenseCategory,ExpenseDetails,ExpenseSummary,TDetails,DEvent,CatEvent
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


def forgot(request):
    return render(request, 'forgot.html')


@login_required
def income(request):
    if request.method == 'POST':
        income_amount = request.POST.get('income')
        profession = request.POST.get('profession')  # Retrieve the profession from the form data
        
        if income_amount:  # Ensure income amount is provided
            # Create a new Income object with income amount, user, and profession
            new_income = Income(amount=income_amount, user=request.user, profession=profession)
            new_income.save()  # Save the new income object to the database

        return redirect('cat')  # Redirect to a relevant URL after saving the income
    else:
        return render(request, 'income.html')

@login_required
def profile(request):
    
    user_incomes = Income.objects.filter(user=request.user)
    if request.method == 'POST':
        debit_amount = request.POST.get('debit_amount')
        user_income = Income.objects.get(user=request.user)
       
        debit_amount = Decimal(debit_amount)
        print(debit_amount)
        if debit_amount >= user_income.emergency:
            debit_amount=user_income.emergency-debit_amount

            if debit_amount > user_income.savings:
                return render(request, 'profle.html', {'error_message': 'Debit amount exceeds the emergency fund.'})
            else:
                user_income.emergency=0
                user_income.savings-=debit_amount
                user_income.save()
        else:
            user_income.emergency-=debit_amount
            user_income.save()
                
        
        # Redirect to a success page or any other appropriate page
        return redirect('profile')
    return render(request, 'profile.html', {'user_incomes': user_incomes,})


@login_required
def cat(request):
    categories = ExpenseCategory.objects.filter(user=request.user).values_list('category', flat=True).distinct() 
    
    #taking income and adding 20%to svings 
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
    # Fetch the income for the current user
    incomes = Income.objects.get(user=request.user)
    total_savings_expenses = ExpenseDetails.objects.filter(user=request.user, category='savings').aggregate(total_savings_expenses=Sum('cat_expense'))['total_savings_expenses'] or 0
    incomes.savings = total_savings_expenses
    incomes.save()
    
    return render(request, 'home.html', {'incomes': incomes, 'total_savings_expenses': total_savings_expenses})


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
            # converting month in to suitable form 
            try:
                submitted_date = datetime.strptime(month_year, '%Y-%m-%d').date()
                month_year_date = submitted_date.replace(day=1)
                
            except ValueError:
                return HttpResponseBadRequest("Invalid month and year format.")


            # Query ExpenseDetails once to get expenses for the current user and month, excluding categories 'remaining' and 'savings'
            expenseso = ExpenseDetails.objects.filter(user=request.user, month_year=month_year_date)


            
            #if the status is one t is closed 
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
               

            # Query ExpenseDetails once to get expenses for the current user and month, excluding categories 'remaining' and 'savings'
            expenseso = ExpenseDetails.objects.filter(user=request.user, month_year=month_year_date).exclude(category__in=['remaining', 'savings'])

            total_expense_amount = total_expense_amount = sum(expense.cat_expense for expense in expenseso)
            summary = ExpenseSummary.objects.filter(user=request.user, month_year=month_year_date).first()
            if summary is None:
                ExpenseSummary.objects.create(user=request.user, month_year=month_year_date, total=total_expense_amount)
            else:
                summary.total = total_expense_amount
                summary.save()            
            print(summary)
            #remaining calculation 
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


from django.shortcuts import render

def chart(request):
    if request.method == 'POST':
        selected_date_str = None
        selected_date_str = request.POST.get('date')
        request.session['selected_date_str'] = selected_date_str  # Store the selected date in session
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d')
        given_date = selected_date.replace(day=1)
        logging.debug(f"Selected date: {selected_date}")  # Add this line for debugging
        try:
            expenses = ExpenseDetails.objects.filter(user=request.user,  month_year=given_date)
            if expenses.exists():
                categories = expenses.values_list('category', flat=True).distinct()
                expense_amounts = [expenses.filter(category=category).aggregate(total=Sum('cat_expense'))['total'] or 0 for category in categories]
                data = list(zip_longest(categories, expense_amounts, fillvalue=''))
                return render(request, 'chart.html', {'data': data, 'selected_date_str': selected_date_str})
            else:
                message = f"The data for {selected_date.strftime('%B %Y')} doesn't exist."
                return render(request, 'chart.html', {'message': message})
        except Exception as e:
            print("except")
            return render(request, 'chart.html', {'error_message': str(e)})
                
    return render(request, 'chart.html')





def header(request):
    return render(request, 'header.html')



from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
class DownloadPDF(View):
    def get(self, request):
        # Retrieve selected date from session
        pdf_export: True
        selected_date_str = request.session.get('selected_date_str', None)

        if selected_date_str is None:
            return HttpResponse('Date parameter is missing.')

        try:
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d')
        except ValueError:
            return HttpResponse('Invalid date format.')

        formatted_date_str = selected_date.strftime('%B %Y')
        given_date = selected_date.replace(day=1)
        expenses = ExpenseDetails.objects.filter(user=request.user, month_year=given_date)
        categories = expenses.values_list('category', flat=True).distinct()
        expense_amounts = [expenses.filter(category=category).aggregate(total=Sum('cat_expense'))['total'] or 0 for category in categories]
        data = list(zip_longest(categories, expense_amounts, fillvalue=''))

        # Pass data to the HTML template
        context = {'data': data,'pdf_export': True}

        # Render HTML template
        template = get_template('chart.html')
        html = template.render(context)

        # Create PDF
        response = HttpResponse(content_type='application/pdf')

        # Dynamically set the filename with the selected date
        filename = f"expense_report of {formatted_date_str}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        # Generate PDF from HTML content
        pisa_status = pisa.CreatePDF(html, dest=response)
        
        if pisa_status.err:
            return HttpResponse('Failed to generate PDF')

        return response
@login_required
def hometour(request):
    # Retrieve the TDetails of the current user
    tour_details = TDetails.objects.filter(user=request.user)

    # Pass the tour details to the template context
    return render(request, 'hometour.html', {'tour_details': tour_details})

def addtour(request):
    if request.method == 'POST':
        tour_name = request.POST.get('tour_name')
        budget = request.POST.get('budget')
        duration = request.POST.get('duration')
        remaining=budget
        request.session['tour_name'] = tour_name
        if tour_name and budget and duration:
            if TDetails.objects.filter(tour_name=tour_name).exists():
                messages.error(request, 'Tour name already exists. Please choose a different name.')
            else:
                user = request.user
                TDetails.objects.create(tour_name=tour_name, budget=budget, duration=duration, user=user,remaining=remaining)
                return redirect('cattour') 
    return render(request, 'addtour.html')

from .models import Tcat

def cattour(request):
    if request.method == 'POST':
        new_category = request.POST.get('category')
        if new_category:
            tour_name = request.session.get('tour_name')
            Tcat.objects.create(category=new_category, tour_name=tour_name)
    
    # Get all categories for the current tour
    tour_name = request.session.get('tour_name')
    categories = Tcat.objects.filter(tour_name=tour_name)
    
    return render(request, 'cattour.html', {'categories': categories})

from django.contrib import messages

def maintour(request, tour_name):
    try:
        tour_details = TDetails.objects.get(tour_name=tour_name)
        tcat_details = Tcat.objects.filter(tour_name=tour_name)
    except TDetails.DoesNotExist:
        tour_details = None
        tcat_details = None

    if request.method == 'POST':
        category = request.POST.get('category')
        expense = Decimal(request.POST.get('expense'))

        # Update TDetails remaining budget
        if tour_details:
            tour_details.remaining -= expense
            tour_details.save()

            # Check if remaining budget is zero or negative
            if tour_details.remaining <= 0:
                messages.warning(request, 'Expense is over budget amount. Spend accordingly.')

            # Check if Tcat entry exists for the category and tour name
            tcat_entry = Tcat.objects.filter(tour_name=tour_name, category=category).first()
            if tcat_entry:
                tcat_entry.expense += expense
                tcat_entry.save()
            else:
                # If the Tcat entry doesn't exist, create a new one
                Tcat.objects.create(tour_name=tour_name, category=category, expense=expense)

        # Re-fetch the updated data after processing the form submission
        try:
            tour_details = TDetails.objects.get(tour_name=tour_name)
            tcat_details = Tcat.objects.filter(tour_name=tour_name)
        except TDetails.DoesNotExist:
            tour_details = None
            tcat_details = None

        return render(request, 'maintour.html', {'tour_details': tour_details, 'tcat_details': tcat_details})

    return render(request, 'maintour.html', {'tour_details': tour_details, 'tcat_details': tcat_details})



def update_status(request, tour_name):
    if request.method == 'POST':
        # Update status in TDetails model for a specific tour_name
        if tour_name:
            try:
                tour = TDetails.objects.get(tour_name=tour_name)
                tour.status = 1  
                tour.save()
            except TDetails.DoesNotExist:
                pass  

    return redirect('hometour') 




    

def eventhome(request):
    # Retrieve the TDetails of the current user
    event_details = DEvent.objects.filter(user=request.user)
    print(event_details)
    return render(request, 'eventhome.html', {'event_details': event_details})
  




def eventadd(request):
    if request.method == 'POST':
        event_name = request.POST.get('event_name')
        event_location = request.POST.get('event_location')
        num_persons = int(request.POST.get('num_persons'))
        president_name = request.POST.get('president_name')
        president_email = request.POST.get('president_email')
        program_secretary_name = request.POST.get('program_secretary_name')
        program_secretary_email = request.POST.get('program_secretary_email')
        amount_collected = float(request.POST.get('amount_collected'))  

        request.session['event_name'] = event_name
        user = request.user

        # Calculate the total amount collected
        total_collected = amount_collected * num_persons

        # Create the event object
        event = DEvent.objects.create(
            user=user,
            event_name=event_name,
            event_location=event_location,
            num_persons=num_persons,
            president_name=president_name,
            president_email=president_email,
            program_secretary_name=program_secretary_name,
            program_secretary_email=program_secretary_email,
            collected=total_collected  # Assign the total collected amount
        )
        event.save()
        return redirect('eventcat')  # Redirect to success page

    return render(request, 'eventadd.html')


def eventcat(request):
    categories = []  # Initialize categories with an empty list
    
    if request.method == 'POST':
        new_category = request.POST.get('category')
        if new_category:
            # Assuming you have a session variable for the current event name
            event_name = request.session.get('event_name')
            CatEvent.objects.create(category=new_category, event_name=event_name)
            return redirect('eventcat')
    
    # Get categories for the current event
    event_name = request.session.get('event_name')
    categories = CatEvent.objects.filter(event_name=event_name)
    
    return render(request, 'eventcat.html', {'categories': categories, 'event_name': event_name})
    

    
from django.core.exceptions import ObjectDoesNotExist
def divider(request, event_name):
    try:
        event_details = DEvent.objects.get(event_name=event_name)
        cat_details = CatEvent.objects.filter(event_name=event_name)
    except ObjectDoesNotExist:
        event_details = None
        cat_details = None

    if request.method == 'POST':
        category = request.POST.get('category')
        amount = request.POST.get('amount')
        try:
            expense = Decimal(amount)
        except Decimal.InvalidOperation:
            messages.error(request, 'Invalid expense amount.')
            return redirect('divider', event_name=event_name)

        if event_details:
            event_details.total += expense
            event_details.save()

            if event_details.total >= event_details.collected:
                messages.warning(request, 'Expense is over budget amount. Spend accordingly.')

            cat_entry = CatEvent.objects.filter(event_name=event_name, category=category).first()
            if cat_entry:
                cat_entry.expense += expense
                cat_entry.save()
            else:
                CatEvent.objects.create(event_name=event_name, category=category, expense=expense)

        return redirect('divider', event_name=event_name)

    return render(request, 'divider.html', {'event_details': event_details, 'cat_details': cat_details})

def close_event(request, event_name):
    if request.method == 'POST':
        try:
            event = DEvent.objects.get(event_name=event_name)
            event.status = 1
            event.save()
        except DEvent.DoesNotExist:
            pass  
    return redirect('eventhome')  

from django.core.mail import send_mail
from django.http import HttpResponse

def send_report(request, event_name):
    if request.method == 'POST':
        try:
            event = DEvent.objects.get(event_name=event_name)
            cat_events = CatEvent.objects.filter(event_name=event_name)
            # Extract email addresses of president and program secretary
            president_email = event.president_email
            secretary_email = event.program_secretary_email
            
            email_message = ""
            for field in event._meta.fields:
                email_message += f"{field.verbose_name.capitalize()}: {getattr(event, field.name)}\n"
            email_message += "\n"
            

            email_message += "\nCategory Details:\n"
            for cat_event in cat_events:
                email_message += f"Category: {cat_event.category} with expense of {cat_event.expense} rupees\n"
            
            print(email_message)
            send_mail(
                'Event Report',
                email_message,
                'niranjanasunil2435@gmail.com',  
                [president_email, secretary_email],  
                fail_silently=False,
            )
           
            messages.warning(request, 'Report send to given emails.')
            return redirect('divider',event_name=event_name)  
        except DEvent.DoesNotExist:
            return HttpResponse('Event not found', status=404)
    
    # Return HTTP 405 (Method Not Allowed) if the request method is not POST
    return HttpResponse('Method not allowed', status=405)