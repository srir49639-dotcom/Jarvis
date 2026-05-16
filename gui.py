"""
GUI Module - CustomTkinter Interface for Jarvis Assistant
Modern dark futuristic UI with neon styling
"""

import customtkinter as ctk
from tkinter import scrolledtext
import threading
from typing import Callable, Optional
from datetime import datetime

# Appearance settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class JarvisGUI:
    """Main GUI Class - Handles all UI components and layout"""
    
    def __init__(self, root: ctk.CTk, on_voice_start: Optional[Callable] = None):
        """
        Initialize the Jarvis GUI
        
        Args:
            root: The CTk root window
            on_voice_start: Callback function when voice listening starts
        """
        self.root = root
        self.on_voice_start = on_voice_start
        self.chat_history = []
        
        # Configure window
        self.root.title("Jarvis - AI Assistant")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Color scheme - Neon dark futuristic
        self.bg_color = "#0a0e27"
        self.primary_color = "#00d9ff"  # Cyan neon
        self.secondary_color = "#ff006e"  # Pink neon
        self.text_color = "#e0e0e0"
        self.button_hover = "#1a1f3a"
        
        self.root.configure(fg_color=self.bg_color)
        
        # Create main layout
        self.create_layout()
    
    def create_layout(self) -> None:
        """Create the main GUI layout with all components"""
        
        # Main container
        main_container = ctk.CTkFrame(self.root, fg_color=self.bg_color)
        main_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        # ===== TOP SECTION =====
        top_section = self.create_top_section(main_container)
        top_section.pack(fill="x", padx=0, pady=0)
        
        # ===== MAIN CONTENT AREA =====
        content_frame = ctk.CTkFrame(main_container, fg_color=self.bg_color)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        content_frame.grid_columnconfigure(0, weight=0)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Left sidebar
        sidebar = self.create_sidebar(content_frame)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)
        
        # Right chat area
        chat_area = self.create_chat_area(content_frame)
        chat_area.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        
        # ===== BOTTOM INPUT SECTION =====
        bottom_section = self.create_bottom_section(main_container)
        bottom_section.pack(fill="x", padx=10, pady=10)
    
    def create_top_section(self, parent: ctk.CTkFrame) -> ctk.CTkFrame:
        """Create the top title and status section"""
        
        top_frame = ctk.CTkFrame(parent, fg_color="#111633", height=120)
        top_frame.pack_propagate(False)
        
        # Gradient background effect with frame
        title_inner = ctk.CTkFrame(top_frame, fg_color="#111633", corner_radius=0)
        title_inner.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Title with neon effect
        title_label = ctk.CTkLabel(
            title_inner,
            text="◆ JARVIS ◆",
            text_color=self.primary_color,
            font=("Arial", 48, "bold"),
            fg_color="#111633"
        )
        title_label.pack(pady=(15, 0))
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            title_inner,
            text="AI ASSISTANT | Futuristic Voice Interface",
            text_color="#888888",
            font=("Arial", 12),
            fg_color="#111633"
        )
        subtitle_label.pack(pady=(0, 15))
        
        return top_frame
    
    def create_sidebar(self, parent: ctk.CTkFrame) -> ctk.CTkFrame:
        """Create the left sidebar with status and controls"""
        
        sidebar = ctk.CTkFrame(
            parent,
            fg_color="#111633",
            corner_radius=15,
            width=200
        )
        sidebar.pack_propagate(False)
        
        # ===== STATUS DISPLAY =====
        status_title = ctk.CTkLabel(
            sidebar,
            text="STATUS",
            text_color=self.secondary_color,
            font=("Arial", 14, "bold"),
            fg_color="#111633"
        )
        status_title.pack(pady=(20, 10), padx=15)
        
        # Status label - Dynamic
        self.status_label = ctk.CTkLabel(
            sidebar,
            text="Sleeping...",
            text_color=self.primary_color,
            font=("Arial", 11, "bold"),
            fg_color="#1a1f3a",
            corner_radius=8
        )
        self.status_label.pack(fill="x", padx=10, pady=5)
        
        # Divider line
        divider1 = ctk.CTkFrame(sidebar, fg_color="#333366", height=2)
        divider1.pack(fill="x", padx=10, pady=15)
        
        # ===== QUICK COMMANDS =====
        commands_title = ctk.CTkLabel(
            sidebar,
            text="QUICK COMMANDS",
            text_color=self.secondary_color,
            font=("Arial", 14, "bold"),
            fg_color="#111633"
        )
        commands_title.pack(pady=(10, 10), padx=15)
        
        commands = [
            ("🎤 Voice Listen", self.start_voice_listening),
            ("🌐 Open Chrome", lambda: self.queue_command("open chrome")),
            ("▶️ YouTube", lambda: self.queue_command("open youtube")),
            ("💻 VS Code", lambda: self.queue_command("open vscode")),
            ("⏰ What time?", lambda: self.queue_command("what is the time")),
        ]
        
        for cmd_text, cmd_func in commands:
            self.create_command_button(sidebar, cmd_text, cmd_func)
        
        # Divider line
        divider2 = ctk.CTkFrame(sidebar, fg_color="#333366", height=2)
        divider2.pack(fill="x", padx=10, pady=15)
        
        # ===== INFO SECTION =====
        info_title = ctk.CTkLabel(
            sidebar,
            text="INFORMATION",
            text_color=self.secondary_color,
            font=("Arial", 14, "bold"),
            fg_color="#111633"
        )
        info_title.pack(pady=(10, 10), padx=15)
        
        info_text = ctk.CTkLabel(
            sidebar,
            text="Say 'Jarvis' to wake\nup the assistant.\n\nThen give your\ncommands or ask\nquestions.\n\nStays active for\n20 seconds.",
            text_color="#999999",
            font=("Arial", 10),
            justify="left",
            fg_color="#111633"
        )
        info_text.pack(padx=15, pady=10)
        
        return sidebar
    
    def create_command_button(self, parent: ctk.CTkFrame, text: str, command: Callable) -> None:
        """Create a styled command button"""
        
        button = ctk.CTkButton(
            parent,
            text=text,
            command=command,
            font=("Arial", 11, "bold"),
            fg_color="#1a2847",
            hover_color=self.button_hover,
            text_color=self.primary_color,
            border_color=self.primary_color,
            border_width=2,
            corner_radius=8,
            height=35
        )
        button.pack(fill="x", padx=10, pady=5)
    
    def create_chat_area(self, parent: ctk.CTkFrame) -> ctk.CTkFrame:
        """Create the main chat display area"""
        
        chat_frame = ctk.CTkFrame(parent, fg_color="#111633", corner_radius=15)
        
        # Chat header
        chat_header = ctk.CTkLabel(
            chat_frame,
            text="💬 CHAT HISTORY",
            text_color=self.secondary_color,
            font=("Arial", 14, "bold"),
            fg_color="#111633"
        )
        chat_header.pack(pady=(15, 10), padx=15)
        
        # Chat display area (using Text widget for better formatting)
        chat_display_frame = ctk.CTkFrame(chat_frame, fg_color="#0a0e27", corner_radius=10)
        chat_display_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.chat_display = ctk.CTkTextbox(
            chat_display_frame,
            fg_color="#0a0e27",
            text_color=self.text_color,
            font=("Courier", 10),
            border_width=2,
            border_color=self.primary_color,
            corner_radius=8
        )
        self.chat_display.pack(fill="both", expand=True, padx=0, pady=0)
        self.chat_display.configure(state="disabled")
        
        return chat_frame
    
    def create_bottom_section(self, parent: ctk.CTkFrame) -> ctk.CTkFrame:
        """Create the bottom input and control section"""
        
        bottom_frame = ctk.CTkFrame(parent, fg_color="#111633", corner_radius=15)
        
        # Input frame
        input_frame = ctk.CTkFrame(bottom_frame, fg_color="#111633")
        input_frame.pack(fill="x", padx=15, pady=(15, 0))
        input_frame.grid_columnconfigure(0, weight=1)
        
        # Text input label
        input_label = ctk.CTkLabel(
            input_frame,
            text="TYPE A MESSAGE:",
            text_color=self.secondary_color,
            font=("Arial", 11, "bold"),
            fg_color="#111633"
        )
        input_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        # Input field
        self.input_field = ctk.CTkEntry(
            input_frame,
            placeholder_text="Ask Jarvis anything...",
            font=("Arial", 12),
            fg_color="#0a0e27",
            text_color=self.text_color,
            border_color=self.primary_color,
            border_width=2,
            corner_radius=8,
            height=40
        )
        self.input_field.grid(row=1, column=0, sticky="ew", pady=5)
        self.input_field.bind("<Return>", self.send_text_message)
        
        # Button frame
        button_frame = ctk.CTkFrame(bottom_frame, fg_color="#111633")
        button_frame.pack(fill="x", padx=15, pady=(10, 15))
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=0)
        button_frame.grid_columnconfigure(2, weight=0)
        
        # Send button
        send_button = ctk.CTkButton(
            button_frame,
            text="📤 SEND",
            command=self.send_text_message,
            font=("Arial", 11, "bold"),
            fg_color="#1a2847",
            hover_color=self.button_hover,
            text_color=self.primary_color,
            border_color=self.primary_color,
            border_width=2,
            corner_radius=8,
            height=35
        )
        send_button.grid(row=0, column=1, padx=(10, 0), sticky="ew")
        
        # Voice button
        voice_button = ctk.CTkButton(
            button_frame,
            text="🎤 LISTEN",
            command=self.start_voice_listening,
            font=("Arial", 11, "bold"),
            fg_color="#1a2847",
            hover_color="#2a3855",
            text_color=self.secondary_color,
            border_color=self.secondary_color,
            border_width=2,
            corner_radius=8,
            height=35,
            width=120
        )
        voice_button.grid(row=0, column=2, padx=(10, 0), sticky="ew")
        
        return bottom_frame
    
    def add_message_to_chat(self, sender: str, message: str) -> None:
        """
        Add a message to the chat display
        
        Args:
            sender: Who sent the message ("You", "Jarvis")
            message: The message content
        """
        # Format timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Format message with color coding
        if sender == "You":
            formatted_msg = f"[{timestamp}] YOU: {message}\n\n"
        else:
            formatted_msg = f"[{timestamp}] JARVIS: {message}\n\n"
        
        # Add to display
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", formatted_msg)
        self.chat_display.see("end")
        self.chat_display.configure(state="disabled")
        
        # Keep chat history
        self.chat_history.append((sender, message, timestamp))
    
    def update_status(self, status_text: str) -> None:
        """
        Update the status label
        
        Args:
            status_text: New status text
        """
        self.status_label.configure(text=status_text)
    
    def start_voice_listening(self) -> None:
        """Start voice listening in a separate thread"""
        if self.on_voice_start:
            threading.Thread(target=self.on_voice_start, daemon=True).start()
    
    def send_text_message(self, event=None) -> None:
        """Send a text message from the input field"""
        message = self.input_field.get().strip()
        
        if message:
            self.add_message_to_chat("You", message)
            self.input_field.delete(0, "end")
            # You can add a callback here to process the message
    
    def queue_command(self, command: str) -> None:
        """Queue a command to be processed"""
        self.add_message_to_chat("You", command)
        # Command processing would be handled by the main app
    
    def clear_chat(self) -> None:
        """Clear the chat history"""
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", "end")
        self.chat_display.configure(state="disabled")
        self.chat_history = []
