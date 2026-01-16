import re
from .models import Event

def detect_intent(message: str) -> str:
    """
    Analyzes the message and returns a string intent.
    """
    msg = message.lower()
    
    # Priority matches
    
    # Bride/Groom/Couple/Description
    if any(x in msg for x in ["bride", "groom", "couple", "names", "who are", "who is", "cine", "nunta", "married", "description", "personality", "descriere"]):
        return "bride_groom"
        
    # Dress code (specific handling requested)
    if any(x in msg for x in ["dress", "code", "wear", "tinuta", "îmbrac", "imbrac"]):
        return "dress_code"
        
    # Date/Time
    if any(x in msg for x in ["when", "date", "time", "ora", "când", "cand"]):
        return "when"
        
    # Location
    if any(x in msg for x in ["where", "location", "place", "venue", "unde", "locatie", "adresa"]):
        return "where"
        
    # Program
    if any(x in msg for x in ["program", "schedule", "plan", "timetable"]):
        return "program"
        
    # RSVP
    if any(x in msg for x in ["rsvp", "confirm", "attendance", "veniti"]):
        return "rsvp"
        
    return "unknown"

def build_response(intent: str, event: Event) -> str:
    """
    Constructs a friendly response based on the intent and event data.
    """
    if not event:
        return "No event found yet. Please create an event first."
        
    if intent == "bride_groom":
        # Check for specific couple Bianca & Cosmin to return detailed bio
        b_name = event.bride_name.strip().title()
        g_name = event.groom_name.strip().title()
        
        if "Bianca" in b_name and "Cosmin" in g_name:
             return (f"{b_name.upper()} & {g_name.upper()}\n\n"
                     f"Bride: {b_name} – green eyes, homemaker, and works as an engineer at a multinational company.\n"
                     f"Groom: {g_name} – firefighter, works in the emergency services, Pitești, Romania.")
        
        return f"The bride is {event.bride_name}. The groom is {event.groom_name}."
        
    elif intent == "when":
        return f"The wedding is on {event.date.strftime('%Y-%m-%d %H:%M')}."
        
    elif intent == "where":
        return f"The event will be held at {event.location}."
        
    elif intent == "dress_code":
        # Extract dress code from details if possible
        details = event.details or ""
        # Look for a line starting with Dress code or similar
        # Regex to find "Dress code: ..." or "Tinuta: ..."
        match = re.search(r"(?:dress\s*code|tinuta|attire)[\s:]+(.+?)(?:$|\n|\.)", details, re.IGNORECASE)
        if match:
            return f"Dress code info: {match.group(1).strip()}"
        else:
            # Fallback: if details is short, return it. If long, give a hint.
            if len(details) < 50:
                 return f"Dress code info: {details}" if details else "No specific dress code mentioned."
            else:
                 return "Please check the full invitation details for dress code information."
                 
    elif intent == "program":
        return f"Here is the plan: {event.details or 'Detailed schedule not yet available.'}"
        
    elif intent == "rsvp":
        return "Please contact us directly to confirm your attendance, or use the RSVP form if available."
        
    else:
        return "I'm sorry, I can only answer basic questions about the wedding (who, when, where, program, RSVP, dress code)."
