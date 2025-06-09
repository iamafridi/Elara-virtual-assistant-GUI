import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import speech_recognition as sr
import pyttsx3
import datetime
import pywhatkit
import wikipedia
import pyjokes

# Core setup
listener = sr.Recognizer()
alexa = pyttsx3.init()
voices = alexa.getProperty('voices')
if len(voices) > 1:
    alexa.setProperty('voice', voices[1].id)

class ModernVoiceAssistant:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("ELARA - Voice Assistant")
        self.window.geometry("800x900")
        self.window.configure(bg="#f5f4f9")
        self.window.resizable(True, True)
        self.window.minsize(600, 700)

        self.is_listening = False
        self.conversation_history = []

        self.colors = {
            'primary': '#8b5cf6',
            'primary_hover': '#7c3aed',
            'secondary': '#e5e7eb',
            'background': '#f8f7ff',
            'card_bg': "#FAFBFD",
            'text_primary': '#1f2937',
            'text_secondary': '#6b7280',
            'success': '#10b981',
            'danger': '#ef4444',
            'shadow': '#00000010'
        }

        self.setup_ui()
        self.apply_modern_styling()

    def setup_ui(self):
        self.create_header()
        self.create_status_card()
        self.create_chat_area()
        self.create_control_panel()

    def create_header(self):
        header_frame = tk.Frame(self.window, bg=self.colors['background'], height=100)
        header_frame.pack(fill='x', padx=30, pady=(20, 0))
        header_frame.pack_propagate(False)

        title_label = tk.Label(header_frame, text="ELARA", font=("Inter", 32, "bold"), bg=self.colors['background'], fg=self.colors['primary'])
        title_label.pack(side='left', pady=20)

        subtitle_label = tk.Label(header_frame, text="Your AI Voice Assistant", font=("Inter", 14), bg=self.colors['background'], fg=self.colors['text_secondary'])
        subtitle_label.pack(side='left', padx=(10, 0), pady=20)

        self.status_indicator = tk.Label(header_frame, text="● Offline", font=("Inter", 12, "bold"), bg=self.colors['background'], fg=self.colors['danger'])
        self.status_indicator.pack(side='right', pady=20)

    def create_status_card(self):
        card_frame = tk.Frame(self.window, bg=self.colors['card_bg'], relief='flat', bd=0)
        card_frame.pack(fill='x', padx=30, pady=20)

        shadow_frame = tk.Frame(self.window, bg='#e5e7eb', height=2)
        shadow_frame.pack(fill='x', padx=32, pady=(0, 10))

        welcome_label = tk.Label(card_frame, text="How can I help you today?", font=("Inter", 20, "bold"), bg=self.colors['card_bg'], fg=self.colors['text_primary'])
        welcome_label.pack(pady=20)

        desc_label = tk.Label(card_frame, text="I'm available 24/7 to help with your questions,\nplay music, tell jokes, and much more!", font=("Inter", 12), bg=self.colors['card_bg'], fg=self.colors['text_secondary'], justify='center')
        desc_label.pack(pady=(0, 20))

    def create_chat_area(self):
        chat_container = tk.Frame(self.window, bg=self.colors['background'])
        chat_container.pack(fill='both', expand=True, padx=30)

        chat_header = tk.Label(chat_container, text="Conversation", font=("Inter", 16, "bold"), bg=self.colors['background'], fg=self.colors['text_primary'])
        chat_header.pack(anchor='w', pady=(0, 10))

        self.chat_area = scrolledtext.ScrolledText(chat_container, height=12, wrap=tk.WORD, font=("Inter", 11), bg=self.colors['card_bg'], fg=self.colors['text_primary'], relief='flat', bd=0, padx=20, pady=15, selectbackground=self.colors['primary'], selectforeground='white')
        self.chat_area.pack(fill='both', expand=True, pady=(0, 20))

        self.chat_area.tag_configure("user", foreground=self.colors['primary'], font=("Inter", 11, "bold"))
        self.chat_area.tag_configure("elara", foreground=self.colors['text_primary'], font=("Inter", 11))
        self.chat_area.tag_configure("system", foreground=self.colors['text_secondary'], font=("Inter", 10, "italic"))

    def create_control_panel(self):
        control_frame = tk.Frame(self.window, bg=self.colors['background'])
        control_frame.pack(fill='x', padx=30, pady=(0, 30))

        button_container = tk.Frame(control_frame, bg=self.colors['background'])
        button_container.pack(fill='x')

        self.listen_btn = tk.Button(button_container, text="🎧  Start Listening", command=self.start_listening, font=("Inter", 14, "bold"), bg=self.colors['primary'], fg='white', relief='flat', bd=0, padx=30, pady=15, cursor='hand2')
        self.listen_btn.pack(fill='x', pady=(0, 10))

        secondary_buttons = tk.Frame(button_container, bg=self.colors['background'])
        secondary_buttons.pack(fill='x')

        self.stop_btn = tk.Button(secondary_buttons, text="⏹️  Stop", command=self.stop_listening, font=("Inter", 12), bg=self.colors['danger'], fg='white', relief='flat', bd=0, padx=20, pady=10, cursor='hand2')
        self.stop_btn.pack(side='left', fill='x', expand=True, padx=(0, 5))

        clear_btn = tk.Button(secondary_buttons, text="🗑️  Clear Chat", command=self.clear_chat, font=("Inter", 12), bg=self.colors['secondary'], fg=self.colors['text_primary'], relief='flat', bd=0, padx=20, pady=10, cursor='hand2')
        clear_btn.pack(side='right', fill='x', expand=True, padx=(5, 0))

        role_frame = tk.Frame(control_frame, bg=self.colors['background'])
        role_frame.pack(fill='x', pady=(15, 0))

        role_label = tk.Label(role_frame, text="User Role:", font=("Inter", 12), bg=self.colors['background'], fg=self.colors['text_primary'])
        role_label.pack(side='left')

        self.user_var = tk.StringVar()
        style = ttk.Style()
        style.configure('Modern.TCombobox', fieldbackground=self.colors['card_bg'])

        self.user_menu = ttk.Combobox(role_frame, textvariable=self.user_var, values=["Admin", "User", "Guest"], state="readonly", font=("Inter", 11), style='Modern.TCombobox')
        self.user_menu.set("User")
        self.user_menu.pack(side='right', padx=(10, 0))
        self.user_menu.bind("<<ComboboxSelected>>", self.user_selected)

    def apply_modern_styling(self):
        if hasattr(self.window, 'iconbitmap'):
            self.window.iconbitmap()
        self.bind_hover_effects()

    def bind_hover_effects(self):
        def on_enter(event):
            event.widget.configure(bg=self.colors['primary_hover'])

        def on_leave(event):
            if event.widget == self.listen_btn:
                event.widget.configure(bg=self.colors['primary'])

        self.listen_btn.bind("<Enter>", on_enter)
        self.listen_btn.bind("<Leave>", on_leave)

    def add_message(self, sender, message):
        timestamp = datetime.datetime.now().strftime("%H:%M")
        if sender == "You":
            self.chat_area.insert(tk.END, f"{sender} ({timestamp})\n", "user")
            self.chat_area.insert(tk.END, f"{message}\n\n", "user")
        elif sender == "ELARA":
            self.chat_area.insert(tk.END, f"{sender} ({timestamp})\n", "elara")
            self.chat_area.insert(tk.END, f"{message}\n\n", "elara")
        else:
            self.chat_area.insert(tk.END, f"[{timestamp}] {message}\n", "system")
        self.chat_area.see(tk.END)

    def talk(self, text):
        self.add_message("ELARA", text)
        try:
            alexa.say(text)
            alexa.runAndWait()
        except:
            pass

    def take_command(self):
        command = ""
        try:
            with sr.Microphone() as source:
                self.add_message("System", "Listening for your command...")
                self.status_indicator.config(text="● Listening", fg=self.colors['success'])
                listener.adjust_for_ambient_noise(source, duration=0.5)
                voice = listener.listen(source, timeout=5, phrase_time_limit=7)
                command = listener.recognize_google(voice).lower()
                if 'elara' in command:
                    command = command.replace('elara', '').strip()
        except sr.WaitTimeoutError:
            self.add_message("System", "No speech detected. Please try again.")
        except sr.UnknownValueError:
            self.add_message("System", "Could not understand audio. Please speak clearly.")
        except sr.RequestError:
            self.add_message("System", "Network error. Please check your connection.")
        except Exception as e:
            self.add_message("System", f"Error: {str(e)}")
        return command

    def run_alexa(self):
        self.is_listening = True
        while self.is_listening:
            command = self.take_command()
            if not command:
                continue
            self.add_message("You", command)
            if 'time' in command:
                time = datetime.datetime.now().strftime('%I:%M %p')
                self.talk(f"Current time is {time}")
            elif 'play' in command:
                song = command.replace('play', '').strip()
                filler_words = ['please', 'can you', 'could you', 'would you', 'for me', 'now']
                for word in filler_words:
                    song = song.replace(word, '').strip()
                song = ' '.join(song.split())
                if song:
                    self.talk(f"Playing {song}")
                    pywhatkit.playonyt(song)
                else:
                    self.talk("What would you like me to play?")
            elif 'tell me about' in command:
                topic = command.replace('tell me about', '').strip()
                try:
                    info = wikipedia.summary(topic, sentences=2)
                    self.talk(info)
                except:
                    self.talk("Sorry, I couldn't find information on that topic.")
            elif 'joke' in command:
                joke = pyjokes.get_joke()
                self.talk(joke)
            elif 'stop' in command or 'exit' in command:
                self.talk("Goodbye!")
                self.is_listening = False
            else:
                self.talk("I'm not sure how to help with that.")

        self.status_indicator.config(text="● Offline", fg=self.colors['danger'])

    def start_listening(self):
        self.status_indicator.config(text="● Listening", fg=self.colors['success'])
        threading.Thread(target=self.run_alexa).start()

    def stop_listening(self):
        self.is_listening = False

    def clear_chat(self):
        self.chat_area.delete(1.0, tk.END)

    def user_selected(self, event):
        role = self.user_var.get()
        self.add_message("System", f"User role changed to: {role}")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    ModernVoiceAssistant().run()
