from model_mommy import mommy
from django.test.testcases import TestCase
from messaging.models import Message, Conversation
from profile.models import User

class MessageTest(TestCase):
    
    def setUp(self):
        self.user1 = mommy.make(User)
        self.user2 = mommy.make(User)
        self.conversation = mommy.make(Conversation)
        self.conversation.users.add(self.user1)
        self.conversation.users.add(self.user2)
        self.message1 = mommy.make(Message, conversation=self.conversation, sender=self.user1)
        self.message2 = mommy.make(Message, conversation=self.conversation, sender=self.user2)

    def test_message_delete(self):
        conversation_id = self.conversation.id
        self.assertEqual(self.message1.conversation.id, self.conversation.id)
        self.assertEqual(self.message2.conversation.id, self.conversation.id)
        self.message1.delete()
        self.assertEqual(self.message1.id, None)
        self.assertEqual(self.conversation.id, conversation_id)
        self.assertEqual(Message.objects.count(), 1)
        self.message2.delete()
        self.assertEqual(self.message2.id, None)
        self.assertEqual(self.conversation.id, None)
        self.assertEqual(Message.objects.count(), 0)
        self.assertEqual(Conversation.objects.count(), 0)

    def test_conversation_delete(self):
        self.conversation.messages.add(self.message2)
        self.assertEqual(self.conversation.messages.count(), 2)
        self.assertEqual(self.message1.conversation, self.conversation)
        self.assertEqual(self.message2.conversation, self.conversation)
        self.assertEqual(Message.objects.count(), 2)
        self.conversation.delete()
        self.assertEqual(Message.objects.count(), 0)
        self.assertEqual(Conversation.objects.count(), 0)

    def test_conversation_is_part_of(self):
        self.assertTrue(self.message1.conversation.is_part_of(self.message1.sender))
        self.assertTrue(self.message1.conversation.is_part_of(self.user1))
        self.assertFalse(self.message1.conversation.is_part_of(mommy.make(User)))
