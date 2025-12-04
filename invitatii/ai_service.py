import random

class AIService:
    """
    Service to handle AI text generation.
    Currently mocks the Gemini API.
    """
    
    @staticmethod
    def generate_invitation_text(event, style="formal"):
        """
        Generates invitation text based on event details and style.
        
        Args:
            event (Event): The event object containing details.
            style (str): The desired tone (formal, casual, funny).
            
        Returns:
            str: The generated text.
        """
        # In a real implementation, this would call the Gemini API
        # e.g., gemini.generate_content(prompt)
        
        bride = event.bride_name
        groom = event.groom_name
        date = event.date.strftime("%B %d, %Y at %I:%M %p")
        location = event.location
        
        prompts = {
            "formal": f"Together with their families, {bride} and {groom} request the honor of your presence at their marriage on {date} at {location}. Reception to follow.",
            "casual": f"Please join us for the wedding of {bride} and {groom} on {date} at {location}. We can't wait to celebrate with you!",
            "funny": f"{bride} and {groom} are finally getting hitched! Come eat our food and drink our booze on {date} at {location}. No backsies!"
        }
        
        return prompts.get(style, prompts["formal"])

# Singleton instance or just use static methods
ai_service = AIService()