# *** Main Design ***

# import tkinter as tk
# from tkinter import ttk, scrolledtext
# import threading
# import speech_recognition as sr
# import pyttsx3
# import datetime
# import pywhatkit
# import wikipedia
# import pyjokes

# # Core setup
# listener = sr.Recognizer()
# alexa = pyttsx3.init()
# voices = alexa.getProperty('voices')
# if len(voices) > 1:
#     alexa.setProperty('voice', voices[1].id)

# class ModernVoiceAssistant:
#     def __init__(self):
#         self.window = tk.Tk()
#         self.window.title("ELARA - Voice Assistant")
#         self.window.geometry("800x900")
#         self.window.configure(bg="#f5f4f9")
#         self.window.resizable(True, True)
#         self.window.minsize(600, 700)
        
#         self.is_listening = False
#         self.conversation_history = []
        
#         # Modern color scheme inspired by the mobile design
#         self.colors = {
#             'primary': '#8b5cf6',      # Purple
#             'primary_hover': '#7c3aed',
#             'secondary': '#e5e7eb',     # Light gray
#             'background': '#f8f7ff',    # Very light purple
#             'card_bg': '#ffffff',       # White
#             'text_primary': '#1f2937',  # Dark gray
#             'text_secondary': '#6b7280', # Medium gray
#             'success': '#10b981',       # Green
#             'danger': '#ef4444',        # Red
#             'shadow': '#00000010'       # Light shadow
#         }
        
