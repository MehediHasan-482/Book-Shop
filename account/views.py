from datetime import date, timedelta
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from account.models import Subscription
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User

@login_required
def subscription_page(request):
    try:
        # Check if the user has an active subscription
        subscription = Subscription.objects.get(user=request.user)
        remaining_days = (subscription.end_date - date.today()).days
        # If subscription is active, display the details
        if subscription.end_date >= date.today():
            return render(request, 'account/subscription.html', {
                'message': f'You are subscribed to {subscription.subscription_type.capitalize()} until {subscription.end_date}.',
                'subscription_remaining_days': remaining_days
            })
    except Subscription.DoesNotExist:
        subscription = None  # No active subscription for the user

    if request.method == 'POST':
        # Handle subscription form submission
        subscription_type = request.POST.get('subscription_type')
        account_number = request.POST.get('account_number')
        
        # Check if account number is valid (must be 11 digits)
        if len(account_number) != 11:
            messages.error(request, "Account number must be exactly 11 digits.")
            return redirect('account:subscription')  # Reload the page with error

        if subscription_type in ['silver', 'gold', 'platinum']:
            # Calculate end_date based on subscription type
            if subscription_type == 'silver':
                end_date = date.today() + timedelta(days=90)
            elif subscription_type == 'gold':
                end_date = date.today() + timedelta(days=180)
            elif subscription_type == 'platinum':
                end_date = date.today() + timedelta(days=365)

            # Update or create the subscription
            Subscription.objects.update_or_create(
                user=request.user,
                defaults={
                    'subscription_type': subscription_type,
                    'end_date': end_date,
                    'account_number': account_number
                }
            )
            messages.success(request, f"Successfully subscribed to the {subscription_type.capitalize()} plan!")
            return redirect('account:subscription')

    # If no active subscription, render the subscription options
    return render(request, 'account/subscription.html', {'subscription': subscription})



@login_required
def profile(request):
    user = request.user  # The currently logged-in user
    info = User.objects.all()  # Fetches all records from the User table
    print(info)
    # Handle Profile Update (name, email, username)
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            first_name = request.POST.get('name')
            email = request.POST.get('email')
            username = request.POST.get('username')
            
            # Check if username already exists
            if user.objects.filter(username=username).exclude(id=user.id).exists():
                messages.error(request, "This username is already taken.")
                return redirect('profile')

            # Update the user profile
            user.first_name = first_name
            user.email = email
            user.username = username
            user.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('profile')  # Redirect to the profile page after update
        
        # Handle Password Change
        elif 'change_password' in request.POST:
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            # Check if new passwords match
            if new_password != confirm_password:
                messages.error(request, "New passwords do not match.")
            else:
                if user.check_password(current_password):
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user)  # Keep the user logged in after password change
                    messages.success(request, "Your password was changed successfully.")
                    return redirect('account:profile')
                else:
                    messages.error(request, "Incorrect current password.")
    
    return render(request, 'account/profile.html',{'user': user})