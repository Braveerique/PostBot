"""
PostBot Launcher - GUI wrapper for the PostBot executable
This provides a simple interface to start/stop the bot and view status
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import subprocess
import threading
import os
import sys
import time
from datetime import datetime
import queue

class PostBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PostBot - Social Media Stream Notifier")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Process management
        self.bot_process = None
        self.is_running = False
        self.output_queue = queue.Queue()
        
        self.setup_ui()
        self.check_env_file()
        
    def setup_ui(self):
        """Setup the GUI interface"""
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="🤖 PostBot Control Panel", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.status_label = ttk.Label(status_frame, text="⚫ Stopped", 
                                     font=("Arial", 12, "bold"), foreground="red")
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=(0, 10))
        
        self.start_btn = ttk.Button(button_frame, text="▶️ Start Bot", 
                                   command=self.start_bot, style="success.TButton")
        self.start_btn.grid(row=0, column=0, padx=(0, 5))
        
        self.stop_btn = ttk.Button(button_frame, text="⏹️ Stop Bot", 
                                  command=self.stop_bot, state="disabled")
        self.stop_btn.grid(row=0, column=1, padx=(5, 5))
        
        self.test_btn = ttk.Button(button_frame, text="🧪 Test", 
                                  command=self.test_bot)
        self.test_btn.grid(row=0, column=2, padx=(5, 5))
        
        self.status_btn = ttk.Button(button_frame, text="📊 Status", 
                                    command=self.check_status)
        self.status_btn.grid(row=0, column=3, padx=(5, 0))
        
        # Configuration frame
        config_frame = ttk.LabelFrame(main_frame, text="Configuration", padding="10")
        config_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(config_frame, text="Environment File:").grid(row=0, column=0, sticky=tk.W)
        
        self.env_var = tk.StringVar()
        self.env_var.set(".env")
        env_entry = ttk.Entry(config_frame, textvariable=self.env_var, width=50)
        env_entry.grid(row=0, column=1, padx=(5, 5), sticky=(tk.W, tk.E))
        
        browse_btn = ttk.Button(config_frame, text="Browse", command=self.browse_env_file)
        browse_btn.grid(row=0, column=2)
        
        # Output frame
        output_frame = ttk.LabelFrame(main_frame, text="Output Log", padding="10")
        output_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.output_text = scrolledtext.ScrolledText(output_frame, width=90, height=20, 
                                                    wrap=tk.WORD, state=tk.DISABLED)
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Clear log button
        clear_btn = ttk.Button(output_frame, text="Clear Log", command=self.clear_log)
        clear_btn.grid(row=1, column=0, sticky=tk.E, pady=(5, 0))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        config_frame.columnconfigure(1, weight=1)
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        # Start output monitoring
        self.monitor_output()
        
    def log_message(self, message, level="INFO"):
        """Add message to the output log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"[{timestamp}] {level}: {message}\n"
        
        self.output_text.configure(state=tk.NORMAL)
        self.output_text.insert(tk.END, formatted_message)
        self.output_text.see(tk.END)
        self.output_text.configure(state=tk.DISABLED)
        
    def clear_log(self):
        """Clear the output log"""
        self.output_text.configure(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.configure(state=tk.DISABLED)
        
    def check_env_file(self):
        """Check if .env file exists"""
        env_path = self.env_var.get()
        if not os.path.exists(env_path):
            self.log_message(f".env file not found: {env_path}", "WARNING")
            self.log_message("Please create .env file or browse to existing one", "WARNING")
        else:
            self.log_message(f"Found .env file: {env_path}", "INFO")
            
    def browse_env_file(self):
        """Browse for .env file"""
        filename = filedialog.askopenfilename(
            title="Select .env file",
            filetypes=[("Environment files", "*.env"), ("All files", "*.*")]
        )
        if filename:
            self.env_var.set(filename)
            self.check_env_file()
            
    def start_bot(self):
        """Start the PostBot"""
        if self.is_running:
            return
            
        env_path = self.env_var.get()
        if not os.path.exists(env_path):
            messagebox.showerror("Error", f".env file not found: {env_path}")
            return
            
        try:
            # Determine the executable path
            if getattr(sys, 'frozen', False):
                # Running as exe
                exe_path = os.path.join(os.path.dirname(sys.executable), "PostBot.exe")
                if not os.path.exists(exe_path):
                    exe_path = "postbot.exe"
            else:
                # Running as Python script
                exe_path = [sys.executable, "postbot.py"]
                
            self.log_message(f"Starting PostBot: {exe_path}", "INFO")
            
            if isinstance(exe_path, list):
                self.bot_process = subprocess.Popen(
                    exe_path,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True
                )
            else:
                self.bot_process = subprocess.Popen(
                    exe_path,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True
                )
                
            self.is_running = True
            self.start_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal")
            self.status_label.configure(text="🟢 Running", foreground="green")
            
            # Start output reader thread
            threading.Thread(target=self.read_output, daemon=True).start()
            
        except Exception as e:
            self.log_message(f"Failed to start bot: {e}", "ERROR")
            messagebox.showerror("Error", f"Failed to start PostBot: {e}")
            
    def stop_bot(self):
        """Stop the PostBot"""
        if not self.is_running:
            return
            
        try:
            if self.bot_process:
                self.bot_process.terminate()
                self.bot_process.wait(timeout=5)
                
            self.is_running = False
            self.start_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled")
            self.status_label.configure(text="⚫ Stopped", foreground="red")
            self.log_message("PostBot stopped", "INFO")
            
        except Exception as e:
            self.log_message(f"Error stopping bot: {e}", "ERROR")
            
    def test_bot(self):
        """Run bot test"""
        try:
            if getattr(sys, 'frozen', False):
                result = subprocess.run(["PostBot.exe", "test"], 
                                      capture_output=True, text=True, timeout=30)
            else:
                result = subprocess.run([sys.executable, "postbot.py", "test"], 
                                      capture_output=True, text=True, timeout=30)
                                      
            if result.returncode == 0:
                self.log_message("Test completed successfully", "SUCCESS")
                self.log_message(result.stdout, "TEST")
            else:
                self.log_message(f"Test failed: {result.stderr}", "ERROR")
                
        except Exception as e:
            self.log_message(f"Test error: {e}", "ERROR")
            
    def check_status(self):
        """Check bot status"""
        try:
            if getattr(sys, 'frozen', False):
                result = subprocess.run(["PostBot.exe", "status"], 
                                      capture_output=True, text=True, timeout=10)
            else:
                result = subprocess.run([sys.executable, "postbot.py", "status"], 
                                      capture_output=True, text=True, timeout=10)
                                      
            if result.returncode == 0:
                self.log_message("Status check completed", "INFO")
                self.log_message(result.stdout, "STATUS")
            else:
                self.log_message(f"Status check failed: {result.stderr}", "ERROR")
                
        except Exception as e:
            self.log_message(f"Status error: {e}", "ERROR")
            
    def read_output(self):
        """Read output from bot process"""
        if not self.bot_process:
            return
            
        try:
            for line in self.bot_process.stdout:
                self.output_queue.put(("BOT", line.strip()))
                
        except Exception as e:
            self.output_queue.put(("ERROR", f"Output reader error: {e}"))
            
    def monitor_output(self):
        """Monitor output queue and update GUI"""
        try:
            while True:
                level, message = self.output_queue.get_nowait()
                self.log_message(message, level)
        except queue.Empty:
            pass
            
        # Check if process is still running
        if self.is_running and self.bot_process and self.bot_process.poll() is not None:
            self.stop_bot()
            self.log_message("PostBot process ended", "WARNING")
            
        # Schedule next check
        self.root.after(100, self.monitor_output)

def main():
    """Main entry point"""
    root = tk.Tk()
    app = PostBotGUI(root)
    
    # Handle window closing
    def on_closing():
        if app.is_running:
            if messagebox.askokcancel("Quit", "PostBot is running. Stop it and quit?"):
                app.stop_bot()
                root.destroy()
        else:
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()