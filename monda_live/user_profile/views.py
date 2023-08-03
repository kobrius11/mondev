from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect
from . forms import ProfileUpdateForm, UserUpdateForm, SignupForm
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from verify_email.email_handler import send_verification_email
from verify_email.views import verify_user_and_activate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils.timezone import now
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

@login_required
def profile(request, user_id=None):
    if user_id == None:
        user = request.user
    else:
        user = get_object_or_404(get_user_model(), id=user_id)
    user.last_login = now()
    user.save()
    return render(request, 'user_profile/profile.html', {'user_': user})

@login_required
@csrf_protect
def profile_update(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            logger.info(f"Profile updated by user: '{request.user.username}'")
            messages.success(request, _("Profile updated."))
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'user_profile/profile_update.html', {'user_form': user_form, 'profile_form': profile_form})


class SignupView(FormView):
    template_name = 'user_profile/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('page_slug', kwargs={'slug': 'user_registration_successful'})

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.is_active = False
        user.save()
        logger.info(f"User registration successful by user: '{user.username}'")
        inactive_user = send_verification_email(self.request, form)

        messages.success(self.request, _("User registration successful!"))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _("Error occurred during registration."))
        logger.warning(f"Error occurred during registration")
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            logger.info(f"In order to sign up, you need to logout first")
            messages.info(self.request, _('In order to sign up, you need to logout first'))
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)
    
class EmailTemplateView(TemplateView):
    template_name = 'verify_email/email_verification_successful.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["link"] = self.request.path
        return context
    

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    logger.info(f"User logged in. User: '{user.username}'")

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    logger.info(f"User logged out. User: '{user.username}'")