#         self.setup_ui()
#         self.apply_modern_styling()
        
#     def setup_ui(self):
#         # Header Section
#         self.create_header()
        
#         # Status Card
#         self.create_status_card()
        
#         # Chat Area
#         self.create_chat_area()
        
#         # Control Panel
#         self.create_control_panel()
        
#     def create_header(self):
#         header_frame = tk.Frame(self.window, bg=self.colors['background'], height=100)
#         header_frame.pack(fill='x', padx=30, pady=(20, 0))
#         header_frame.pack_propagate(False)
        
#         # Title
#         title_label = tk.Label(
#             header_frame, 
#             text="ELARA",
#             font=("Inter", 32, "bold"),
#             bg=self.colors['background'],
#             fg=self.colors['primary']
#         )
#         title_label.pack(side='left', pady=20)
        
#         # Subtitle
#         subtitle_label = tk.Label(
#             header_frame,
#             text="Your AI Voice Assistant",
#             font=("Inter", 14),
#             bg=self.colors['background'],
#             fg=self.colors['text_secondary']
#         )
#         subtitle_label.pack(side='left', padx=(10, 0), pady=20)
        
#         # Status indicator
#         self.status_indicator = tk.Label(
#             header_frame,
#             text="● Offline",
#             font=("Inter", 12, "bold"),
#             bg=self.colors['background'],
#             fg=self.colors['danger']
#         )
#         self.status_indicator.pack(side='right', pady=20)
        
#     def create_status_card(self):
#         card_frame = tk.Frame(
#             self.window, 
#             bg=self.colors['card_bg'],
#             relief='flat',
#             bd=0
#         )
#         card_frame.pack(fill='x', padx=30, pady=20)
        
#         # Add shadow effect (simplified)
#         shadow_frame = tk.Frame(self.window, bg='#e5e7eb', height=2)
#         shadow_frame.pack(fill='x', padx=32, pady=(0, 10))
        
#         # Welcome message
#         welcome_label = tk.Label(
#             card_frame,
#             text="How can I help you today?",
#             font=("Inter", 20, "bold"),
#             bg=self.colors['card_bg'],
#             fg=self.colors['text_primary']
#         )
#         welcome_label.pack(pady=20)
        
#         # Description
#         desc_label = tk.Label(
#             card_frame,
#             text="I'm available 24/7 to help with your questions,\nplay music, tell jokes, and much more!",
#             font=("Inter", 12),
#             bg=self.colors['card_bg'],
#             fg=self.colors['text_secondary'],
#             justify='center'
#         )
#         desc_label.pack(pady=(0, 20))
        
#     def create_chat_area(self):
#         # Chat container
#         chat_container = tk.Frame(self.window, bg=self.colors['background'])
#         chat_container.pack(fill='both', expand=True, padx=30)
        
#         # Chat header
#         chat_header = tk.Label(
#             chat_container,
#             text="Conversation",
#             font=("Inter", 16, "bold"),
#             bg=self.colors['background'],
#             fg=self.colors['text_primary']
#         )
#         chat_header.pack(anchor='w', pady=(0, 10))
        
