from django.utils.translation import ugettext as _
from django.views.generic.detail import DetailView
from profile.models import User
from django.views.generic.edit import UpdateView, CreateView, FormView
from django.core.exceptions import PermissionDenied
from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse
from frontpage.forms import LoginForm
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from braces.views import LoginRequiredMixin


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Redirect if already logged in.
        if request.user.is_authenticated():
            return redirect('user', request.user.username)
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                if not self.request.POST.get('remember_me', None):
                    self.request.session.set_expiry(0)
                login(self.request, user)
                if 'next' in self.request.GET:
                    return HttpResponseRedirect(self.request.GET.get('next'))
                else:
                    return super(LoginView, self).form_valid(form)
            else:
                messages.warning(self.request, _(u'Your account is not acitve.'))
        else:
            messages.warning(self.request, _(u'Wrong username/password.'))
            return self.render_to_response(self.get_context_data(form=form))
        
    def get_context_data(self, **kwargs):
        context_data = super(LoginView, self).get_context_data(**kwargs)
        # Add username to context if user entered it.
        if kwargs['form'].data.get('username'):
            context_data['username'] = kwargs['form'].cleaned_data['username']
        return context_data
        
    def get_success_url(self):
        return reverse('user', args=[self.request.user.username])


class LogoutView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            logout(self.request)
        return reverse('frontpage')


class ProfileRediretView(RedirectView):
    permanent = False
    
    def get_redirect_url(self, *args, **kwargs):
        return reverse('user', args=[self.request.user.username])


class UserDetailView(DetailView):
    template_name = 'user_detail.html'
    
    def get_object(self):
        return get_object_or_404(User, username=self.kwargs['username'])


class UserCreateView(CreateView):
    model = User
    template_name = 'user_create.html'
    fields = ['username', 'first_name', 'last_name', 'email', 'password', 'profile_pic', 'instruments']

    def dispatch(self, request, *args, **kwargs):
        # Redirect if already logged in.
        if request.user.is_authenticated():
            return redirect('user', request.user.username)
        else:
            return super(UserCreateView, self).dispatch(request, *args, **kwargs)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'user_update.html'
    fields = ['first_name', 'last_name', 'email', 'gender', 'year', 'profile_pic', 'bio', 'instruments', 'genres', 'interests', 'region']
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get_object(self, *args, **kwargs):
        obj = super(UserUpdateView, self).get_object(*args, **kwargs)
        if not obj.username == self.request.user.username:
            raise PermissionDenied()
        return obj

