import os
import struct
import array

def generate_mo_file(po_file_path, mo_file_path):
    """
    Generate a binary .mo file from a .po file.
    This is a simplified implementation of msgfmt.
    """
    with open(po_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    messages = {}
    current_msgid = None
    current_msgstr = None
    in_msgid = False
    in_msgstr = False
    
    # Simple parser
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
            
        if line.startswith('msgid "'):
            if current_msgid is not None and current_msgstr is not None:
                messages[current_msgid] = current_msgstr
            
            current_msgid = line[7:-1]
            current_msgstr = ""
            in_msgid = True
            in_msgstr = False
        elif line.startswith('msgstr "'):
            current_msgstr = line[8:-1]
            in_msgid = False
            in_msgstr = True
        elif line.startswith('"'):
            content = line[1:-1]
            if in_msgid:
                current_msgid += content
            elif in_msgstr:
                current_msgstr += content

    # Add the last message
    if current_msgid is not None and current_msgstr is not None:
        messages[current_msgid] = current_msgstr

    # Process escapes
    def unescape(s):
        return s.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"')

    # Prepare data for .mo file
    # The header (empty msgid) MUST be included
    
    keys = sorted(messages.keys())
    # Ensure empty string (header) is first if present
    if "" in keys:
        keys.remove("")
        keys.insert(0, "")
    
    offsets = []
    ids = b''
    strs = b''
    
    for k in keys:
        v = messages[k]
        k = unescape(k).encode('utf-8')
        v = unescape(v).encode('utf-8')
        
        offsets.append((len(ids), len(k), len(strs), len(v)))
        ids += k + b'\0'
        strs += v + b'\0'

    # Write .mo file
    # Magic number: 0x950412de
    # Version: 0
    # Number of strings
    # Offset of table with original strings
    # Offset of table with translation strings
    # Size of hash table (0)
    # Offset of hash table (0)
    
    with open(mo_file_path, 'wb') as f:
        # Header
        f.write(struct.pack('I', 0x950412de)) # Magic
        f.write(struct.pack('I', 0))          # Version
        f.write(struct.pack('I', len(keys)))  # N strings
        
        # Offsets
        o_table_offset = 28
        t_table_offset = 28 + (len(keys) * 8)
        
        f.write(struct.pack('I', o_table_offset))
        f.write(struct.pack('I', t_table_offset))
        f.write(struct.pack('I', 0)) # Hash size
        f.write(struct.pack('I', 0)) # Hash offset
        
        # Table of original strings
        # Length, Offset
        ids_start = t_table_offset + (len(keys) * 8)
        for o in offsets:
            f.write(struct.pack('II', o[1], ids_start + o[0]))
            
        # Table of translation strings
        # Length, Offset
        strs_start = ids_start + len(ids)
        for o in offsets:
            f.write(struct.pack('II', o[3], strs_start + o[2]))
            
        # Data
        f.write(ids)
        f.write(strs)

    print(f"Compiled {po_file_path} -> {mo_file_path}")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    locale_dir = os.path.join(base_dir, 'locale')
    
    for lang in ['en', 'ro']:
        po_path = os.path.join(locale_dir, lang, 'LC_MESSAGES', 'django.po')
        mo_path = os.path.join(locale_dir, lang, 'LC_MESSAGES', 'django.mo')
        
        if os.path.exists(po_path):
            try:
                generate_mo_file(po_path, mo_path)
            except Exception as e:
                print(f"Error compiling {po_path}: {e}")
        else:
            print(f"Warning: {po_path} not found")

if __name__ == '__main__':
    main()