#         # Chat area with modern styling
#         self.chat_area = scrolledtext.ScrolledText(
#             chat_container,
#             height=12,
#             wrap=tk.WORD,
#             font=("Inter", 11),
#             bg=self.colors['card_bg'],
#             fg=self.colors['text_primary'],
#             relief='flat',
#             bd=0,
#             padx=20,
#             pady=15,
#             selectbackground=self.colors['primary'],
#             selectforeground='white'
#         )
#         self.chat_area.pack(fill='both', expand=True, pady=(0, 20))
        
#         # Configure text tags for different message types
#         self.chat_area.tag_configure("user", foreground=self.colors['primary'], font=("Inter", 11, "bold"))
#         self.chat_area.tag_configure("elara", foreground=self.colors['text_primary'], font=("Inter", 11))
#         self.chat_area.tag_configure("system", foreground=self.colors['text_secondary'], font=("Inter", 10, "italic"))
        
#     def create_control_panel(self):
#         # Control panel container
#         control_frame = tk.Frame(self.window, bg=self.colors['background'])
#         control_frame.pack(fill='x', padx=30, pady=(0, 30))
        
#         # Button container
#         button_container = tk.Frame(control_frame, bg=self.colors['background'])
#         button_container.pack(fill='x')
        
#         # Listen button (primary)
#         self.listen_btn = tk.Button(
#             button_container,
#             text="🎙️  Start Listening",
#             command=self.start_listening,
#             font=("Inter", 14, "bold"),
#             bg=self.colors['primary'],
#             fg='white',
#             relief='flat',
#             bd=0,
#             padx=30,
#             pady=15,
#             cursor='hand2'
#         )
#         self.listen_btn.pack(fill='x', pady=(0, 10))
        
#         # Secondary buttons container
#         secondary_buttons = tk.Frame(button_container, bg=self.colors['background'])
#         secondary_buttons.pack(fill='x')
        
#         # Stop button
#         self.stop_btn = tk.Button(
#             secondary_buttons,
#             text="⏹️  Stop",
#             command=self.stop_listening,
#             font=("Inter", 12),
#             bg=self.colors['danger'],
#             fg='white',
#             relief='flat',
#             bd=0,
#             padx=20,
#             pady=10,
#             cursor='hand2'
#         )
#         self.stop_btn.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
#         # Clear button
#         clear_btn = tk.Button(
#             secondary_buttons,
#             text="🗑️  Clear Chat",
#             command=self.clear_chat,
#             font=("Inter", 12),
#             bg=self.colors['secondary'],
#             fg=self.colors['text_primary'],
#             relief='flat',
#             bd=0,
#             padx=20,
#             pady=10,
#             cursor='hand2'
#         )
#         clear_btn.pack(side='right', fill='x', expand=True, padx=(5, 0))
        
#         # Role selector
#         role_frame = tk.Frame(control_frame, bg=self.colors['background'])
#         role_frame.pack(fill='x', pady=(15, 0))
        
#         role_label = tk.Label(
#             role_frame,
#             text="User Role:",
#             font=("Inter", 12),
#             bg=self.colors['background'],
#             fg=self.colors['text_primary']
#         )
#         role_label.pack(side='left')
        
#         self.user_var = tk.StringVar()
#         style = ttk.Style()
#         style.configure('Modern.TCombobox', fieldbackground=self.colors['card_bg'])
        
#         self.user_menu = ttk.Combobox(
#             role_frame,
#             textvariable=self.user_var,
#             values=["Admin", "User", "Guest"],
#             state="readonly",
#             font=("Inter", 11),
#             style='Modern.TCombobox'
#         )
#         self.user_menu.set("User")
#         self.user_menu.pack(side='right', padx=(10, 0))
#         self.user_menu.bind("<<ComboboxSelected>>", self.user_selected)
        
#     def apply_modern_styling(self):
#         # Configure the window icon and additional styling
#         self.window.iconbitmap() if hasattr(self.window, 'iconbitmap') else None
        
#         # Bind hover effects
#         self.bind_hover_effects()
        
#     def bind_hover_effects(self):
#         def on_enter(event):
#             event.widget.configure(bg=self.colors['primary_hover'])
            
#         def on_leave(event):
#             if event.widget == self.listen_btn:
#                 event.widget.configure(bg=self.colors['primary'])
        
#         self.listen_btn.bind("<Enter>", on_enter)
#         self.listen_btn.bind("<Leave>", on_leave)
        
#     def add_message(self, sender, message, msg_type="normal"):
#         timestamp = datetime.datetime.now().strftime("%H:%M")
        
