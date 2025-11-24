import os
from pathlib import Path

def extract_text_from_file(file):
    """
    Extract text from uploaded file.
    Supports: PDF, DOCX, TXT, and images (placeholder for OCR/multimodal AI)
    
    Args:
        file: Django UploadedFile object
    
    Returns:
        str: Extracted text
    """
    file_ext = Path(file.name).suffix.lower()
    
    try:
        if file_ext == '.txt':
            return extract_from_txt(file)
        elif file_ext == '.pdf':
            return extract_from_pdf(file)
        elif file_ext in ['.docx', '.doc']:
            return extract_from_docx(file)
        elif file_ext in ['.jpg', '.jpeg', '.png', '.webp']:
            return extract_from_image(file)
        else:
            return f"Unsupported file type: {file_ext}"
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def extract_from_txt(file):
    """Extract text from TXT file"""
    try:
        content = file.read()
        # Try UTF-8 first, fallback to latin-1
        try:
            return content.decode('utf-8')
        except UnicodeDecodeError:
            return content.decode('latin-1')
    except Exception as e:
        return f"Error reading TXT file: {str(e)}"

def extract_from_pdf(file):
    """Extract text from PDF file using pypdf"""
    try:
        from pypdf import PdfReader
        from io import BytesIO
        
        pdf_file = BytesIO(file.read())
        reader = PdfReader(pdf_file)
        
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n\n"
        
        return text.strip() if text.strip() else "No text found in PDF"
    except ImportError:
        return "PDF support not available. Install 'pypdf' library."
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def extract_from_docx(file):
    """Extract text from DOCX file using python-docx"""
    try:
        from docx import Document
        from io import BytesIO
        
        docx_file = BytesIO(file.read())
        doc = Document(docx_file)
        
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        
        return text.strip() if text.strip() else "No text found in DOCX"
    except ImportError:
        return "DOCX support not available. Install 'python-docx' library."
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"

def extract_from_image(file):
    """
    Placeholder for image text extraction.
    In production, this would use:
    - OCR (pytesseract + Pillow)
    - OR multimodal AI API (e.g., GPT-4 Vision, Gemini Vision)
    """
    return """[Image file uploaded]

NOTE: Image text extraction requires either:
1. OCR setup (pytesseract + Tesseract engine)
2. Multimodal AI API (GPT-4 Vision, Gemini Vision)

For now, please manually type or paste the text from your image below."""
