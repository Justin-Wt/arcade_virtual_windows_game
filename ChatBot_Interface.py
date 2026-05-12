import customtkinter as ctk
import ChatBot_AI
import json
import os

chat = 0
parent = ""
filename = "chatbot_memories.json"

ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.geometry("700x400")

# SIDEBAR
sidebar = ctk.CTkFrame(app)
sidebar.place(relwidth=0.2, relheight=1.0)

new_chat_button = ctk.CTkButton(sidebar, text="New Chat", command=lambda: new_chat())
new_chat_button.pack(pady=10)
# SEPARATOR
separator = ctk.CTkFrame(app, width=2, fg_color="#000000")
separator.place(relx=0.2, relheight=1.0)

# HORIZONTAL SEPARATOR
separator_horizontal = ctk.CTkFrame(sidebar, height=2, fg_color="#000000")
separator_horizontal.pack(fill="x", pady=5)

# BOTTOM SECTION
bottom_sidebar = ctk.CTkScrollableFrame(sidebar)
bottom_sidebar.pack(fill="both", expand=True, padx=5, pady=5)

label2 = ctk.CTkLabel(bottom_sidebar, text="Chat History")
label2.pack(pady=10)

# MAIN AREA
main = ctk.CTkFrame(app)
main.place(relx=0.2, relwidth=0.8, relheight=1.0)

label = ctk.CTkLabel(main, text="Hello There")
label.pack(pady=20)
chat_area = ctk.CTkScrollableFrame(main)
chat_area.pack(fill="both", expand=True, padx=10, pady=10)

# BOTTOM BAR
bottom_frame = ctk.CTkFrame(main)
bottom_frame.pack(side="bottom", fill="x", padx=10, pady=10)

entry = ctk.CTkEntry(bottom_frame)
entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

button = ctk.CTkButton(
    bottom_frame, text="Send", command=lambda: add_message(entry.get())
)
button.pack(side="left")
buttons = []
messages = []
if os.path.exists(filename):
    with open(filename, "r") as f:
        history = json.load(f)
    for item in history:
        button = ctk.CTkButton(
            bottom_sidebar,
            text=item["name"],
            fg_color="#333333",
            hover_color="#555555",
            anchor="w",
            command=lambda item=item: load_chat(item["name"]),
        )
        button.pack(pady=5, expand=True, fill="x")
        buttons.append(button)


def refresh_history():
    for button in buttons:
        button.destroy()
    buttons.clear()
    with open(filename, "r") as f:
        history = json.load(f)
    for item in history:
        button = ctk.CTkButton(
            bottom_sidebar,
            text=item["name"],
            fg_color="#333333",
            hover_color="#555555",
            anchor="w",
            command=lambda item=item: load_chat(item["name"]),
        )
        button.pack(pady=5, expand=True, fill="x")


def load_chat(name):
    for bubble in messages:
        bubble.destroy()
    messages.clear()
    global parent
    global chat
    parent = name
    with open(filename, "r") as f:
        history = json.load(f)
    for item in history:
        if item["name"] == name:
            for i, message in enumerate(item["data"], start=1):
                bubble = ctk.CTkFrame(chat_area)
                if i % 2 == 1:
                    bubble.pack(anchor="e", padx=10, pady=5)
                else:
                    bubble.pack(anchor="w", padx=10, pady=5)
                label = ctk.CTkLabel(bubble, text=message["content"], width=100)
                label.pack(side="left", padx=10, pady=10)
                messages.append(bubble)
    chat = len(item["data"]) // 2


def new_chat():
    for bubble in messages:
        bubble.destroy()
    messages.clear()


def add_message(text):
    global parent
    global chat
    if chat == 0:
        parent = text
    bubble = ctk.CTkFrame(chat_area)
    bubble.pack(anchor="e", padx=10, pady=5)
    label = ctk.CTkLabel(bubble, text=text, width=100)
    label.pack(side="left", padx=10, pady=10)
    messages.append(bubble)
    text = ChatBot_AI.chat(parent, text)
    bubble = ctk.CTkFrame(chat_area)
    bubble.pack(anchor="w", padx=10, pady=5)
    label = ctk.CTkLabel(bubble, text=text, width=100)
    label.pack(side="left", padx=10, pady=10)
    messages.append(bubble)
    if chat == 0:
        refresh_history()
    chat += 1


app.mainloop()