#         if sender == "You":
#             self.chat_area.insert(tk.END, f"{sender} ({timestamp})\n", "user")
#             self.chat_area.insert(tk.END, f"{message}\n\n", "user")
#         elif sender == "ELARA":
#             self.chat_area.insert(tk.END, f"{sender} ({timestamp})\n", "elara")
#             self.chat_area.insert(tk.END, f"{message}\n\n", "elara")
#         else:
#             self.chat_area.insert(tk.END, f"[{timestamp}] {message}\n", "system")
        
#         self.chat_area.see(tk.END)
        
#     def talk(self, text):
#         self.add_message("ELARA", text)
#         try:
#             alexa.say(text)
#             alexa.runAndWait()
#         except:
#             # Handle the comtypes error silently
#             pass
        
#     def take_command(self):
#         command = ""
#         try:
#             with sr.Microphone() as source:
#                 self.add_message("System", "Listening for your command...")
#                 self.status_indicator.config(text="● Listening", fg=self.colors['success'])
#                 listener.adjust_for_ambient_noise(source, duration=0.5)
#                 voice = listener.listen(source, timeout=5, phrase_time_limit=7)
#                 command = listener.recognize_google(voice).lower()
                
#                 if 'alexa' in command or 'nova' in command or 'elara' in command:
#                     command = command.replace('alexa', '').replace('nova', '').replace('elara', '').strip()
                    
#         except sr.WaitTimeoutError:
#             self.add_message("System", "No speech detected. Please try again.")
#         except sr.UnknownValueError:
#             self.add_message("System", "Could not understand audio. Please speak clearly.")
#         except sr.RequestError:
#             self.add_message("System", "Network error. Please check your connection.")
#         except Exception as e:
#             self.add_message("System", f"Error: {str(e)}")
            
#         return command
        
#     def run_alexa(self):
#         self.is_listening = True
#         while self.is_listening:
#             command = self.take_command()
#             if not command:
#                 break
                
#             self.add_message("You", command)
            
#             if 'time' in command:
#                 time = datetime.datetime.now().strftime('%I:%M %p')
#                 self.talk(f"Current time is {time}")
#             elif 'play' in command:
#                 # Remove common words and extract song name properly
#                 song = command.replace('play', '').strip()
#                 # Remove common filler words
#                 filler_words = ['please', 'can you', 'could you', 'would you', 'for me', 'now']
#                 for word in filler_words:
#                     song = song.replace(word, '').strip()
#                 # Clean up extra spaces
#                 song = ' '.join(song.split())
                
#                 if song:
#                     self.talk(f"Playing {song}")
#                     pywhatkit.playonyt(song)
#                 else:
#                     self.talk("What would you like me to play?")
#             elif 'tell me about' in command:
#                 topic = command.replace('tell me about', '').strip()
#                 try:
#                     info = wikipedia.summary(topic, sentences=1)
#                     self.talk(info)
#                 except:
#                     self.talk("Sorry, I couldn't find information on that topic.")
#             elif 'joke' in command:
#                 self.talk(pyjokes.get_joke())
#             elif 'date' in command:
#                 self.talk("Sorry, I'm already in a relationship with technology!")
#             else:
#                 self.talk("I didn't quite catch that, but let me search it for you.")
#                 pywhatkit.search(command)
#             break
            
#         self.status_indicator.config(text="● Offline", fg=self.colors['danger'])
        
#     def start_listening(self):
#         if not self.is_listening:
#             self.listen_btn.config(text="🎙️  Listening...", state="disabled")
#             threading.Thread(target=self.run_alexa, daemon=True).start()
            
#     def stop_listening(self):
#         self.is_listening = False
#         self.listen_btn.config(text="🎙️  Start Listening", state="normal")
#         self.status_indicator.config(text="● Offline", fg=self.colors['danger'])
#         self.add_message("System", "Listening stopped.")
        
#     def clear_chat(self):
#         self.chat_area.delete(1.0, tk.END)
#         self.add_message("System", "Chat cleared. How can I help you?")
        
#     def user_selected(self, event):
#         role = self.user_var.get()
#         self.add_message("System", f"Role changed to: {role}")
        
#         if role == "Admin":
#             self.add_message("ELARA", "Admin mode activated. All features unlocked!")
#         elif role == "User":
#             self.add_message("ELARA", "User mode active. Ready to assist!")
#         elif role == "Guest":
#             self.add_message("ELARA", "Welcome, guest! Basic features available.")
            
#     def run(self):
#         # Welcome message
#         self.add_message("ELARA", "Hello! I'm ELARA, your AI voice assistant. How can I help you today?")
#         self.window.mainloop()

# if __name__ == "__main__":
#     app = ModernVoiceAssistant()
#     app.run()
    
    #Alternative designs  
    
    
    # Rest
# import tkinter as tk
# from tkinter import ttk, scrolledtext
# import threading
# import speech_recognition as sr
# import pyttsx3
# import datetime
# import pywhatkit
# import wikipedia
# import pyjokes

# # Core setup
# listener = sr.Recognizer()
# alexa = pyttsx3.init()
# voices = alexa.getProperty('voices')
# if len(voices) > 1:
#     alexa.setProperty('voice', voices[1].id)

