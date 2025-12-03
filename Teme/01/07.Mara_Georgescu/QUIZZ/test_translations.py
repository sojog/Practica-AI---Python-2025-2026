#!/usr/bin/env python
"""
Test script to verify translations are working correctly.
Run this from the QUIZZ directory.
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'QUIZZ.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.utils import translation
from django.utils.translation import gettext as _

# Test translations
print("Testing Django translations...")
print("-" * 50)

# Test with English
translation.activate('en')
print(f"Language: {translation.get_language()}")
print(f"'Dashboard' -> '{_('Dashboard')}'")
print(f"'Back to Edit' -> '{_('Back to Edit')}'")
print()

# Test with Romanian
translation.activate('ro')
print(f"Language: {translation.get_language()}")
print(f"'Dashboard' -> '{_('Dashboard')}'")
print(f"'Back to Edit' -> '{_('Back to Edit')}'")
print(f"'Generate Quiz' -> '{_('Generate Quiz')}'")
print(f"'Upload Note' -> '{_('Upload Note')}'")
print()

# Check if .mo file exists
mo_file = 'locale/ro/LC_MESSAGES/django.mo'
if os.path.exists(mo_file):
    print(f"✓ Translation file exists: {mo_file}")
    print(f"  Size: {os.path.getsize(mo_file)} bytes")
else:
    print(f"✗ Translation file NOT found: {mo_file}")

print("-" * 50)
print("If Romanian translations show in English, the .mo file may be corrupted.")
print("Solution: Restart Django server to reload translations.")
