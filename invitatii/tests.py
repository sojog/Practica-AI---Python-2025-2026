from django.test import TestCase
from .models import Event
from . import chat_service
from django.utils import timezone
import datetime

class ChatServiceTest(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            bride_name="Bianca",
            groom_name="Cosmin",
            date=timezone.now() + datetime.timedelta(days=30),
            location="Pitești",
            details="Start at 4PM.\nDress code: Elegant.\nSee you there."
        )

    def test_detect_intent(self):
        self.assertEqual(chat_service.detect_intent("What is the bride and groom name?"), "bride_groom")
        self.assertEqual(chat_service.detect_intent("Who are the bride and groom?"), "bride_groom")
        self.assertEqual(chat_service.detect_intent("Bride name"), "bride_groom")
        # Dress code
        self.assertEqual(chat_service.detect_intent("What is the dress code"), "dress_code")
        # Date
        self.assertEqual(chat_service.detect_intent("When is the wedding"), "when")
        # Location
        self.assertEqual(chat_service.detect_intent("Where is it held"), "where")
        
    def test_build_response_bride_groom(self):
        # Expect detailed bio for Bianca & Cosmin
        resp = chat_service.build_response("bride_groom", self.event)
        self.assertIn("BIANCA & COSMIN", resp)
        self.assertIn("green eyes", resp)
        self.assertIn("firefighter", resp)

    def test_detect_intent_description(self):
        self.assertEqual(chat_service.detect_intent("what is bride and groom description"), "bride_groom")
        self.assertEqual(chat_service.detect_intent("personality"), "bride_groom")

    def test_build_response_dress_code(self):
        # Expect only extraction
        resp = chat_service.build_response("dress_code", self.event)
        self.assertIn("Elegant", resp)
        self.assertNotIn("Start at 4PM", resp)

    def test_build_response_no_event(self):
        resp = chat_service.build_response("bride_groom", None)
        self.assertIn("No event found", resp)