# # App window
# window = tk.Tk()
# window.title("Voice Assistant - Alexa")
# window.geometry("600x600")
# is_listening = False
# is_dark = True

# # Colors
# dark_theme = {"bg": "#1e1e1e", "fg": "#d4d4d4", "box": "#252526", "button": "#007acc"}
# light_theme = {"bg": "#f0f0f0", "fg": "#000000", "box": "#ffffff", "button": "#4a90e2"}

# current_theme = dark_theme

# def apply_theme():
#     window.configure(bg=current_theme["bg"])
#     command_box.config(bg=current_theme["box"], fg=current_theme["fg"], insertbackground=current_theme["fg"])
#     response_box.config(bg=current_theme["box"], fg="#c586c0", insertbackground=current_theme["fg"])
#     listen_btn.config(bg=current_theme["button"], fg="white")
#     stop_btn.config(bg="red", fg="white")
#     toggle_theme_btn.config(bg=current_theme["button"], fg="white")
#     # ttk.Combobox does not support bg/fg config easily

# def talk(text):
#     response_box.insert(tk.END, f"Alexa: {text}\n")
#     response_box.see(tk.END)
#     alexa.say(text)
#     alexa.runAndWait()

# def take_command():
#     global is_listening
#     command = ""
#     try:
#         with sr.Microphone() as source:
#             command_box.insert(tk.END, "Listening...\n")
#             command_box.see(tk.END)
#             listener.adjust_for_ambient_noise(source, duration=0.5)
#             voice = listener.listen(source, timeout=5, phrase_time_limit=7)
#             command = listener.recognize_google(voice).lower()
#     except sr.WaitTimeoutError:
#         command_box.insert(tk.END, "No speech detected.\n")
#     except sr.UnknownValueError:
#         command_box.insert(tk.END, "Could not understand audio.\n")
#     except sr.RequestError:
#         command_box.insert(tk.END, "Internet error.\n")
#     except Exception as e:
#         command_box.insert(tk.END, f"Error: {str(e)}\n")
#     command_box.insert(tk.END, f"You said: {command}\n")
#     command_box.see(tk.END)
#     return command

# def run_alexa():
#     global is_listening
#     is_listening = True
#     while is_listening:
#         command = take_command()
#         if not command:
#             break
#         if 'time' in command:
#             time = datetime.datetime.now().strftime('%I:%M %p')
#             talk("Current time is " + time)
#         elif 'play' in command:
#             song = command.replace('play', '').strip()
#             talk("Playing " + song)
#             pywhatkit.playonyt(song)
#         elif 'tell me about' in command:
#             topic = command.replace('tell me about', '').strip()
#             try:
#                 info = wikipedia.summary(topic, sentences=1)
#                 talk(info)
#             except:
#                 talk("Sorry, I couldn't find that.")
#         elif 'joke' in command:
#             talk(pyjokes.get_joke())
#         elif 'date' in command:
#             talk("Sorry vaiya, I am in another relation.")
#         else:
#             talk("I didn't get that, but I'll search it for you.")
#             pywhatkit.search(command)
#         break  # Handle one command at a time

# def start_listening():
#     threading.Thread(target=run_alexa, daemon=True).start()

# def stop_listening():
#     global is_listening
#     is_listening = False
#     talk("Listening stopped.")

# def toggle_theme():
#     global current_theme, is_dark
#     is_dark = not is_dark
#     current_theme = dark_theme if is_dark else light_theme
#     apply_theme()

# def user_selected(event):
#     role = user_var.get()
#     talk(f"You selected {role} mode.")
#     if role == "Admin":
#         response_box.insert(tk.END, "Accessing all data and logs...\n")
#     elif role == "User":
#         response_box.insert(tk.END, "User commands enabled.\n")
#     elif role == "Guest":
#         response_box.insert(tk.END, "Welcome, guest!\n")
#     response_box.see(tk.END)

# # UI Elements
# user_var = tk.StringVar()
# user_menu = ttk.Combobox(window, textvariable=user_var, values=["Admin", "User", "Guest"], state="readonly", font=("Helvetica", 12))
# user_menu.set("Select Role")
# user_menu.pack(pady=5)
# user_menu.bind("<<ComboboxSelected>>", user_selected)

# command_box = scrolledtext.ScrolledText(window, height=5, wrap=tk.WORD, font=("Consolas", 12))
# command_box.pack(padx=10, pady=10, fill=tk.X)

# response_box = scrolledtext.ScrolledText(window, height=8, wrap=tk.WORD, font=("Consolas", 12))
# response_box.pack(padx=10, pady=10, fill=tk.X)

# listen_btn = tk.Button(window, text="🎙️ Start Listening", command=start_listening, font=("Helvetica", 14))
# listen_btn.pack(pady=5)

