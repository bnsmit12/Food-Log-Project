from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import FoodEntry
from datetime import datetime
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .forms import FoodEntryForm, EmailVerificationForm, PasswordResetForm, ResetPasswordForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
import random
from utils.email_utils import send_verification_code, send_password_reset_code
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email is already registered.')
        return email

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.is_active = False
                user.save()

                verification_code = str(random.randint(1000, 9999))
                send_verification_code(user.email, verification_code)

                request.session['verification_code'] = verification_code
                request.session['user_id'] = user.id

                return render(request, 'registration/verify_code.html', {'form': EmailVerificationForm()})

            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
                return render(request, 'registration/signup.html', {'form': form})

    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})

def verify_code(request):
    if request.method == 'POST':
        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            input_code = form.cleaned_data['verification_code']
            stored_code = request.session.get('verification_code')
            print(f"Entered Code: {input_code}, Stored Code: {stored_code}")
            if input_code == stored_code:
                user_id = request.session.get('user_id')
                if user_id:
                    try:
                        user = get_user_model().objects.get(pk=user_id)
                        print(f"User fetched: {user.username}, Active: {user.is_active}")
                        user.is_active = True
                        user.save()
                        print(f"User after activation: {user.username}, Active: {user.is_active}")
                        del request.session['verification_code']
                        del request.session['user_id']
                        messages.success(request, 'Your email has been verified successfully.')
                        return redirect('login')
                    except get_user_model().DoesNotExist:
                        messages.error(request, 'User does not exist.')
                        return redirect('signup')
                else:
                    messages.error(request, 'Invalid session data.')
                    return redirect('signup')
            else:
                messages.error(request, 'Invalid verification code.')
    else:
        print("GET request received")
        form = EmailVerificationForm()

    return render(request, 'registration/verify_code.html', {'form': form})

def request_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)

            reset_code = str(random.randint(1000, 9999))
            send_password_reset_code(email, reset_code)

            request.session['password_reset_code'] = reset_code
            request.session['reset_email'] = email

            return redirect('verify_reset_code')
        except User.DoesNotExist:
            messages.error(request, 'No user found with this email address.')
            return redirect('request-reset')

    return render(request, 'registration/request_reset.html')


def reset_password(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password has been reset successfully.')
            return redirect('login')
    else:
        form = ResetPasswordForm(user=request.user)

    return render(request, 'registration/reset_password.html', {'form': form})

def verify_reset_code(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            input_code = form.cleaned_data['verification_code']

            stored_code = request.session.get('password_reset_code')
            stored_email = request.session.get('reset_email')

            if input_code == stored_code:
                user = User.objects.get(email=stored_email)
                user.set_password(form.cleaned_data['new_password'])
                user.save()

                del request.session['password_reset_code']
                del request.session['reset_email']

                messages.success(request, 'Your password has been reset successfully!')
                return redirect('login')
            else:
                messages.error(request, 'Invalid verification code. Please try again.')

    else:
        form = PasswordResetForm()

    return render(request, 'registration/password_verify.html', {'form': form})

@login_required
def redirect_to_calendar(request):
    return redirect('calendar')

@login_required
def calendar_view(request):
    food_entries = FoodEntry.objects.all()
    form = FoodEntryForm()

    context = {
        'food_entries': food_entries,
        'form': form,
    }
    return render(request, 'food_log/calendar.html', context)

@login_required
@require_POST
@csrf_exempt
def add_food_entry(request):
    date = request.POST.get('date')
    meal_type = request.POST.get('meal_type')
    food_item = request.POST.get('food_item')
    calories = request.POST.get('calories')
    notes = request.POST.get('notes', '')

    FoodEntry.objects.create(
        user=request.user,
        date=datetime.strptime(date, '%Y-%m-%d').date(),
        meal_type=meal_type,
        food_item=food_item,
        calories=calories,
        notes=notes
    )
    return redirect('calendar')


@login_required
def get_food_entries(request):
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')

    entries = FoodEntry.objects.filter(
        user=request.user,
        date__range=[start_date, end_date]
    )

    data = [{
        'id': entry.id,
        'date': entry.date.isoformat(),
        'meal_type': entry.meal_type,
        'food_item': entry.food_item,
        'calories': entry.calories
    } for entry in entries]

    return JsonResponse(data, safe=False)

@login_required
def get_food_entries_by_date(request):
    date = request.GET.get('date')
    entries = FoodEntry.objects.filter(user=request.user, date=date)

    data = [{
        'id': entry.id,
        'meal_type': entry.meal_type,
        'food_item': entry.food_item,
        'calories': entry.calories
    } for entry in entries]

    return JsonResponse(data, safe=False)

def new_food_entry(request):
    if request.method == 'POST':
        form = FoodEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('calendar')
    else:
        form = FoodEntryForm()
    return render(request, 'food_log/new_entry.html', {'form': form})


def view_entries(request):
    selected_date = request.GET.get('date')
    entries = FoodEntry.objects.filter(date=selected_date, user=request.user)
    total_calories = entries.aggregate(Sum('calories'))['calories__sum'] or 0

    return render(request, 'food_log/entry_list.html', {
        'entries': entries,
        'selected_date': selected_date,
        'total_calories': total_calories
    })

@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(FoodEntry, id=entry_id, user=request.user)
    entry.delete()
    messages.success(request, 'Entry deleted successfully.')
    return redirect('calendar')
