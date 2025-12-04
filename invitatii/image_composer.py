from PIL import Image, ImageDraw, ImageFont
import os
from django.conf import settings
import textwrap

class ImageComposer:
    """
    Composes the final invitation image by overlaying text on the background.
    """
    
    @staticmethod
    def render_final_invitation_image(invitation):
        """
        Overlays text on the background image and saves the result.
        
        Args:
            invitation (GeneratedInvitation): The invitation object.
        """
        # Load background image
        bg_path = settings.MEDIA_ROOT / str(invitation.background_image)
        try:
            img = Image.open(bg_path)
        except FileNotFoundError:
            return None

        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        # Fonts Configuration
        # Try to find system fonts or fallbacks
        # Windows paths
        font_dir = "C:/Windows/Fonts"
        
        try:
            # Elegant script font for names (e.g., Edwardian Script, Kunstler, or similar)
            # Fallback to a standard script if specific ones aren't found
            script_font_path = os.path.join(font_dir, "ITCEDSCR.TTF") # Edwardian Script
            if not os.path.exists(script_font_path):
                 script_font_path = os.path.join(font_dir, "GABRIOLA.TTF") # Gabriola
            
            # Serif font for body text
            serif_font_path = os.path.join(font_dir, "times.ttf") # Times New Roman
            
            # Load fonts
            name_font = ImageFont.truetype(script_font_path, 90)
            title_font = ImageFont.truetype(serif_font_path, 30)
            body_font = ImageFont.truetype(serif_font_path, 40)
            
        except IOError:
            # Absolute fallback
            name_font = ImageFont.load_default()
            title_font = ImageFont.load_default()
            body_font = ImageFont.load_default()
            
        # Colors
        gold_color = (184, 134, 11) # Dark Goldenrod
        dark_gray = (60, 60, 60)
        
        # Define center area (approximate safe zone inside the frame)
        # Assuming A5 portrait (approx 1748 x 2480 px at 300dpi, or smaller)
        # The generated image size might vary, so we calculate based on image size
        center_x = width / 2
        
        # Vertical spacing
        current_y = height * 0.25 # Start 25% down
        
        # 1. "Together with their families"
        text = "TOGETHER WITH THEIR FAMILIES"
        bbox = draw.textbbox((0, 0), text, font=title_font)
        w = bbox[2] - bbox[0]
        draw.text((center_x - w/2, current_y), text, font=title_font, fill=dark_gray)
        current_y += 80
        
        # 2. Couple Names
        names = f"{invitation.event.bride_name} & {invitation.event.groom_name}"
        bbox = draw.textbbox((0, 0), names, font=name_font)
        w = bbox[2] - bbox[0]
        draw.text((center_x - w/2, current_y), names, font=name_font, fill=gold_color)
        current_y += 150
        
        # 3. "Invite you to join their wedding celebration"
        text = "INVITE YOU TO JOIN THEIR WEDDING CELEBRATION"
        bbox = draw.textbbox((0, 0), text, font=title_font)
        w = bbox[2] - bbox[0]
        draw.text((center_x - w/2, current_y), text, font=title_font, fill=dark_gray)
        current_y += 100
        
        # 4. Date & Time
        date_str = invitation.event.date.strftime("%B %d, %Y").upper()
        time_str = invitation.event.date.strftime("AT %I:%M %p")
        
        bbox = draw.textbbox((0, 0), date_str, font=body_font)
        w = bbox[2] - bbox[0]
        draw.text((center_x - w/2, current_y), date_str, font=body_font, fill=dark_gray)
        current_y += 50
        
        bbox = draw.textbbox((0, 0), time_str, font=body_font)
        w = bbox[2] - bbox[0]
        draw.text((center_x - w/2, current_y), time_str, font=body_font, fill=dark_gray)
        current_y += 100
        
        # 5. Location
        location = invitation.event.location.upper()
        # Wrap location if too long
        wrapper = textwrap.TextWrapper(width=40)
        loc_lines = wrapper.wrap(text=location)
        
        for line in loc_lines:
            bbox = draw.textbbox((0, 0), line, font=body_font)
            w = bbox[2] - bbox[0]
            draw.text((center_x - w/2, current_y), line, font=body_font, fill=dark_gray)
            current_y += 50
            
        current_y += 50
        
        # 6. Reception
        text = "RECEPTION TO FOLLOW"
        bbox = draw.textbbox((0, 0), text, font=title_font)
        w = bbox[2] - bbox[0]
        draw.text((center_x - w/2, current_y), text, font=title_font, fill=dark_gray)
        
        # Save final image
        final_dir = settings.MEDIA_ROOT / 'inv_final'
        os.makedirs(final_dir, exist_ok=True)
        
        filename = f"final_{os.path.basename(invitation.background_image.name)}"
        filepath = final_dir / filename
        img.save(filepath)
        
        # Update model
        invitation.final_image = f"inv_final/{filename}"
        invitation.save()
