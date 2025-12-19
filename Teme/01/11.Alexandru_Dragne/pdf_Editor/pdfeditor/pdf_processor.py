"""
PDF Processing Module - Core logic pentru editare text în PDF-uri.

Folosește PyMuPDF (fitz) pentru a găsi și înlocui text în PDF-uri,
păstrând layout-ul original cât mai mult posibil.
"""
import os
import re
from datetime import datetime
import fitz  # PyMuPDF
from django.conf import settings
from typing import Tuple, List, Optional


def parse_page_range(range_string: str, total_pages: int) -> List[int]:
    """
    Parsează un string de tipul '1-3,5,7-9' într-o listă de indici de pagini.
    
    Args:
        range_string: String cu intervale (ex: "1-3,5")
        total_pages: Numărul total de pagini din PDF
        
    Returns:
        Listă de indici de pagini (0-indexed)
        
    Raises:
        ValueError: Dacă range-ul este invalid
    """
    if not range_string or not range_string.strip():
        return list(range(total_pages))
    
    pages = set()
    parts = range_string.replace(' ', '').split(',')
    
    for part in parts:
        if '-' in part:
            # Range: "1-3"
            try:
                start, end = part.split('-')
                start_idx = int(start) - 1  # Convert to 0-indexed
                end_idx = int(end) - 1
                
                if start_idx < 0 or end_idx >= total_pages or start_idx > end_idx:
                    raise ValueError(f"Invalid page range: {part}")
                
                pages.update(range(start_idx, end_idx + 1))
            except ValueError as e:
                raise ValueError(f"Invalid page range format: {part}") from e
        else:
            # Single page: "5"
            try:
                page_num = int(part) - 1  # Convert to 0-indexed
                if page_num < 0 or page_num >= total_pages:
                    raise ValueError(f"Page {part} out of range (1-{total_pages})")
                pages.add(page_num)
            except ValueError as e:
                raise ValueError(f"Invalid page number: {part}") from e
    
    return sorted(list(pages))


def check_pdf_has_text(pdf_path: str) -> Tuple[bool, str]:
    """
    Verifică dacă PDF-ul conține text selectabil.
    
    Args:
        pdf_path: Calea către fișierul PDF
        
    Returns:
        Tuple (has_text: bool, message: str)
    """
    try:
        doc = fitz.open(pdf_path)
        has_text = False
        
        for page in doc:
            text = page.get_text().strip()
            if text:
                has_text = True
                break
        
        doc.close()
        
        if has_text:
            return True, "PDF-ul conține text selectabil."
        else:
            return False, "PDF-ul nu conține text selectabil (posibil scanat doar cu imagini)."
            
    except Exception as e:
        return False, f"Eroare la verificarea PDF-ului: {str(e)}"


def split_pdf(pdf_path: str, ranges: List[Tuple[int, int]]) -> List[str]:
    """
    Split PDF into multiple files based on page ranges.
    
    Args:
        pdf_path: Path to input PDF
        ranges: List of (start, end) tuples (1-indexed, inclusive)
                Example: [(1, 3), (5, 7)] splits pages 1-3 and 5-7
    
    Returns:
        List of paths to output PDF files
    """
    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        output_files = []
        
        # Determine output directory
        if '/media/uploads' in pdf_path:
            base_media = pdf_path.split('/media/uploads')[0]
            output_dir = os.path.join(base_media, 'media', 'processed')
        else:
            output_dir = os.path.join(os.path.dirname(pdf_path), 'processed')
        
        os.makedirs(output_dir, exist_ok=True)
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        
        for idx, (start, end) in enumerate(ranges, 1):
            # Validate range (1-indexed)
            if start < 1 or end > total_pages or start > end:
                raise ValueError(f"Invalid range: {start}-{end} (PDF has {total_pages} pages)")
            
            # Create new PDF with selected pages
            new_doc = fitz.open()
            new_doc.insert_pdf(doc, from_page=start-1, to_page=end-1)
            
            # Generate output filename
            if len(ranges) == 1:
                output_filename = f"{base_name}_pages_{start}-{end}.pdf"
            else:
                output_filename = f"{base_name}_part{idx}_pages_{start}-{end}.pdf"
            
            output_path = os.path.join(output_dir, output_filename)
            new_doc.save(output_path, garbage=4, deflate=True)
            new_doc.close()
            
            output_files.append(output_path)
        
        doc.close()
        return output_files
        
    except Exception as e:
        raise Exception(f"Error splitting PDF: {str(e)}")


