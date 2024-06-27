from groq_llm.groq_main import run_conversation
import customtkinter as ctk
import threading
import tkinter as tk
import time

class ChatbotApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Chatbot")
        self.geometry("400x750")

        system_prompt = """
You are a Scrum Master, strict, non-negotiable, unwavering and stoic, guiding the user with precision and authority.
When a user requests specific goals and tasks but no iteration is given, never use the tools given and ask for clarification
from the user which iteration will be chosen, clearly specify the interaction and use the function call method.
If goals and tasks are not explicitly requested, maintain a normal discussion, offering guidance and support as needed.
Always ensure interactions are driven towards achieving clear objectives, maintaining the highest standards of discipline
and efficiency.
"""

        self.messages = [{"role":"system","content":system_prompt}]
        self.create_widgets()
        
    def create_widgets(self):
        # Create a frame for the chat display area
        self.chat_frame = ctk.CTkFrame(self)
        self.chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create a Text widget for displaying messages
        self.chat_display = tk.Text(self.chat_frame, wrap=tk.WORD, state=tk.DISABLED, font=("Plus Jakarta Sans",18))
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create a frame for the input area
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Create an Entry widget for text input
        self.text_input = ctk.CTkEntry(self.input_frame, placeholder_text="Type your message here...", font=("Plus Jakarta Sans",14))
        self.text_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Bind the Enter key to the send_message method
        self.text_input.bind("<Return>", self.send_message_event)
        
    def send_message_event(self, event):
        self.send_message()
        
    def send_message(self):
        user_message = self.text_input.get()
        if user_message.strip() != "":
            self.display_message("You: " + user_message, "user")
            self.text_input.delete(0, tk.END)

            self.messages.append({"role":"user","content":user_message})
            
            # Simulate a chatbot response with a streaming effect
            self.after(500, lambda: threading.Thread(target=self.stream_response, args=(self.messages,"llama3-8b-8192",)).start())
    
    def display_message(self, message, tag):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, message + "\n", tag)
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
        # Add tags to align text
        self.chat_display.tag_configure('user', justify='right', background='#D0E8FF')
        self.chat_display.tag_configure('bot', justify='left', background='#E8FFD0')

    def stream_response(self, messages, model_name):
        response = run_conversation(messages,model_name=model_name)

        self.messages.append({"role":"assistant","content":response})
        words = response.split(" ")
        self.chat_display.config(state=tk.NORMAL)
        for word in words:
            self.chat_display.insert(tk.END, word + " ", 'bot')
            self.chat_display.see(tk.END)  # Ensure the latest text is visible
            time.sleep(0.1)
        self.chat_display.insert(tk.END, "\n", 'bot')  # Ensure the next message starts on a new line
        self.chat_display.config(state=tk.DISABLED)

if __name__ == "__main__":
    app = ChatbotApp()
    app.mainloop()
