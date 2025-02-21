import base64
import tempfile
import tkinter as tk
import os

class AppIcon:
    def __init__(self):
        self.ICON_DATA = base64.b64decode("""
        AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A
        ... (tam base64 verisi)
        """)
        
    def set_icon(self, root):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.ico') as tmp:
                tmp.write(self.ICON_DATA)
                tmp.flush()
                
            root.iconbitmap(tmp.name)
            tmp.close()
            os.unlink(tmp.name)
        except Exception as e:
            print(f"Icon load error: {str(e)}") 