def merge_pdfs(pdf_paths, output_name=None):
    """
    Merge multiple PDF files into one.
    
    Args:
        pdf_paths (list): List of absolute paths to PDF files in desired merge order
        output_name (str, optional): Custom name for output file (without .pdf extension)
    
    Returns:
        str: Path to the merged PDF file
    
    Raises:
        ValueError: If less than 2 PDFs provided or if any file doesn't exist
    """
    if len(pdf_paths) < 2:
        raise ValueError("At least 2 PDF files are required for merging")
    
    # Validate all files exist
    for pdf_path in pdf_paths:
        if not os.path.exists(pdf_path):
            raise ValueError(f"PDF file not found: {pdf_path}")
    
    # Create output document
    output_doc = fitz.open()
    
    try:
        # Append each PDF to the output document
        for pdf_path in pdf_paths:
            with fitz.open(pdf_path) as input_doc:
                output_doc.insert_pdf(input_doc)
        
        # Generate output filename
        if output_name:
            # User provided custom name
            filename = f"{output_name}.pdf"
        else:
            # Generate timestamp-based name
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"merged_{timestamp}.pdf"
        
        # Save to processed directory
        output_path = os.path.join(settings.MEDIA_ROOT, 'processed', filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        output_doc.save(output_path)
        output_doc.close()
        
        return output_path
        
    except Exception as e:
        output_doc.close()
        raise Exception(f"Error merging PDFs: {str(e)}")


def compress_pdf(pdf_path, quality='medium', output_name=None):
    """
    Compress PDF by reducing image quality and optimizing.
    
    Args:
        pdf_path (str): Absolute path to source PDF
        quality (str): 'low' (max compression), 'medium' (balanced), 'high' (minimal compression)
        output_name (str, optional): Custom output filename
    
    Returns:
        tuple: (output_path, original_size, compressed_size, compression_ratio)
    
    Raises:
        ValueError: If PDF file doesn't exist
    """
    if not os.path.exists(pdf_path):
        raise ValueError(f"PDF file not found: {pdf_path}")
    
    # Get original file size
    original_size = os.path.getsize(pdf_path)
    
    # Quality settings: (image_quality, deflate)
    quality_settings = {
        'low': {'quality': 50, 'deflate': True},      # Max compression
        'medium': {'quality': 75, 'deflate': True},   # Balanced
        'high': {'quality': 90, 'deflate': True}      # Minimal loss
    }
    
    settings_used = quality_settings.get(quality, quality_settings['medium'])
    
    try:
        # Open source document
        doc = fitz.open(pdf_path)
        
        # Process each page
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Get images on page
            image_list = page.get_images(full=True)
            
            for img_index, img in enumerate(image_list):
                xref = img[0]
                
                # Extract image
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                
                # Re-compress image with lower quality
                # Note: PyMuPDF will handle this during save with deflate
        
        # Generate output filename
        if output_name:
            filename = f"{output_name}.pdf"
        else:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"compressed_{timestamp}.pdf"
        
        # Save to processed directory
        output_path = os.path.join(settings.MEDIA_ROOT, 'processed', filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save with compression options
        doc.save(
            output_path,
            garbage=4,           # Maximum garbage collection
            deflate=settings_used['deflate'],  # Compress streams
            clean=True           # Clean up unused objects
        )
        doc.close()
        
        # Get compressed file size
        compressed_size = os.path.getsize(output_path)
        
        # Calculate compression ratio
        if original_size > 0:
            compression_ratio = ((original_size - compressed_size) / original_size) * 100
        else:
            compression_ratio = 0
        
        return output_path, original_size, compressed_size, compression_ratio
        
    except Exception as e:
        raise Exception(f"Error compressing PDF: {str(e)}")


def add_watermark(pdf_path, watermark_type, watermark_content, options=None):
    """
    Add watermark to PDF pages.
    
    Args:
        pdf_path: Source PDF absolute path
        watermark_type: 'text' or 'image'
        watermark_content: Text string or path to watermark image file
        options: dict with keys:
            - position: 'center', 'top-left', 'top-center', etc.
            - opacity: float 0.0-1.0
            - rotation: int angle in degrees
            - font_size: int (for text only)
    
    Returns:
        str: Path to watermarked PDF
    """
    if not os.path.exists(pdf_path):
        raise ValueError(f"PDF file not found: {pdf_path}")
    
    # Default options
    if options is None:
        options = {}
    
    position = options.get('position', 'center')
    opacity = float(options.get('opacity', 0.3))
    rotation = int(options.get('rotation', 45))
    font_size = int(options.get('font_size', 48))
    
    try:
        doc = fitz.open(pdf_path)
        
        # Pre-process image watermark ONCE before page loop (to avoid huge file sizes)
        temp_img_path = None
        if watermark_type == 'image':
            if not os.path.exists(watermark_content):
                raise ValueError(f"Watermark image not found: {watermark_content}")
            
            # Apply opacity and rotation to image using PIL
            from PIL import Image as PILImage
            
            # Open image with PIL
            pil_img = PILImage.open(watermark_content)
            
            # Convert to RGBA if not already
            if pil_img.mode != 'RGBA':
                pil_img = pil_img.convert('RGBA')
            
            # CRITICAL: Resize to reasonable dimensions to prevent huge PDFs
            # Max 800x800 for watermarks is more than enough
            max_size = 800
            if pil_img.width > max_size or pil_img.height > max_size:
                ratio = min(max_size / pil_img.width, max_size / pil_img.height)
                new_size = (int(pil_img.width * ratio), int(pil_img.height * ratio))
                pil_img = pil_img.resize(new_size, PILImage.LANCZOS)
            
            # Apply rotation (expand=True to keep entire rotated image)
            if rotation != 0:
                pil_img = pil_img.rotate(-rotation, expand=True, resample=PILImage.BICUBIC)
            
            # Apply opacity by adjusting alpha channel
            alpha = pil_img.split()[3]  # Get alpha channel
            alpha = alpha.point(lambda p: int(p * opacity))  # Apply opacity
            pil_img.putalpha(alpha)
            
            # Save temporarily with compression
            temp_img_path = watermark_content.replace('.', f'_watermark.')
            pil_img.save(temp_img_path, 'PNG', optimize=True, compress_level=9)
        
        # Process each page
        for page in doc:
            page_rect = page.rect
            page_width = page_rect.width
            page_height = page_rect.height
            
            if watermark_type == 'text':
                # Text watermark
                text = watermark_content
                
                # Calculate text dimensions (approximate)
                text_width = len(text) * font_size * 0.6
                text_height = font_size
                
                # Calculate position
                x, y = _calculate_position(position, page_width, page_height, text_width, text_height)
                
                # Create rotation matrix
                if rotation != 0:
                    # Rotate around text center point
                    center_x = x + text_width / 2
                    center_y = y + text_height / 2
                    mat = fitz.Matrix(1, 0, 0, 1, center_x, center_y)
                    mat = mat * fitz.Matrix(rotation)
                    mat = mat * fitz.Matrix(1, 0, 0, 1, -center_x, -center_y)
                else:
                    mat = fitz.Matrix(1, 0, 0, 1, 0, 0)
                
                # Insert text with opacity
                page.insert_text(
                    point=(x, y),
                    text=text,
                    fontsize=font_size,
                    fontname="helv-bold",
                    color=(0.5, 0.5, 0.5),
                    rotate=rotation,
                    overlay=True,
                    morph=(fitz.Point(x, y), mat)
                )
                
                # Apply opacity by adding transparent overlay
                # Note: PyMuPDF doesn't directly support text opacity, 
                # so we use a lighter color for transparency effect
                
            elif watermark_type == 'image':
                # Image already processed above, just insert it
                img_doc = fitz.open(temp_img_path)
                img_page = img_doc[0]
                img_rect = img_page.rect
                
                # Scale image to reasonable size (max 30% of page)
                max_width = page_width * 0.3
                max_height = page_height * 0.3
                
                scale = min(max_width / img_rect.width, max_height / img_rect.height, 1.0)  # Don't upscale
                img_width = img_rect.width * scale
                img_height = img_rect.height * scale
                
                # Calculate position
                x, y = _calculate_position(position, page_width, page_height, img_width, img_height)
                
                # Create target rectangle
                target_rect = fitz.Rect(x, y, x + img_width, y + img_height)
                
                # Insert image with opacity and rotation already applied
                page.insert_image(
                    target_rect,
                    filename=temp_img_path,
                    overlay=True
                )
                
                img_doc.close()
        
        # Clean up temp image file
        if temp_img_path and os.path.exists(temp_img_path):
            os.remove(temp_img_path)
        
        # Generate output filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"watermarked_{timestamp}.pdf"
        
        # Save to processed directory
        output_path = os.path.join(settings.MEDIA_ROOT, 'processed', filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        doc.save(output_path)
        doc.close()
        
        return output_path
        
    except Exception as e:
        raise Exception(f"Error adding watermark: {str(e)}")


def rotate_pages(pdf_path, rotation_angle, page_range=None):
    """
    Rotate specific pages in PDF.
    
    Args:
        pdf_path: Source PDF absolute path
        rotation_angle: 90, 180, or 270 degrees clockwise
        page_range: Optional page range string like '1-3,5,7-9' (1-indexed)
    
    Returns:
        str: Path to rotated PDF
    """
    if not os.path.exists(pdf_path):
        raise ValueError(f"PDF file not found: {pdf_path}")
    
    if rotation_angle not in [90, 180, 270]:
        raise ValueError("Rotation angle must be 90, 180, or 270 degrees")
    
    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        
        # Determine which pages to rotate
        if page_range:
            pages_to_rotate = parse_page_range(page_range, total_pages)
        else:
            pages_to_rotate = list(range(total_pages))  # All pages
        
        # Rotate selected pages
        for page_idx in pages_to_rotate:
            page = doc[page_idx]
            page.set_rotation(rotation_angle)
        
        # Generate output filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"rotated_{timestamp}.pdf"
        
        # Save to processed directory
        output_path = os.path.join(settings.MEDIA_ROOT, 'processed', filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        doc.save(output_path)
        doc.close()
        
        return output_path
        
    except Exception as e:
        raise Exception(f"Error rotating pages: {str(e)}")


def add_page_numbers(pdf_path, options=None):
    """
    Add page numbers to PDF pages.
    
    Args:
        pdf_path: Source PDF absolute path
        options: dict with keys:
            - position: 'bottom-center', 'bottom-left', 'bottom-right', 
                       'top-center', 'top-left', 'top-right'
            - format: 'number' (1,2,3), 'page_number' (Page 1), 'of_total' (1 of 10)
            - font_size: int (default 12)
            - start_page: int (default 1, 1-indexed)
    
    Returns:
        str: Path to PDF with page numbers
    """
    if not os.path.exists(pdf_path):
        raise ValueError(f"PDF file not found: {pdf_path}")
    
    # Default options
    if options is None:
        options = {}
    
    position = options.get('position', 'bottom-center')
    format_type = options.get('format', 'number')
    font_size = int(options.get('font_size', 12))
    start_page = int(options.get('start_page', 1))
    
    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        
        for page_idx, page in enumerate(doc):
            if page_idx < start_page - 1:
                continue  # Skip pages before start_page
            
            page_rect = page.rect
            page_width = page_rect.width
            page_height = page_rect.height
            
            # Calculate page number for display
            display_page_num = page_idx + 1
            
            # Format the page number text
            if format_type == 'number':
                page_text = str(display_page_num)
            elif format_type == 'page_number':
                page_text = f"Page {display_page_num}"
            elif format_type == 'of_total':
                page_text = f"{display_page_num} of {total_pages}"
            else:
                page_text = str(display_page_num)
            
            # Calculate position
            margin = 30
            text_width = len(page_text) * font_size * 0.6  # Approximate width
            
            if position == 'bottom-center':
                x = (page_width - text_width) / 2
                y = page_height - margin
            elif position == 'bottom-left':
                x = margin
                y = page_height - margin
            elif position == 'bottom-right':
                x = page_width - text_width - margin
                y = page_height - margin
            elif position == 'top-center':
                x = (page_width - text_width) / 2
                y = margin + font_size
            elif position == 'top-left':
                x = margin
                y = margin + font_size
            elif position == 'top-right':
                x = page_width - text_width - margin
                y = margin + font_size
            else:
                x = (page_width - text_width) / 2
                y = page_height - margin
            
            # Insert page number
            page.insert_text(
                point=(x, y),
                text=page_text,
                fontsize=font_size,
                fontname="helv",
                color=(0, 0, 0),
                overlay=True
            )
        
        # Generate output filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"numbered_{timestamp}.pdf"
        
        # Save to processed directory
        output_path = os.path.join(settings.MEDIA_ROOT, 'processed', filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        doc.save(output_path)
        doc.close()
        
        return output_path
        
    except Exception as e:
        raise Exception(f"Error adding page numbers: {str(e)}")


def extract_text_from_pdf(pdf_path):
    """
    Extract text from PDF using PyMuPDF (native text extraction).
    Works best for PDFs with actual text layers.
    
    Args:
        pdf_path: Source PDF absolute path
    
    Returns:
        str: Extracted text from all pages
    
    Raises:
        ValueError: If PDF file doesn't exist
    """
    if not os.path.exists(pdf_path):
        raise ValueError(f"PDF file not found: {pdf_path}")
    
    try:
        doc = fitz.open(pdf_path)
        text_content = []
        
        for page_num, page in enumerate(doc, 1):
            page_text = page.get_text()
            if page_text.strip():
                text_content.append(f"=== Page {page_num} ===\n{page_text}\n")
        
        doc.close()
        
        if not text_content:
            return "No text found in PDF. This might be a scanned document - try OCR instead."
        
        return "\n".join(text_content)
        
    except Exception as e:
        raise Exception(f"Error extracting text: {str(e)}")


def ocr_pdf_to_text(pdf_path):
    """
    OCR PDF to text using pytesseract.
    Converts each page to image, then applies OCR.
    Best for scanned PDFs or images.
    
    Args:
        pdf_path: Source PDF absolute path
    
    Returns:
        str: OCR-extracted text from all pages
    
    Raises:
        ValueError: If PDF file doesn't exist
    """
    if not os.path.exists(pdf_path):
        raise ValueError(f"PDF file not found: {pdf_path}")
    
    try:
        import pytesseract
        from PIL import Image
        import io
        
        doc = fitz.open(pdf_path)
        text_content = []
        
        for page_num, page in enumerate(doc, 1):
            # Convert page to image
            pix = page.get_pixmap(dpi=300)  # Higher DPI for better OCR
            img_data = pix.tobytes("png")
            
            # Open with PIL
            img = Image.open(io.BytesIO(img_data))
            
            # Perform OCR
            page_text = pytesseract.image_to_string(img)
            
            if page_text.strip():
                text_content.append(f"=== Page {page_num} ===\n{page_text}\n")
        
        doc.close()
        
        if not text_content:
            return "No text could be extracted via OCR. The document might be blank or poor quality."
        
        return "\n".join(text_content)
        
    except ImportError:
        raise Exception("pytesseract not installed. Run: pip install pytesseract")
    except Exception as e:
        raise Exception(f"Error performing OCR: {str(e)}")


def _calculate_position(position, page_width, page_height, content_width, content_height):
    """Calculate x, y coordinates based on position name."""
    positions = {
        'top-left': (20, content_height + 20),
        'top-center': ((page_width - content_width) / 2, content_height + 20),
        'top-right': (page_width - content_width - 20, content_height + 20),
        'center-left': (20, (page_height + content_height) / 2),
        'center': ((page_width - content_width) / 2, (page_height + content_height) / 2),
        'center-right': (page_width - content_width - 20, (page_height + content_height) / 2),
        'bottom-left': (20, page_height - 20),
        'bottom-center': ((page_width - content_width) / 2, page_height - 20),
        'bottom-right': (page_width - content_width - 20, page_height - 20),
    }
    
    return positions.get(position, positions['center'])


def extract_font_info_at_position(page, rect):
    """
    Încearcă să extragă informații despre font din poziția specificată.
    
    Args:
        page: PyMuPDF page object
        rect: Rectangle (fitz.Rect) cu poziția textului
        
    Returns:
        Dict cu fontname, fontsize, color
    """
    # Default values - folosim fonturi standard PyMuPDF (Base14)
    font_info = {
        'fontname': 'helv',
        'fontsize': 11,
        'color': (0, 0, 0)
    }
    
    # Mapping pentru fonturi comune din PDF -> fonturi PyMuPDF Base14
    # PyMuPDF suportă doar anumite fonturi pentru insert_text
    font_mapping = {
        'times': 'times',
        'timesnewroman': 'times',
        'times-roman': 'times',
        'times-bold': 'tibo',
        'times-italic': 'tiri',
        'times-bolditalic': 'tibi',
        'helvetica': 'helv',
        'arial': 'helv',
        'helvetica-bold': 'hebo',
        'arial-bold': 'hebo',
        'helvetica-oblique': 'heit',
        'arial-italic': 'heit',
        'courier': 'cour',
        'couriernew': 'cour',
        'courier-bold': 'cobo',
        'courier-oblique': 'coit',
        'symbol': 'symb',
        'zapfdingbats': 'zadb',
    }
    
    try:
        # Get text blocks with detailed information
        blocks = page.get_text("dict", flags=fitz.TEXTFLAGS_TEXT)
        
        # Find the block that overlaps with our rectangle
        for block in blocks.get("blocks", []):
            if block.get("type") != 0:  # 0 = text block
                continue
                
            for line in block.get("lines", []):
                line_bbox = fitz.Rect(line["bbox"])
                if line_bbox.intersects(rect):
                    # Found overlapping line, get font info from first span
                    for span in line.get("spans", []):
                        # Get original font name from PDF
                        original_font = span.get('font', 'helv').lower()
                        
                        # Clean up font name (remove subset prefix like "ABCDEF+")
                        if '+' in original_font:
                            original_font = original_font.split('+')[1]
                        
                        # Remove hyphens and spaces for matching
                        clean_font = original_font.replace('-', '').replace(' ', '')
                        
                        # Try to find a matching PyMuPDF font
                        matched_font = 'helv'  # default
                        for pdf_font, pymupdf_font in font_mapping.items():
                            if pdf_font in clean_font:
                                matched_font = pymupdf_font
                                break
                        
                        font_info['fontname'] = matched_font
                        font_info['fontsize'] = span.get('size', 11)
                        font_info['color'] = span.get('color', 0)  # Integer color code
                        
                        # Convert integer color to RGB tuple if needed
                        if isinstance(font_info['color'], int):
                            # PyMuPDF color is BGR integer, convert to RGB float tuple
                            color_int = font_info['color']
                            r = (color_int >> 16) & 0xFF
                            g = (color_int >> 8) & 0xFF
                            b = color_int & 0xFF
                            font_info['color'] = (r/255.0, g/255.0, b/255.0)
                        
                        return font_info
    except Exception:
        pass
    
    return font_info


def detect_text_line_containing(page, target_rect):
    """
    Detectează LINIA de text care conține rectangleul dat (nu blocul întreg).
    
    Args:
        page: PyMuPDF page object
        target_rect: Rectangle care conține textul căutat
        
    Returns:
        Dict cu informații despre linie: {
            'rect': fitz.Rect - boundary-ul liniei,
            'text': str - textul complet din linie,
            'font_info': Dict - informații despre font,
            'alignment': str - 'left', 'center', 'right',
            'y_position': float - poziția Y a liniei
        }
    """
    blocks = page.get_text("dict", flags=fitz.TEXTFLAGS_TEXT)
    page_width = page.rect.width
    
    for block in blocks.get("blocks", []):
        if block.get("type") != 0:  # Skip non-text blocks
            continue
        
        for line in block.get("lines", []):
            line_rect = fitz.Rect(line["bbox"])
            
            # Check if target rectangle intersects with this line
            if line_rect.intersects(target_rect) or line_rect.contains(target_rect):
                # Found the line!
                line_text = ""
                font_info = None
                
                # Extract text and font info from spans
                for span in line.get("spans", []):
                    line_text += span.get("text", "")
                    
                    # Get font info from first span
                    if font_info is None:
                        original_font = span.get('font', 'helv').lower()
                        if '+' in original_font:
                            original_font = original_font.split('+')[1]
                        
                        font_info = {
                            'fontname': map_font_name(original_font),
                            'fontsize': span.get('size', 11),
                            'color': convert_color(span.get('color', 0))
                        }
                
                # Detect alignment based on x position in page
                x_center = (line_rect.x0 + line_rect.x1) / 2
                
                if x_center < page_width * 0.35:
                    alignment = 'left'
                elif x_center > page_width * 0.65:
                    alignment = 'right'
                else:
                    alignment = 'center'
                
                return {
                    'rect': line_rect,
                    'text': line_text,
                    'font_info': font_info or {'fontname': 'helv', 'fontsize': 11, 'color': (0, 0, 0)},
                    'alignment': alignment,
                    'y_position': line_rect.y1  # Bottom of line for text insertion
                }
    
    return None


def map_font_name(original_font):
    """Helper pentru maparea numelor de fonturi, păstrând bold/italic."""
    # Clean font name
    clean_font = original_font.replace('-', '').replace(' ', '').lower()
    
    # Detect style (bold, italic, bolditalic)
    is_bold = any(x in clean_font for x in ['bold', 'bd', 'heavy', 'black'])
    is_italic = any(x in clean_font for x in ['italic', 'it', 'oblique', 'slant'])
    
    # Detect base font family and return with proper style
    if any(x in clean_font for x in ['times', 'timesnewroman']):
        if is_bold and is_italic:
            return 'tibi'  # Times Bold Italic
        elif is_bold:
            return 'tibo'  # Times Bold
        elif is_italic:
            return 'tiit'  # Times Italic
        else:
            return 'tiro'  # Times Roman

    
    elif any(x in clean_font for x in ['helvetica', 'arial']):
        if is_bold and is_italic:
            return 'hebi'  # Helvetica Bold Italic
        elif is_bold:
            return 'hebo'  # Helvetica Bold
        elif is_italic:
            return 'heit'  # Helvetica Italic
        else:
            return 'helv'  # Helvetica
    
    elif any(x in clean_font for x in ['courier', 'couriernew']):
        if is_bold and is_italic:
            return 'cobi'  # Courier Bold Italic
        elif is_bold:
            return 'cobo'  # Courier Bold
        elif is_italic:
            return 'coit'  # Courier Italic
        else:
            return 'cour'  # Courier
    
    elif 'symbol' in clean_font:
        return 'symb'
    
    elif 'zapf' in clean_font or 'dingbat' in clean_font:
        return 'zadb'
    
    # Default fallback
    return 'helv'


def convert_color(color_int):
    """Helper pentru conversia culorilor."""
    if isinstance(color_int, int):
        r = (color_int >> 16) & 0xFF
        g = (color_int >> 8) & 0xFF
        b = color_int & 0xFF
        return (r/255.0, g/255.0, b/255.0)
    return (0, 0, 0)


def reflow_single_line(page, line_info, modified_text):
    """
    Re-renderează o SINGURĂ LINIE cu păstrarea poziției Y și alignment-ului.
    
    Args:
        page: PyMuPDF page object
        line_info: Informații despre linie (de la detect_text_line_containing)
        modified_text: Textul modificat al liniei
        
    Returns:
        bool: True dacă reflow-ul a reușit
    """
    try:
        line_rect = line_info['rect']
        font_info = line_info['font_info']
        alignment = line_info['alignment']
        y_pos = line_info['y_position']
        
        # Clear only this line
        clear_rect = fitz.Rect(line_rect)
        # Extend slightly to ensure clean removal
        clear_rect.x0 -= 5
        clear_rect.x1 = page.rect.width - clear_rect.x0  # Clear to same margin on right
        
        page.add_redact_annot(clear_rect, fill=(1, 1, 1))
        page.apply_redactions()
        
        # Calculate text width
        text_width = fitz.get_text_length(
            modified_text,
            fontname=font_info['fontname'],
            fontsize=font_info['fontsize']
        )
        
        # Calculate X position based on alignment
        page_width = page.rect.width
        
        if alignment == 'center':
            x_pos = (page_width - text_width) / 2
        elif alignment == 'right':
            x_pos = page_width - text_width - line_rect.x0  # Same margin as original
        else:  # left
            x_pos = line_rect.x0
        
        # Insert text at calculated position
        rc = page.insert_text(
            (x_pos, y_pos),
            modified_text,
            fontname=font_info['fontname'],
            fontsize=font_info['fontsize'],
            color=font_info['color']
        )
        
        return rc >= 0
        
    except Exception as e:
        return False


def rephrase_with_coordinates(
    pdf_path: str,
    page_number: int,
    bounding_box: dict,
    replace_text: str,
    original_text: str = ""
) -> Tuple[str, int, List[str]]:
    """
    Înlocuiește text în PDF folosind coordonate exacte din selecția PDF.js.
    Mută conținutul de sub selecție mai jos dacă textul nou e mai lung.
    
    Args:
        pdf_path: Calea către PDF-ul original
        page_number: Numărul paginii (0-indexed)
        bounding_box: Dict cu coordonatele {"x0": ..., "y0": ..., "x1": ..., "y1": ...}
        replace_text: Textul de înlocuire (reformulat de AI)
        original_text: Textul original (pentru a estima dimensiunea fontului)
        
    Returns:
        Tuple (output_path: str, replacement_count: int, warnings: List[str])
    """
    warnings = []
    
    try:
        doc = fitz.open(pdf_path)
        
        if page_number < 0 or page_number >= len(doc):
            doc.close()
            raise ValueError(f"Invalid page number: {page_number}")
        
        page = doc[page_number]
        page_width = page.rect.width
        page_height = page.rect.height
        
        # Create rectangle from bounding box
        rect = fitz.Rect(
            bounding_box['x0'],
            bounding_box['y0'],
            bounding_box['x1'],
            bounding_box['y1']
        )
        
        # Extract ALL text blocks from the page with positions
        text_dict = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)
        all_blocks = []
        
        for block in text_dict.get("blocks", []):
            if block.get("type") == 0:  # Text block
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        span_rect = fitz.Rect(span["bbox"])
                        span_text = span["text"]
                        if span_text.strip():
                            all_blocks.append({
                                "text": span_text,
                                "rect": span_rect,
                                "font": span.get("font", "helv"),
                                "size": span.get("size", 11),
                                "color": span.get("color", 0),
                                "flags": span.get("flags", 0)
                            })
        
        # Determine font for replacement text
        fontname = 'helv'
        fontsize = 11
        fontcolor = (0, 0, 0)
        
        # Find spans in or near the selection area to get font info
        for blk in all_blocks:
            if blk["rect"].intersects(rect):
                # Map font to PyMuPDF builtin
                fname = blk["font"].lower()
                if 'times' in fname or 'roman' in fname or 'serif' in fname:
                    fontname = 'tiro'
                elif 'courier' in fname or 'mono' in fname:
                    fontname = 'cour'
                elif 'bold' in fname:
                    fontname = 'hebo'
                else:
                    fontname = 'helv'
                fontsize = blk["size"]
                
                # Convert color
                color_int = blk["color"]
                if isinstance(color_int, int):
                    r = ((color_int >> 16) & 0xFF) / 255.0
                    g = ((color_int >> 8) & 0xFF) / 255.0
                    b = (color_int & 0xFF) / 255.0
                    fontcolor = (r, g, b)
                break
        
        # Calculate original height of selection
        original_height = rect.height
        original_width = rect.width
        
        # Calculate how much space the new text needs
        line_height = fontsize * 1.3
        char_width = fitz.get_text_length("x", fontname=fontname, fontsize=fontsize)
        chars_per_line = int(original_width / char_width) if char_width > 0 else 60
        
        # Word wrap replacement text
        words = replace_text.split()
        wrapped_lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            word_len = len(word)
            if current_length + word_len + 1 <= chars_per_line:
                current_line.append(word)
                current_length += word_len + 1
            else:
                if current_line:
                    wrapped_lines.append(' '.join(current_line))
                current_line = [word]
                current_length = word_len
        
        if current_line:
            wrapped_lines.append(' '.join(current_line))
        
        # Calculate new text height
        new_text_height = len(wrapped_lines) * line_height
        
        # Calculate extra space needed
        extra_space = max(0, new_text_height - original_height)
        
        if extra_space > 0:
            warnings.append(f"Content below selection shifted down by {extra_space:.0f}pt")
        
        # Separate blocks into: above selection, in selection, below selection
        blocks_above = []
        blocks_below = []
        
        selection_bottom = rect.y1
        
        for blk in all_blocks:
            blk_center_y = (blk["rect"].y0 + blk["rect"].y1) / 2
            
            if blk["rect"].intersects(rect):
                # Skip blocks in selection area - they will be replaced
                continue
            elif blk_center_y < rect.y0:
                # Above selection - keep as is
                blocks_above.append(blk)
            else:
                # Below selection - needs to be shifted down
                blocks_below.append(blk)
        
        # Clear the entire page
        page.add_redact_annot(page.rect, fill=(1, 1, 1))
        page.apply_redactions()
        
        # Re-insert blocks ABOVE selection (unchanged positions)
        for blk in blocks_above:
            # Map font for insertion
            fname = blk["font"].lower()
            if 'times' in fname or 'roman' in fname:
                insert_font = 'tiro'
            elif 'courier' in fname or 'mono' in fname:
                insert_font = 'cour'
            elif 'bold' in fname and 'italic' in fname:
                insert_font = 'hebi'
            elif 'bold' in fname:
                insert_font = 'hebo'
            elif 'italic' in fname:
                insert_font = 'heit'
            else:
                insert_font = 'helv'
            
            # Convert color
            color = (0, 0, 0)
            if isinstance(blk["color"], int):
                color_int = blk["color"]
                r = ((color_int >> 16) & 0xFF) / 255.0
                g = ((color_int >> 8) & 0xFF) / 255.0
                b = (color_int & 0xFF) / 255.0
                color = (r, g, b)
            
            page.insert_text(
                (blk["rect"].x0, blk["rect"].y1),  # baseline position
                blk["text"],
                fontname=insert_font,
                fontsize=blk["size"],
                color=color
            )
        
        # Insert NEW replacement text
        y_pos = rect.y0 + fontsize
        x_pos = rect.x0
        
        for line in wrapped_lines:
            page.insert_text(
                (x_pos, y_pos),
                line,
                fontname=fontname,
                fontsize=fontsize,
                color=fontcolor
            )
            y_pos += line_height
        
        # Re-insert blocks BELOW selection (shifted down by extra_space)
        for blk in blocks_below:
            fname = blk["font"].lower()
            if 'times' in fname or 'roman' in fname:
                insert_font = 'tiro'
            elif 'courier' in fname or 'mono' in fname:
                insert_font = 'cour'
            elif 'bold' in fname and 'italic' in fname:
                insert_font = 'hebi'
            elif 'bold' in fname:
                insert_font = 'hebo'
            elif 'italic' in fname:
                insert_font = 'heit'
            else:
                insert_font = 'helv'
            
            color = (0, 0, 0)
            if isinstance(blk["color"], int):
                color_int = blk["color"]
                r = ((color_int >> 16) & 0xFF) / 255.0
                g = ((color_int >> 8) & 0xFF) / 255.0
                b = (color_int & 0xFF) / 255.0
                color = (r, g, b)
            
            # Shift Y position down
            new_y = blk["rect"].y1 + extra_space
            
            # Check if it would overflow the page
            if new_y > page_height - 20:
                warnings.append("Some content may overflow the page")
            
            page.insert_text(
                (blk["rect"].x0, new_y),
                blk["text"],
                fontname=insert_font,
                fontsize=blk["size"],
                color=color
            )
        
        # Generate output path
        base_name = os.path.basename(pdf_path)
        name_without_ext = os.path.splitext(base_name)[0]
        
        if '/media/uploads' in pdf_path:
            base_media = pdf_path.split('/media/uploads')[0]
            processed_dir = os.path.join(base_media, 'media', 'processed')
        else:
            processed_dir = os.path.join(os.path.dirname(pdf_path), 'processed')
        
        os.makedirs(processed_dir, exist_ok=True)
        output_path = os.path.join(processed_dir, f"{name_without_ext}_rephrased.pdf")
        
        doc.save(output_path, garbage=4, deflate=True, clean=True)
        doc.close()
        
        return output_path, 1, warnings
        
    except Exception as e:
        raise Exception(f"Error processing PDF: {str(e)}")




def rephrase_text_in_pdf(
    pdf_path: str,
    search_text: str,
    replace_text: str,
    case_sensitive: bool = True,
    page_range: Optional[str] = None
) -> Tuple[str, int, List[str]]:
    """
    Caută și înlocuiește text în PDF, gestionând text pe mai multe linii.
    Folosește PyMuPDF search pentru a găsi textul exact.
    """
    import re
    warnings = []
    replacement_count = 0
    
    def normalize_whitespace(text):
        """Normalizează toate tipurile de whitespace la spații simple."""
        return ' '.join(text.split())
    
    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        
        if page_range:
            try:
                pages_to_process = parse_page_range(page_range, total_pages)
            except ValueError as e:
                doc.close()
                raise ValueError(f"Invalid page range: {str(e)}")
        else:
            pages_to_process = list(range(total_pages))
        
        # Normalize search text
        normalized_search = normalize_whitespace(search_text)
        words = normalized_search.split()
        
        if len(words) < 2:
            # For very short text, use regular find_and_replace
            doc.close()
            return find_and_replace_text(pdf_path, search_text, replace_text, case_sensitive, page_range)
        
        # Get first few words and last few words for searching
        first_words = ' '.join(words[:min(4, len(words))])
        last_words = ' '.join(words[-min(4, len(words)):])
        
        for page_num in pages_to_process:
            page = doc[page_num]
            
            # Verify text exists in page (normalized)
            page_text = page.get_text()
            normalized_page = normalize_whitespace(page_text)
            
            if case_sensitive:
                if normalized_search not in normalized_page:
                    continue
            else:
                if normalized_search.lower() not in normalized_page.lower():
                    continue
            
            # Search for first and last parts of the text
            first_rects = page.search_for(first_words)
            last_rects = page.search_for(last_words)
            
            if not first_rects or not last_rects:
                # Try with just first 2 words
                first_words = ' '.join(words[:2])
                last_words = ' '.join(words[-2:])
                first_rects = page.search_for(first_words)
                last_rects = page.search_for(last_words)
            
            if not first_rects or not last_rects:
                warnings.append(f"Could not locate text boundaries on page {page_num + 1}")
                continue
            
            # Use first occurrence of first_words and appropriate last_words
            first_rect = first_rects[0]
            
            # Find the last_rect that comes AFTER first_rect
            last_rect = None
            for lr in last_rects:
                if lr.y0 >= first_rect.y0 - 5:  # Same line or below
                    last_rect = lr
                    break
            
            if not last_rect:
                last_rect = last_rects[0]
            
            # Calculate combined bounding box
            combined_rect = fitz.Rect(
                min(first_rect.x0, last_rect.x0) - 2,
                first_rect.y0 - 2,
                max(first_rect.x1, last_rect.x1) + 2,
                last_rect.y1 + 2
            )
            
            # Get font info from this area
            font_info = extract_font_info_at_position(page, first_rect)
            if font_info['fontname'] not in ['helv', 'hebo', 'times', 'tibo', 'cour', 'cobo']:
                font_info['fontname'] = 'helv'
            
            # Redact (clear) the old text area
            page.add_redact_annot(combined_rect, fill=(1, 1, 1))
            page.apply_redactions()
            
            # Calculate text layout
            available_width = combined_rect.width
            char_width = fitz.get_text_length("x", fontname=font_info['fontname'], fontsize=font_info['fontsize'])
            chars_per_line = int(available_width / char_width) if char_width > 0 else 80
            
            # Word wrap replacement text
            rep_words = replace_text.split()
            lines = []
            current_line = []
            current_length = 0
            
            for word in rep_words:
                word_len = len(word)
                if current_length + word_len + 1 <= chars_per_line:
                    current_line.append(word)
                    current_length += word_len + 1
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                    current_line = [word]
                    current_length = word_len
            
            if current_line:
                lines.append(' '.join(current_line))
            
            # Insert new text
            line_height = font_info['fontsize'] * 1.2
            y_pos = combined_rect.y0 + font_info['fontsize']
            x_pos = combined_rect.x0
            
            for line in lines:
                page.insert_text(
                    (x_pos, y_pos),
                    line,
                    fontname=font_info['fontname'],
                    fontsize=font_info['fontsize'],
                    color=font_info['color']
                )
                y_pos += line_height
            
            replacement_count += 1
        
        # Save output
        base_name = os.path.basename(pdf_path)
        name_without_ext = os.path.splitext(base_name)[0]
        
        if '/media/uploads' in pdf_path:
            base_media = pdf_path.split('/media/uploads')[0]
            processed_dir = os.path.join(base_media, 'media', 'processed')
        else:
            processed_dir = os.path.join(os.path.dirname(pdf_path), 'processed')
        
        os.makedirs(processed_dir, exist_ok=True)
        output_path = os.path.join(processed_dir, f"{name_without_ext}_modified.pdf")
        
        doc.save(output_path, garbage=4, deflate=True, clean=True)
        doc.close()
        
        return output_path, replacement_count, warnings
        
    except Exception as e:
        raise Exception(f"Error processing PDF: {str(e)}")


def find_and_replace_text(
    pdf_path: str,
    search_text: str,
    replace_text: str,
    case_sensitive: bool = True,
    page_range: Optional[str] = None
) -> Tuple[str, int, List[str]]:
    """
    Găsește și înlocuiește text într-un PDF, păstrând layout-ul original.
    
    Args:
        pdf_path: Calea către PDF-ul original
        search_text: Textul de căutat
        replace_text: Textul de înlocuire
        case_sensitive: Dacă căutarea e case-sensitive
        page_range: String cu interval de pagini (ex: "1-3,5") sau None pentru toate
        
    Returns:
        Tuple (output_path: str, replacement_count: int, warnings: List[str])
        
    Raises:
        Exception: Dacă procesarea PDF-ului eșuează
    """
    warnings = []
    replacement_count = 0
    
    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        
        # Determine pages to process
        if page_range:
            try:
                pages_to_process = parse_page_range(page_range, total_pages)
            except ValueError as e:
                doc.close()
                raise ValueError(f"Invalid page range: {str(e)}")
        else:
            pages_to_process = list(range(total_pages))
        
        # Process each page
        for page_num in pages_to_process:
            page = doc[page_num]
            
            # Search for text in page
            # PyMuPDF search_for with flags parameter
            # No flags = case-sensitive; TEXT_INHIBIT_SPACES = case-insensitive
            if case_sensitive:
                text_instances = page.search_for(search_text)
            else:
                text_instances = page.search_for(search_text, flags=fitz.TEXT_INHIBIT_SPACES)
            
            if not text_instances:
                continue
            
            # Track which lines we've already processed to avoid duplicates
            processed_lines = set()
            
            # Process instances in REVERSE order to avoid position shifts
            for inst in reversed(text_instances):
                try:
                    # Detect the specific LINE containing this match (not the whole block!)
                    line_info = detect_text_line_containing(page, inst)
                    
                    if line_info is None:
                        warnings.append(
                            f"Warning pe pagina {page_num + 1}: Nu s-a putut detecta linia. "
                            f"Textul nu a fost înlocuit."
                        )
                        continue
                    
                    # Create a unique identifier for this line based on position
                    line_id = (round(line_info['rect'].x0, 2), 
                              round(line_info['rect'].y0, 2),
                              round(line_info['rect'].x1, 2), 
                              round(line_info['rect'].y1, 2))
                    
                    # Skip if we've already processed this line
                    if line_id in processed_lines:
                        continue
                    
                    processed_lines.add(line_id)
                    
                    # Get the line text
                    line_text = line_info['text']
                    
                    # Perform text replacement in this line only
                    if case_sensitive:
                        modified_line = line_text.replace(search_text, replace_text)
                        count_in_line = line_text.count(search_text)
                    else:
                        # Case-insensitive replacement
                        import re
                        pattern = re.compile(re.escape(search_text), re.IGNORECASE)
                        modified_line = pattern.sub(replace_text, line_text)
                        count_in_line = len(re.findall(pattern, line_text))
                    
                    # Re-render the line if text was modified
                    if modified_line != line_text:
                        success = reflow_single_line(page, line_info, modified_line)
                        
                        if success:
                            replacement_count += count_in_line
                        else:
                            warnings.append(
                                f"Warning pe pagina {page_num + 1}: Nu s-a putut re-renderarea liniei. "
                                f"Posibil text prea lung."
                            )
                        
                except Exception as e:
                    warnings.append(
                        f"Warning pe pagina {page_num + 1}: {str(e)}"
                    )
        
        # Generate output path
        base_name = os.path.basename(pdf_path)
        name_without_ext = os.path.splitext(base_name)[0]
        
        # Determine processed directory
        # If pdf_path is in .../media/uploads/, use .../media/processed/
        # Otherwise, use same directory as input with _processed suffix
        if '/media/uploads' in pdf_path:
            # Production mode: save to media/processed
            base_media = pdf_path.split('/media/uploads')[0]
            processed_dir = os.path.join(base_media, 'media', 'processed')
        else:
            # Test mode or direct call: save next to original file
            processed_dir = os.path.join(os.path.dirname(pdf_path), 'processed')
        
        os.makedirs(processed_dir, exist_ok=True)
        
        output_path = os.path.join(processed_dir, f"{name_without_ext}_modified.pdf")
        
        # Save with optimization
        doc.save(output_path, garbage=4, deflate=True, clean=True)
        doc.close()
        
        return output_path, replacement_count, warnings
        
    except Exception as e:
        raise Exception(f"Eroare la procesarea PDF-ului: {str(e)}")
