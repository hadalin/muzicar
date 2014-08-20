from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http.response import Http404
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from messaging.models import Message, Conversation
from profile.models import User
import datetime
from braces.views import LoginRequiredMixin
from django.views.generic.base import RedirectView


class MessagingView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'messaging.html'
    
    def get_queryset(self):
        # Get all conversation with current user
        conversation_list = Conversation.objects.filter(users__in=[self.request.user])
        if len(conversation_list) > 0:
            # Return latest messages from every conversation
            return [conversation.messages.all().order_by('-sent')[0] for conversation in conversation_list]
        else:
            return []
 
 
class ConversationRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False
    
    def get_redirect_url(self, *args, **kwargs):
        try:
            conversation = Conversation.objects.get(pk=kwargs['pk'])
            if not conversation.is_part_of(self.request.user):
                raise Http404
        except ObjectDoesNotExist:
            raise Http404
        # Get the other user, i.e. not current user.
        user = conversation.users.exclude(id=self.request.user.id)[0]
        return reverse('conversation', kwargs={'username': user.username})
 

class ConversationView(LoginRequiredMixin, CreateView):
    model = Message
    template_name = 'conversation.html'
    fields = ['body']
    
    def dispatch(self, request, *args, **kwargs):
        try:
            self.user = User.objects.get(username=kwargs['username'])
            # User can't send to himself
            if self.user.id == request.user.id:
                raise Http404
        except ObjectDoesNotExist:
            raise Http404

        return super(ConversationView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        conversation_list = Conversation.objects \
            .filter(users__in=[self.request.user]) \
            .filter(users__in=[self.user]) \
            .distinct()
        if len(conversation_list) == 1:
            kwargs['object_list'] = conversation_list[0].messages.all().order_by('sent')
        elif len(conversation_list) > 1:
            raise Exception('There seems to be more than one conversation between two users.')
        return super(ConversationView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        message = form.save(commit=False)
        conversation_list = Conversation.objects \
            .filter(users__in=[self.request.user]) \
            .filter(users__in=[self.user]) \
            .distinct()

        if len(conversation_list) == 0:
            # Conversation does not exist yet
            conversation = Conversation()
            conversation.save()
            conversation.users.add(self.request.user)
            conversation.users.add(self.user)

        elif len(conversation_list) == 1:
            # Conversation already exists
            conversation = conversation_list[0]

        else:
            # There can only be one conversation between two users
            # Raise exception
            raise Exception('There seems to be more than one conversation between two users.')
            
        message.conversation = conversation
        message.sender = self.request.user
        message.sent = datetime.datetime.now()
        message.save()
        return super(ConversationView, self).form_valid(form)

    def get_success_url(self):
        return reverse('conversation', args=[self.kwargs['username']])
