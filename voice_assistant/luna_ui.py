import tkinter as tk
from tkinter import scrolledtext
from threading import Thread
import queue


class LunaUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Luna Assistant")
        self.window.geometry("600x600")
        self.window.resizable(False, False)

        # Make the window circular

        # Center the window on the screen
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width // 2) - (600 // 2)  # 400 is the width of the circular shape
        y = (screen_height // 2) - (600 // 2)
        self.window.geometry(f"600x600+{x}+{y}")

        # Removes the default title bar
        self.window.overrideredirect(True)
        # Set transparency color
        self.window.attributes("-transparentcolor", "blue")
        # Background color for shaping
        self.window.config(bg="blue")

        # Create a circular shape
        self.canvas = tk.Canvas(self.window, width=600, height=600, bg="blue", highlightthickness=0)
        self.canvas.create_oval(0, 0, 600, 600, fill="white", outline="")
        self.canvas.pack()

        # Status Display for "Processing"
        self.status_label = tk.Label(self.window, text="Waiting for command...", font=("Arial", 10), fg="green", bg="white")
        # self.status_label.pack(pady=10)
        self.status_label.place(relx=0.5, rely=0.4, anchor="center")

        # Response Display
        self.response_label = tk.Label(self.window, text="", font=("Arial", 12), fg="black", bg="white", wraplength=500, justify="center")
        self.response_label.place(relx=0.5, rely=0.6, anchor="center")

        # Queue for thread-safe communication
        self.queue = queue.Queue()
        self.running = True

    def update_status(self, status):
        self.queue.put(("status", status))

    def update_response(self, response):
        self.queue.put(("response", response))

    def process_queue(self):
        while not self.queue.empty():
            try:
                task, message = self.queue.get_nowait()
                if task == "status":
                    # self.status_label.config(text=message)
                    self.status_label.config(text=message, fg="green")
                elif task == "response":
                    # self.response_text.delete(1.0, tk.END)
                    # self.response_text.insert(tk.END, message)
                    self.response_label.config(text=message, fg="black")
            except queue.Empty:
                pass
        if self.running:
            self.window.after(100, self.process_queue)

    def run(self):
        self.process_queue()
        self.window.mainloop()

    def stop(self):
        self.running = False
