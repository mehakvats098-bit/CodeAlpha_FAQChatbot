
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

from chatbot import get_response


# ---------- Theme ----------
BG = "#F3F6FB"
NAVY = "#172B4D"
BLUE = "#3157D5"
WHITE = "#FFFFFF"
TEXT = "#243247"
MUTED = "#65758B"
GREEN = "#16805D"


root = tk.Tk()
root.title("College FAQ Assistant")
root.geometry("900x720")
root.minsize(650, 550)
root.configure(bg=BG)


# ---------- Header ----------
header = tk.Frame(root, bg=NAVY, padx=22, pady=16)
header.pack(fill="x")

title = tk.Label(
    header,
    text="College FAQ Assistant",
    font=("Segoe UI", 20, "bold"),
    bg=NAVY,
    fg=WHITE
)
title.pack(anchor="w")

subtitle = tk.Label(
    header,
    text="Student support • Admissions • Fees • Exams • Campus life",
    font=("Segoe UI", 10),
    bg=NAVY,
    fg="#D4DEEF"
)
subtitle.pack(anchor="w", pady=(4, 0))


# ---------- Suggested questions ----------
suggestion_frame = tk.Frame(root, bg=BG, padx=16, pady=10)
suggestion_frame.pack(fill="x")

tk.Label(
    suggestion_frame,
    text="TRY ASKING",
    font=("Segoe UI", 9, "bold"),
    fg=MUTED,
    bg=BG
).pack(anchor="w", pady=(0, 7))

suggestion_row = tk.Frame(suggestion_frame, bg=BG)
suggestion_row.pack(fill="x")

suggestions = [
    "How can I apply for admission?",
    "How much are the college fees?",
    "When are the examinations held?",
    "Are scholarships available?"
]


# ---------- Chat area ----------
chat_area = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    font=("Segoe UI", 11),
    bg=WHITE,
    fg=TEXT,
    padx=18,
    pady=16,
    relief="flat",
    borderwidth=0,
    state="disabled",
    cursor="arrow"
)
chat_area.pack(fill="both", expand=True, padx=16, pady=(0, 12))

chat_area.tag_configure(
    "bot_name", foreground=BLUE, font=("Segoe UI", 10, "bold")
)
chat_area.tag_configure(
    "user_name", foreground="#6B46C1", font=("Segoe UI", 10, "bold")
)
chat_area.tag_configure(
    "message", foreground=TEXT, font=("Segoe UI", 11), lmargin1=12,
    lmargin2=12, spacing1=4, spacing3=5
)
chat_area.tag_configure(
    "time", foreground=MUTED, font=("Segoe UI", 8), lmargin1=12
)
chat_area.tag_configure(
    "separator", foreground="#DDE5F0"
)


def add_message(sender, message, is_user=False, confidence=None):
    """Display a timestamped message in the conversation."""
    chat_area.configure(state="normal")

    timestamp = datetime.now().strftime("%I:%M %p")

    name_tag = "user_name" if is_user else "bot_name"
    name = "You" if is_user else "College Assistant"

    chat_area.insert(tk.END, f"{name}\n", name_tag)
    chat_area.insert(tk.END, f"{message}\n", "message")

    if confidence is not None and not is_user:
        chat_area.insert(
            tk.END,
            f"FAQ match confidence: {confidence:.0%}\n",
            "time"
        )

    chat_area.insert(tk.END, f"{timestamp}\n", "time")
    chat_area.insert(tk.END, "─" * 42 + "\n\n", "separator")

    chat_area.configure(state="disabled")
    chat_area.see(tk.END)


def send_message(event=None):
    """Process the user's question and display the response."""
    message = entry.get().strip()

    if not message:
        return "break"

    entry.delete(0, tk.END)
    add_message("You", message, is_user=True)

    result = get_response(message)

    confidence = result["confidence"] if result["known"] else None

    add_message(
        "College Assistant",
        result["answer"],
        confidence=confidence
    )

    return "break"


def ask_suggestion(question):
    """Send a suggested question."""
    entry.delete(0, tk.END)
    entry.insert(0, question)
    send_message()


def clear_chat():
    """Clear the visible conversation and show the welcome message."""
    chat_area.configure(state="normal")
    chat_area.delete("1.0", tk.END)
    chat_area.configure(state="disabled")

    add_message(
        "College Assistant",
        "Welcome back! Ask me about admissions, fees, exams, "
        "scholarships, hostel facilities, placements, or student services."
    )


# ---------- Suggestion buttons ----------
for question in suggestions:
    button = tk.Button(
        suggestion_row,
        text=question,
        font=("Segoe UI", 9),
        bg=WHITE,
        fg=BLUE,
        activebackground="#E6ECFF",
        activeforeground=NAVY,
        relief="solid",
        bd=1,
        padx=8,
        pady=7,
        wraplength=155,
        justify="left",
        cursor="hand2",
        command=lambda q=question: ask_suggestion(q)
    )
    button.pack(side="left", fill="x", expand=True, padx=(0, 6))


# ---------- Input area ----------
input_frame = tk.Frame(root, bg=BG, padx=16, pady=10)
input_frame.pack(fill="x")

entry = tk.Entry(
    input_frame,
    font=("Segoe UI", 12),
    bg=WHITE,
    fg=TEXT,
    insertbackground=TEXT,
    relief="solid",
    bd=1
)
entry.pack(side="left", fill="x", expand=True, ipady=12, padx=(0, 10))
entry.bind("<Return>", send_message)

send_button = tk.Button(
    input_frame,
    text="Send  ➤",
    font=("Segoe UI", 10, "bold"),
    bg=BLUE,
    fg=WHITE,
    activebackground=NAVY,
    activeforeground=WHITE,
    relief="flat",
    padx=18,
    pady=11,
    cursor="hand2",
    command=send_message
)
send_button.pack(side="left")

clear_button = tk.Button(
    input_frame,
    text="Clear chat",
    font=("Segoe UI", 9),
    bg=BG,
    fg=MUTED,
    activebackground="#E1E8F3",
    relief="flat",
    padx=8,
    pady=10,
    cursor="hand2",
    command=clear_chat
)
clear_button.pack(side="left", padx=(6, 0))


# ---------- Footer ----------
footer = tk.Label(
    root,
    text="For official deadlines, fees and policies, confirm with your college.",
    font=("Segoe UI", 9),
    fg=MUTED,
    bg=BG,
    pady=8
)
footer.pack(fill="x")

add_message(
    "College Assistant",
    "Hello! Welcome to the College FAQ Assistant. "
    "How can I help you today? Choose a suggested question or type your own."
)

entry.focus_set()
root.mainloop()
