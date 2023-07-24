from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect
from . forms import ProfileUpdateForm, UserUpdateForm, SignupForm
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from verify_email.email_handler import send_verification_email

User = get_user_model()


@login_required
def profile(request, user_id=None):
    if user_id == None:
        user = request.user
    else:
        user = get_object_or_404(get_user_model(), id=user_id)
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
            messages.success(request, "Profile updated.")
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'user_profile/profile_update.html', {'user_form': user_form, 'profile_form': profile_form})


# TODO: refactor to CBV form, also fix template: Done, but need to recheck for bugs
class SignupView(FormView):
    template_name = 'user_profile/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.is_active = False
        user.save()

        inactive_user = send_verification_email(self.request, form)

        messages.success(self.request, "User registration successful! Please check your email.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error occurred during registration.")
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.info(self.request, 'In order to sign up, you need to logout first')
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)
    
class EmailTemplateView(TemplateView):
    template_name = 'verify_email/email_verification_msg.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["link"] = self.request.path
        return context
    