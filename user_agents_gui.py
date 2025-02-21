import sys
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import ua_generator
from datetime import datetime
import threading

class UAGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AgentX: Advanced User-Agent Generator with GUI")
        self.root.geometry("500x400")
        self.setup_icon()
        
        # Değişken tanımları
        self.device_var = tk.StringVar(value='desktop')
        self.platform_vars = {
            'windows': tk.BooleanVar(value=True),
            'macos': tk.BooleanVar(),
            'linux': tk.BooleanVar(),
            'ios': tk.BooleanVar(),
            'android': tk.BooleanVar()
        }
        self.browser_vars = {
            'chrome': tk.BooleanVar(value=True),
            'edge': tk.BooleanVar(),
            'firefox': tk.BooleanVar(),
            'safari': tk.BooleanVar()
        }
        
        # Widget'ları oluştur
        self.create_widgets()
        self.update_platform_options()
        self.device_var.trace_add('write', self.on_device_change)

    def setup_icon(self):
        try:
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            icon_path = os.path.join(base_path, 'ua.ico')
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print("Icon error:", e)

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Device Selection
        device_frame = ttk.LabelFrame(main_frame, text="Device Type")
        device_frame.pack(fill=tk.X, pady=5, anchor='w')
        
        ttk.Radiobutton(device_frame, text="Desktop", variable=self.device_var, 
                      value='desktop').pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(device_frame, text="Mobile", variable=self.device_var, 
                      value='mobile').pack(side=tk.LEFT)

        # Platform Selection
        platform_frame = ttk.LabelFrame(main_frame, text="Operating System")
        platform_frame.pack(fill=tk.X, pady=5, anchor='w')
        self.platform_container = ttk.Frame(platform_frame)
        self.platform_container.pack(side=tk.LEFT)

        # Browser Selection
        browser_frame = ttk.LabelFrame(main_frame, text="Supported Browsers")
        browser_frame.pack(fill=tk.X, pady=5)
        
        browsers = ['chrome', 'edge', 'firefox', 'safari']
        for browser in browsers:
            ttk.Checkbutton(browser_frame, variable=self.browser_vars[browser],
                          text=browser.capitalize()).pack(side=tk.LEFT, padx=10)

        # File Settings
        file_frame = ttk.Frame(main_frame)
        file_frame.pack(fill=tk.X, pady=10)
        ttk.Label(file_frame, text="Count:").pack(side=tk.LEFT)
        self.count_var = tk.IntVar(value=1000)
        ttk.Spinbox(file_frame, from_=1, to=100000, textvariable=self.count_var, 
                  width=8).pack(side=tk.LEFT, padx=5)
        ttk.Button(file_frame, text="Save Location", command=self.choose_file).pack(side=tk.RIGHT)
        self.filepath_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.filepath_var, width=40).pack(side=tk.RIGHT, 
                                                                         fill=tk.X, 
                                                                         expand=True, 
                                                                         padx=5)

        # Progress Bar
        self.progress_var = tk.DoubleVar()
        ttk.Progressbar(main_frame, variable=self.progress_var, 
                      maximum=100).pack(fill=tk.X, pady=10)

        # Generate Button
        ttk.Button(main_frame, text="Generate User Agents", 
                 command=self.start_generation).pack(pady=10)

        # Footer
        footer = ttk.Frame(main_frame)
        footer.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        ttk.Label(footer, text="WebAdHere Technologies", font=('Tahoma', 8)).pack(side=tk.LEFT)
        ttk.Label(footer, text="AgentX v2.0", font=('Tahoma', 8)).pack(side=tk.RIGHT)

    def update_platform_options(self):
        for widget in self.platform_container.winfo_children():
            widget.destroy()

        platforms = ['windows', 'macos', 'linux'] if self.device_var.get() == 'desktop' else ['ios', 'android']
        for platform in platforms:
            var = self.platform_vars[platform]
            text = "iOS" if platform == 'ios' else platform.capitalize()
            ttk.Checkbutton(self.platform_container, 
                          text=text, 
                          variable=var).pack(side=tk.LEFT, padx=5)

    def choose_file(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialdir=os.path.join(os.path.expanduser('~'), 'Desktop'),
            filetypes=[("Text files", "*.txt")]
        )
        if path:
            self.filepath_var.set(path)

    def start_generation(self):
        threading.Thread(target=self.generate_agents, daemon=True).start()

    def generate_agents(self):
        try:
            count = self.count_var.get()
            filepath = self.filepath_var.get() or os.path.join(
                os.path.expanduser('~'), 'Desktop',
                f'UserAgents_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
            )

            platforms = tuple(p for p, var in self.platform_vars.items() if var.get())
            browsers = tuple(b for b, var in self.browser_vars.items() if var.get())

            if not platforms:
                messagebox.showerror("Error", "Please select at least one platform!")
                return
            
            if not browsers:
                messagebox.showerror("Error", "Please select at least one browser!")
                return

            with open(filepath, 'w') as f:
                for i in range(count):
                    ua = ua_generator.generate(
                        device=self.device_var.get(),
                        platform=platforms,
                        browser=browsers
                    )
                    f.write(f"{ua}\n")
                    self.progress_var.set((i+1)/count*100)

            messagebox.showinfo("Success", f"{count} UAs created!\nSaved to: {filepath}")
            self.progress_var.set(0)

        except Exception as e:
            messagebox.showerror("Error", f"Error:\n{str(e)}")
            self.progress_var.set(0)

    def on_device_change(self, *args):
        self.update_platform_options()

if __name__ == "__main__":
    root = tk.Tk()
    app = UAGeneratorApp(root)
    root.mainloop() 