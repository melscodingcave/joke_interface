import tkinter as tk
from tkinter import ttk
import pyjokes as pj

style = ttk.Style()
style.theme_use("default")

style.configure("TFrame", background="#1e1e1e")
style.configure("TLabel", background="#1e1e1e",
                foreground="#f5f5f5", font=("Helvetica", 12))
style.configure("TButton", background="#2c2c2c",
                foreground="#f5f5f5", font=("Helvetica", 11))
style.map("TButton", background=[
          ("active", "#00adb5")], foreground=[("active", "#ffffff")])

# Function to create widgets with all options


def create_widget(parent, widget_type, **options):
    return widget_type(parent, **options)


def create_button(parent, text, fg):
    return create_widget(parent, ttk.Button, text=text, cursor='hand2')


def create_radio(parent, text, fg):
    return create_widget(parent, ttk.Radiobutton, text=text, cursor='hand2')


def create_listbox(parent):
    return create_widget(parent, tk.Listbox, cursor='hand2')


def get_selected_language():
    try:
        selection = lb_languages.curselection()[0]
        display_name = lb_languages.get(selection)
        return language_map[display_name]
    except IndexError:
        return "en"


def create_messagebox(parent):
    return create_widget(parent, ttk.Message, cursor='hand2')


def get_joke():
    lang = get_selected_language()
    type_choice = joke_type.get()
    try:
        joke = pj.get_joke(language=lang, category=type_choice)
        joke_text.delete("1.0", tk.END)
        joke_text.insert(tk.END, joke)
    except Exception as e:
        joke_text.delete("1.0", tk.END)
        joke_text.insert(
            tk.END, f"No jokes found for {type_choice} in {lang.upper()}.")


def show_all_jokes():
    jokes = pj.get_jokes()
    all_jokes = "\n\n".join(jokes)
    joke_text.delete("1.0", tk.END)
    joke_text.insert(tk.END, all_jokes)


def clear_jokes():
    joke_text.delete("1.0", tk.END)
    joke_text.insert(tk.END, "")


# Create the main window
window = create_widget(None, tk.Tk)
window.title("Dev Jokes")
window.configure(bg="#1e1e1e")

# Create a Frame widget with all options
frame = create_widget(window, ttk.Frame, cursor='hand2',
                      height=100, width=200)
frame.pack(padx=20, pady=20)

# Create Label widget with all options
label = create_widget(frame, ttk.Label, text='Jokes for Programmers',
                      font='50', cursor='hand2')
label.pack()

# Create a frame for buttons
button_frame = create_widget(
    window, ttk.Frame, cursor='hand2', height=50, width=200)
button_frame.pack(pady=10)

# Create buttons
buttons_info = [("Get Joke", "red", get_joke),
                ("Get All Jokes", "brown", show_all_jokes), ("Clear", "blue", clear_jokes)]

for text, fg, cmd in buttons_info:
    button = create_button(button_frame, text=text, fg=fg)
    button.config(command=cmd)
    button.pack(side=tk.LEFT)

# Create a frame for radios
radio_frame = create_widget(
    window, ttk.Frame, cursor='hand2')
radio_frame.pack(pady=10)

joke_type = tk.StringVar(value="all")

# Create radios
radios_info = [
    ("All", "green", "all"),
    ("Chuck", "purple", "chuck"),
    ("Neutral", "orange", "neutral")
]

for text, fg, val in radios_info:
    radio = create_radio(radio_frame, text=text, fg=fg)
    radio.config(variable=joke_type, value=val)
    radio.pack(side=tk.LEFT)

# Create a frame for listbox
listbox_frame = create_widget(
    window, ttk.Frame, cursor='hand2')
listbox_frame.pack(pady=10)

# Create radios
lb_languages = create_listbox(listbox_frame)

language_map = {
    "English": "en",
    "Czech": "cs",
    "German": "de",
    "Spanish": "es",
    "Basque": "eu",
    "French": "fr",
    "Galician": "gl",
    "Hungarian": "hu",
    "Italian": "it",
    "Lithuanian": "lt",
    "Polish": "pl",
    "Russian": "ru",
    "Swedish": "sv",
    "Turkish": "tr"
}

for name in language_map.keys():
    lb_languages.insert(tk.END, name)

lb_languages.pack(side=tk.LEFT)

message_frame = create_widget(
    window, ttk.Frame, cursor='hand2', height=50, width=200)
message_frame.pack(pady=10)

joke_text = tk.Text(message_frame, wrap="word",
                    height=10, width=50)
joke_text.pack(padx=10, pady=10)

# Run the Tkinter event loop
window.mainloop()
