from django.db import models
from profile.models import User


class Conversation(models.Model):
    users = models.ManyToManyField(User, related_name='conversations')
    
    def is_part_of(self, user):
        """Check if user is part of conversation"""
        return True if len(self.users.filter(id__in=[user.id])) > 0 else False
    
    def delete(self):
        # Delete all messages in conversation as well
        self.messages.all().delete()
        super(Conversation, self).delete()
    

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='messages')
    sent = models.DateTimeField()
    body = models.TextField(max_length=2048)
    conversation = models.ForeignKey(Conversation, related_name='messages')

    def delete(self):
        super(Message, self).delete()
        if self.conversation.messages.count() == 0:
            # Delete conversation if it has no messages
            self.conversation.delete()
