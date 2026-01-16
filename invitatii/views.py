from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import json
from .models import Event, Guest, Invitation, InvitationTemplate
from django import forms
from . import ai_service, ai_image_service, image_composer
from .models import Event, Guest, Invitation, InvitationTemplate, GeneratedInvitation

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['bride_name', 'groom_name', 'date', 'location', 'details']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['name', 'email', 'phone']

def event_list(request):
    """
    Displays a list of all wedding events.
    """
    events = Event.objects.all().order_by('-date')
    return render(request, 'invitatii/event_list.html', {'events': events})

def event_create(request):
    """
    Handles the creation of a new event.
    Redirects to the guest management page upon success.
    """
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            return redirect('guest_list', event_id=event.id)
    else:
        form = EventForm()
    return render(request, 'invitatii/event_form.html', {'form': form})

def guest_list(request, event_id):
    """
    Lists all guests for a specific event.
    """
    event = get_object_or_404(Event, pk=event_id)
    guests = event.guests.all()
    return render(request, 'invitatii/guest_list.html', {'event': event, 'guests': guests})

def guest_add(request, event_id):
    """
    Adds a new guest to an event.
    """
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = GuestForm(request.POST)
        if form.is_valid():
            guest = form.save(commit=False)
            guest.event = event
            guest.save()
            return redirect('guest_list', event_id=event.id)
    else:
        form = GuestForm()
    return render(request, 'invitatii/guest_form.html', {'form': form, 'event': event})

def generate_invitation(request, event_id):
    event = Event.objects.get(pk=event_id)
    generated_text = ""
    if request.method == 'POST':
        style = request.POST.get('style')
        generated_text = ai_service.AIService.generate_invitation_text(event, style)
        
        # Save as an Invitation (optional for now, but good to have)
        # For simplicity, we just show it, user can save later or we save automatically
        
    return render(request, 'invitatii/generate_text.html', {'event': event, 'generated_text': generated_text})

def render_invitation(request, invitation_id):
    invitation = get_object_or_404(Invitation, pk=invitation_id)
    # For now, we assume the template name matches a file in templates/invit/
    # In the future, we might render html_content from the DB
    template_name = invitation.template.name if invitation.template else 'default'
    template_file = f'invit/{template_name}.html'
    return render(request, template_file, {'invitation': invitation})

def save_invitation(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        template_name = request.POST.get('template_name')
        
        # Get or create the template object (temporary logic until we have admin seeding)
        template, _ = InvitationTemplate.objects.get_or_create(name=template_name)
        
        invitation = Invitation.objects.create(event=event, content=content, template=template)
        return redirect('render_invitation', invitation_id=invitation.id)
    return redirect('event_list')
    return redirect('event_list')

def generate_invitation_image(request, event_id):
    """
    Triggers the AI image generation and Pillow composition.
    """
    event = get_object_or_404(Event, pk=event_id)
    
    if request.method == 'POST':
        tone = request.POST.get('tone', 'formal')
        ai_text = request.POST.get('ai_text', '')
        
        # Create the GeneratedInvitation record
        invitation = GeneratedInvitation.objects.create(
            event=event,
            tone=tone,
            ai_text=ai_text
        )
        
        # 1. Generate Background (Mock AI)
        prompt = f"Wedding invitation background, {tone} style"
        bg_path = ai_image_service.AIImageService.generate_wedding_background_image(prompt)
        invitation.background_image = bg_path
        invitation.save()
        
        # 2. Compose Final Image (Pillow)
        image_composer.ImageComposer.render_final_invitation_image(invitation)
        
        return redirect('invitation_image_detail', invitation_id=invitation.id)
        
    return redirect('generate_invitation', event_id=event.id)

def invitation_image_detail(request, invitation_id):
    """
    Displays the final generated invitation image.
    """
    invitation = get_object_or_404(GeneratedInvitation, pk=invitation_id)
    return render(request, 'invitatii/invitation_image_detail.html', {'invitation': invitation})

from . import chat_service

def chat_page(request):
    """
    Renders the chatbot UI page.
    """
    return render(request, 'chatbot.html')

def chatbot_response(request):
    """
    API endpoint for the chatbot.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = data.get("message", "")
            # Prefer answering using the latest created Event
            event = Event.objects.order_by('-id').first()
            
            intent = chat_service.detect_intent(message)
            reply = chat_service.build_response(intent, event)
            
            return JsonResponse({"reply": reply})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "POST required"}, status=405)
