import tkinter as tk
from tkinter import ttk
import pyjokes as pj


class DevJokesApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dev Jokes")
        self.configure(bg='#1e1e1e')

        self._setup_styles()
        self._setup_widgets()

    # ---------- Styles ----------
    def _setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("default")

        style.configure("TFrame", background="#1e1e1e")
        style.configure("TLabel",
                        background="#1e1e1e",
                        foreground="#f5f5f5",
                        font=("Helvetica", 12))
        style.configure("TButton",
                        background="#2c2c2c",
                        foreground="#f5f5f5",
                        font=("Helvetica", 11))
        style.map("TButton",
                  background=[("active", "#00adb5")],
                  foreground=[("active", "#ffffff")])

    # ---------- Widgets ----------
    def _setup_widgets(self):
        # Header
        frame = ttk.Frame(self)
        frame.pack(padx=20, pady=20)

        label = ttk.Label(frame, text='Jokes for Programers',
                          font=('Helvetica', 16, 'bold'))
        label.pack()

        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        buttons_info = [
            ('Get Joke', self.get_joke),
            ('Get All Jokes', self.show_all_jokes),
            ('Clear', self.clear_jokes),
        ]

        for text, cmd in buttons_info:
            ttk.Button(button_frame, text=text, command=cmd).pack(
                side=tk.LEFT, padx=5)

        # Radio buttons (joke type)
        radio_frame = ttk.Frame(self)
        radio_frame.pack(pady=10)

        self.joke_type = tk.StringVar(value='all')

        for text, val in [('All', 'all'), ('Chuck', 'chuck'), ('Neutral', 'neutral')]:
            ttk.Radiobutton(radio_frame, text=text, variable=self.joke_type,
                            value=val).pack(side=tk.LEFT, padx=5)

        # Language Listbox
        listbox_frame = ttk.Frame(self)
        listbox_frame.pack(pady=10)

        self.lb_languages = tk.Listbox(listbox_frame, height=8)
        self.lb_languages.pack(side=tk.LEFT)

        self.language_map = {
            'English': 'en', 'Czech': 'cs', 'German': 'de', 'Spanish': 'es',
            'Basque': 'eu', 'French': 'fr', 'Galician': 'gl', 'Hungarian': 'hu',
            'Italian': 'it', 'Lithuanian': 'lt', 'Polish': 'pl', 'Russian': 'ru',
            'Swedish': 'sv', 'Turkish': 'tr'
        }

        for name in self.language_map.keys():
            self.lb_languages.insert(tk.END, name)

        # Default select English (first item) on startup
        self.lb_languages.selection_set(0)

        # Joke display with scrollbar
        message_frame = ttk.Frame(self)
        message_frame.pack(pady=10)

        self.joke_text = tk.Text(
            message_frame, wrap='word', height=10, width=50)
        self.joke_text.pack(side=tk.LEFT, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(
            message_frame, orient='vertical', command=self.joke_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.joke_text.configure(yscrollcommand=scrollbar.set)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(self, textvariable=self.status_var,
                                    style='Status.TLabel', anchor='w')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Initialize status with defaults
        self._update_status('Ready')

    # ---------- Utility Methods ----------
    def _update_status(self, context=''):
        lang = self.get_selected_language().upper()
        category = self.joke_type.get()
        msg = f'Lang: {lang} | Category: {category}'
        if context:
            msg = f'{context} -> {msg}'
        self.status_var.set(msg)

    def get_selected_language(self):
        selection = self.lb_languages.curselection()
        if selection:
            return self.language_map[self.lb_languages.get(selection[0])]
        return 'en'

    # ---------- Actions ----------
    def get_joke(self):
        lang = self.get_selected_language()
        category = self.joke_type.get()
        self.joke_text.delete('1.0', tk.END)
        try:
            joke = pj.get_joke(language=lang, category=category)
            self.joke_text.insert(tk.END, joke)
            self._update_status('1 joke shown')
        except Exception:
            self.joke_text.insert(
                tk.END, f"No jokes found for {category} in {lang.upper()}."
            )
            self._update_status('No jokes found')

    def show_all_jokes(self):
        jokes = pj.get_jokes()
        self.joke_text.delete('1.0', tk.END)
        self.joke_text.insert(tk.END, '\n\n'.join(jokes))
        self._update_status(f'{len(jokes)} jokes shown')

    def clear_jokes(self):
        self.joke_text.delete('1.0', tk.END)
        self._update_status('Cleared jokes')


# ---------- Run App ----------
if __name__ == '__main__':
    app = DevJokesApp()
    app.mainloop()
