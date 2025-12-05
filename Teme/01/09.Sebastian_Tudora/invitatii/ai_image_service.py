from PIL import Image, ImageDraw
import os
from django.conf import settings
import uuid
import shutil

class AIImageService:
    """
    Mocks an AI image generation service.
    """
    
    @staticmethod
    def generate_wedding_background_image(prompt):
        """
        Generates a mock background image based on the prompt.
        In a real scenario, this would call an API like Vertex AI or DALL-E.
        
        Returns:
            str: The relative path to the generated image.
        """
        # Create a directory for backgrounds if it doesn't exist
        bg_dir = settings.MEDIA_ROOT / 'inv_backgrounds'
        os.makedirs(bg_dir, exist_ok=True)
        
        # Use the high-quality pre-generated asset if available
        # In a real app, we might have a set of "AI generated" styles cached
        source_image = bg_dir / 'elegant_floral.png'
        
        filename = f"{uuid.uuid4()}.png"
        filepath = bg_dir / filename
        
        if os.path.exists(source_image):
            shutil.copy(source_image, filepath)
        else:
            # Fallback to simple generation if asset is missing
            color = (255, 240, 245) # Default pastel pink
            img = Image.new('RGB', (800, 1200), color=color)
            draw = ImageDraw.Draw(img)
            draw.rectangle([20, 20, 780, 1180], outline="gold", width=5)
            img.save(filepath)
        
        return f"inv_backgrounds/{filename}"