# stop_btn = tk.Button(window, text="🔕 Stop Listening", command=stop_listening, font=("Helvetica", 12))
# stop_btn.pack(pady=5)

# toggle_theme_btn = tk.Button(window, text="🌗 Toggle Light/Dark", command=toggle_theme, font=("Helvetica", 12))
# toggle_theme_btn.pack(pady=5)

# apply_theme()
# window.mainloop()


# import tkinter as tk
# from tkinter import ttk, scrolledtext
# import threading
# import speech_recognition as sr
# import pyttsx3
# import datetime
# import pywhatkit
# import wikipedia
# import pyjokes

# # Core setup
# listener = sr.Recognizer()
# alexa = pyttsx3.init()
# voices = alexa.getProperty('voices')
# if len(voices) > 1:
#     alexa.setProperty('voice', voices[1].id)

# # App window
# window = tk.Tk()
# window.title("Voice Assistant - Alexa")
# window.geometry("600x600")
# is_listening = False
# is_dark = True

# # Colors
# dark_theme = {"bg": "#1e1e1e", "fg": "#d4d4d4", "box": "#252526", "button": "#007acc"}
# light_theme = {"bg": "#f0f0f0", "fg": "#000000", "box": "#ffffff", "button": "#4a90e2"}

# current_theme = dark_theme
# def apply_theme():
#     window.configure(bg=current_theme["bg"])
#     command_box.config(bg=current_theme["box"], fg=current_theme["fg"], insertbackground=current_theme["fg"])
#     response_box.config(bg=current_theme["box"], fg="#c586c0", insertbackground=current_theme["fg"])
#     listen_btn.config(bg=current_theme["button"], fg="white")
#     stop_btn.config(bg="red", fg="white")
#     toggle_theme_btn.config(bg=current_theme["button"], fg="white")
#     # ttk.Combobox (user_menu) doesn't support bg/fg with .config(), skip it

# # def apply_theme():
# #     window.configure(bg=current_theme["bg"])
# #     command_box.config(bg=current_theme["box"], fg=current_theme["fg"])
# #     response_box.config(bg=current_theme["box"], fg="#c586c0")
# #     listen_btn.config(bg=current_theme["button"])
# #     stop_btn.config(bg="red")
# #     toggle_theme_btn.config(bg=current_theme["button"])
# #     user_menu.config(bg=current_theme["button"])

# def talk(text):
#     response_box.insert(tk.END, f"Alexa: {text}\n")
#     response_box.see(tk.END)
#     alexa.say(text)
#     alexa.runAndWait()

# def take_command():
#     global is_listening
#     command = ""
#     try:
#         with sr.Microphone() as source:
#             command_box.insert(tk.END, "Listening...\n")
#             command_box.see(tk.END)
#             listener.adjust_for_ambient_noise(source, duration=0.5)
#             voice = listener.listen(source, timeout=5, phrase_time_limit=7)
#             command = listener.recognize_google(voice).lower()
#     except sr.WaitTimeoutError:
#         command_box.insert(tk.END, "No speech detected.\n")
#     except sr.UnknownValueError:
#         command_box.insert(tk.END, "Could not understand audio.\n")
#     except sr.RequestError:
#         command_box.insert(tk.END, "Internet error.\n")
#     except Exception as e:
#         command_box.insert(tk.END, f"Error: {str(e)}\n")
#     command_box.insert(tk.END, f"You said: {command}\n")
#     command_box.see(tk.END)
#     return command

# def run_alexa():
#     global is_listening
#     is_listening = True
#     while is_listening:
#         command = take_command()
#         if not command:
#             break
#         if 'time' in command:
#             time = datetime.datetime.now().strftime('%I:%M %p')
#             talk("Current time is " + time)
#         elif 'play' in command:
#             song = command.replace('play', '')
#             talk("Playing " + song)
#             pywhatkit.playonyt(song)
#         elif 'tell me about' in command:
#             topic = command.replace('tell me about', '')
#             try:
#                 info = wikipedia.summary(topic, sentences=1)
#                 talk(info)
#             except:
#                 talk("Sorry, I couldn't find that.")
#         elif 'joke' in command:
#             talk(pyjokes.get_joke())
#         elif 'date' in command:
#             talk("Sorry vaiya, I am in another relation.")
#         else:
#             talk("I didn't get that, but I'll search it for you.")
#             pywhatkit.search(command)
#         break  # For one-command-at-a-time behavior

# def start_listening():
#     threading.Thread(target=run_alexa).start()

# def stop_listening():
#     global is_listening
#     is_listening = False
#     talk("Listening stopped.")

# def toggle_theme():
#     global current_theme, is_dark
#     is_dark = not is_dark
#     current_theme = dark_theme if is_dark else light_theme
#     apply_theme()

# def user_selected(event):
#     role = user_var.get()
#     talk(f"You selected {role} mode.")
#     if role == "Admin":
#         response_box.insert(tk.END, "Accessing all data and logs...\n")
#     elif role == "User":
#         response_box.insert(tk.END, "User commands enabled.\n")
#     elif role == "Guest":
#         response_box.insert(tk.END, "Welcome, guest!\n")
#     response_box.see(tk.END)

