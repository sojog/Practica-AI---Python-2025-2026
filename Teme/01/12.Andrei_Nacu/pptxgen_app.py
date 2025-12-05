import sys
import os

# Fix for Protobuf error: Force python implementation
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

# Add the parent directory to sys.path to allow imports if running from inside PPTXGen folder
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from PPTXGen.gui import PPTXGenApp

if __name__ == "__main__":
    app = PPTXGenApp()
    app.mainloop()
