from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm, UserProfileFormWithPic
from django.contrib import messages
from .models import UserProfile

@login_required
def update_profile(request):
    try:
        user_profile = request.user.profile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')  # Redirect to the profile view (you need to define this URL)
        else:
            messages.error(request, 'There was an error updating your profile. Please correct the form.')
    else:
        form = UserProfileForm(instance=user_profile)

    context = {'form': form}
    return render(request, 'accounts/profile.html', context)

@login_required
def profile(request):
    try:
        user_profile = request.user.profile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=request.user) # Handle case where profile might not exist
    context = {'user_profile': user_profile}
    return render(request, 'accounts/profile.html', context)

@login_required
def update_pic(request):
    if request.method == 'POST' and request.FILES.get('pic') and request.POST.get('type'):
        type = request.POST.get('type')
        print(type)
        user_profile = request.user.profile
        if type == 'profile_pic':
            user_profile.profile_pic = request.FILES['pic']
            user_profile.save()
            return JsonResponse({'success': True, 'message': 'Profile picture updated successfully!', 'pic_url': user_profile.profile_pic.url})
        elif type == 'cover_pic':
            user_profile.cover_pic = request.FILES['pic']
            user_profile.save()
            return JsonResponse({'success': True, 'message': 'Cover picture updated successfully!', 'pic_url': user_profile.cover_pic.url})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request or no file provided.'}, status=400)
    

@login_required
def user_profile_update(request):
    try:
        user_profile = request.user.profile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=request.user)

    if request.method == 'POST':
        form = UserProfileFormWithPic(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('user_profile_update')  # Redirect to the profile view (you need to define this URL)
        else:
            messages.error(request, 'There was an error updating your profile. Please correct the form.')
    else:
        form = UserProfileFormWithPic(instance=user_profile)

    context = {'form': form}
    return render(request, 'accounts/user-profile.html', context)



