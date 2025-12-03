#!/usr/bin/env python
"""
Compile .po file to .mo file using polib library.
"""
import polib
import os

po_file = 'locale/ro/LC_MESSAGES/django.po'
mo_file = 'locale/ro/LC_MESSAGES/django.mo'

if os.path.exists(po_file):
    try:
        # Load .po file
        po = polib.pofile(po_file)
        
        # Save as .mo file
        po.save_as_mofile(mo_file)
        
        print(f"Successfully compiled {po_file} to {mo_file}")
        print(f"File size: {os.path.getsize(mo_file)} bytes")
        print(f"Translations: {len(po)} entries")
    except Exception as e:
        print(f"Error: {e}")
else:
    print(f"Error: {po_file} not found")