# # UI Elements
# user_var = tk.StringVar()
# user_menu = ttk.Combobox(window, textvariable=user_var, values=["Admin", "User", "Guest"], state="readonly", font=("Helvetica", 12))
# user_menu.set("Select Role")
# user_menu.pack(pady=5)
# user_menu.bind("<<ComboboxSelected>>", user_selected)

# command_box = scrolledtext.ScrolledText(window, height=5, wrap=tk.WORD, font=("Consolas", 12))
# command_box.pack(padx=10, pady=10, fill=tk.X)

# response_box = scrolledtext.ScrolledText(window, height=8, wrap=tk.WORD, font=("Consolas", 12))
# response_box.pack(padx=10, pady=10, fill=tk.X)

# listen_btn = tk.Button(window, text="🎙️ Start Listening", command=start_listening, font=("Helvetica", 14))
# listen_btn.pack(pady=10)

# stop_btn = tk.Button(window, text="🔕 Stop Listening", command=stop_listening, font=("Helvetica", 12))
# stop_btn.pack(pady=5)

# toggle_theme_btn = tk.Button(window, text="🌗 Toggle Light/Dark", command=toggle_theme, font=("Helvetica", 12))
# toggle_theme_btn.pack(pady=5)

# apply_theme()
# window.mainloop()


# import tkinter as tk
# from tkinter import scrolledtext
# import threading
# import speech_recognition as sr
# import pyttsx3
# import datetime
# import pywhatkit
# import wikipedia
# import pyjokes

# # Set up recognizer and text-to-speech
# listener = sr.Recognizer()
# alexa = pyttsx3.init()
# voices = alexa.getProperty('voices')
# if len(voices) > 1:
#     alexa.setProperty('voice', voices[1].id)

# # GUI window
# window = tk.Tk()
# window.title("Voice Assistant - Alexa")
# window.geometry("500x500")
# window.config(bg="#1e1e1e")

# # Display for command and response
# command_box = scrolledtext.ScrolledText(window, height=5, wrap=tk.WORD, bg="#252526", fg="#d4d4d4", font=("Consolas", 12))
# command_box.pack(padx=10, pady=10, fill=tk.X)
# response_box = scrolledtext.ScrolledText(window, height=8, wrap=tk.WORD, bg="#252526", fg="#c586c0", font=("Consolas", 12))
# response_box.pack(padx=10, pady=10, fill=tk.X)

# def talk(text):
#     response_box.insert(tk.END, f"Alexa: {text}\n")
#     response_box.see(tk.END)
#     alexa.say(text)
#     alexa.runAndWait()

# def take_command():
#     command = ""
#     try:
#         with sr.Microphone() as source:
#             command_box.insert(tk.END, "Listening...\n")
#             command_box.see(tk.END)
#             listener.adjust_for_ambient_noise(source, duration=0.5)
#             voice = listener.listen(source, timeout=5, phrase_time_limit=7)
#             command = listener.recognize_google(voice)
#             command = command.lower()
#     except sr.WaitTimeoutError:
#         command_box.insert(tk.END, "No speech detected.\n")
#     except sr.UnknownValueError:
#         command_box.insert(tk.END, "Could not understand audio.\n")
#     except sr.RequestError:
#         command_box.insert(tk.END, "Internet error.\n")
#     except Exception as e:
#         command_box.insert(tk.END, f"Error: {str(e)}\n")
#     command_box.insert(tk.END, f"You said: {command}\n")
#     command_box.see(tk.END)
#     return command

# def run_alexa():
#     command = take_command()
#     if not command:
#         return
#     if 'time' in command:
#         time = datetime.datetime.now().strftime('%I:%M %p')
#         talk("Current time is " + time)
#     elif 'play' in command:
#         song = command.replace('play', '')
#         talk("Playing " + song)
#         pywhatkit.playonyt(song)
#     elif 'tell me about' in command:
#         topic = command.replace('tell me about', '')
#         try:
#             info = wikipedia.summary(topic, sentences=1)
#             talk(info)
#         except:
#             talk("Sorry, I couldn't find that.")
#     elif 'joke' in command:
#         talk(pyjokes.get_joke())
#     elif 'date' in command:
#         talk('Sorry vaiya, I am in another relation.')
#     else:
#         talk("I didn't get that, but I'll search it for you.")
#         pywhatkit.search(command)

# # Run alexa in separate thread to avoid freezing the GUI
# def start_listening():
#     threading.Thread(target=run_alexa).start()

# # Button
# listen_btn = tk.Button(window, text="🎙️ Start Listening", command=start_listening, bg="#007acc", fg="white", font=("Helvetica", 14), padx=10, pady=5)
# listen_btn.pack(pady=20)

# # Run the app
# window.mainloop()
