from django.db import models
import uuid

class Event(models.Model):
    """
    Stores the main details of the wedding event.
    """
    bride_name = models.CharField(max_length=100, help_text="Name of the bride")
    groom_name = models.CharField(max_length=100, help_text="Name of the groom")
    date = models.DateTimeField(help_text="Date and time of the wedding")
    location = models.CharField(max_length=200, help_text="Venue address or name")
    details = models.TextField(blank=True, null=True, help_text="Extra info like dress code, etc.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bride_name} & {self.groom_name}"

class Guest(models.Model):
    """
    Represents a guest invited to a specific event.
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='guests')
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_attending = models.BooleanField(null=True, blank=True, help_text="RSVP status")
    
    def __str__(self):
        return self.name

class InvitationTemplate(models.Model):
    name = models.CharField(max_length=100)
    html_content = models.TextField(help_text="HTML content or path to template file")
    preview_image = models.ImageField(upload_to='template_previews/', blank=True, null=True)

    def __str__(self):
        return self.name

class Invitation(models.Model):
    # Renamed from GeneratedInvitation for simplicity, but matches the concept
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, blank=True, null=True)
    template = models.ForeignKey(InvitationTemplate, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invitation for {self.guest} - {self.event}"

class GeneratedInvitation(models.Model):
    """
    Stores the AI-generated invitation with background and final composition.
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, null=True, blank=True)
    tone = models.CharField(max_length=50, default="formal")
    ai_text = models.TextField()
    background_image = models.ImageField(upload_to="inv_backgrounds/", null=True, blank=True)
    final_image = models.ImageField(upload_to="inv_final/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Generated Image Invitation for {self.event} ({self.created_at})"
