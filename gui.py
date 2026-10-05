import tkinter as tk
from tkinter import filedialog, messagebox
import core

COLORS = {"HIGH": "#d9534f", "MEDIUM": "#f0ad4e", "LOW": "#5cb85c"}


class App:
    def __init__(self, root):
        self.root = root
        self.current_file = None
        root.title("Metadata Privacy Checker")
        root.geometry("560x520")

        tk.Label(root, text="Metadata Privacy Checker",
                 font=("Arial", 16, "bold")).pack(pady=(15, 5))
        tk.Label(root, text="Supports JPG, PDF and DOCX files").pack()

        tk.Button(root, text="Choose File", width=20,
                  command=self.choose_file).pack(pady=10)

        self.file_label = tk.Label(root, text="No file selected", fg="gray")
        self.file_label.pack()

        self.risk_label = tk.Label(root, text="RISK: -", font=("Arial", 14, "bold"),
                                   width=30, pady=8, bg="#cccccc")
        self.risk_label.pack(pady=10)

        self.reason_label = tk.Label(root, text="")
        self.reason_label.pack()

        self.text = tk.Text(root, height=12, width=62, state="disabled")
        self.text.pack(pady=10)

        self.clean_btn = tk.Button(root, text="Clean File", width=20,
                                   state="disabled", command=self.clean_file)
        self.clean_btn.pack(pady=5)

    def choose_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("Supported files", "*.jpg *.jpeg *.pdf *.docx")])
        if not path:
            return
        self.current_file = path
        self.file_label.config(text=path.split("/")[-1], fg="black")
        try:
            result = core.analyze(path)
        except Exception as e:
            messagebox.showerror("Error", f"Could not read file:\n{e}")
            return
        self.show_result(result)

    def show_result(self, result):
        level = result["risk"]
        self.risk_label.config(text=f"RISK: {level}", bg=COLORS[level], fg="white")
        self.reason_label.config(text=result["reasons"][0])

        self.text.config(state="normal")
        self.text.delete("1.0", "end")
        if result["fields"]:
            for name, value in result["fields"]:
                self.text.insert("end", f"{name}: {value}\n")
        else:
            self.text.insert("end", "No metadata found. This file looks clean!")
        self.text.config(state="disabled")
        self.clean_btn.config(state="normal")

    def clean_file(self):
        try:
            out = core.clean(self.current_file)
        except Exception as e:
            messagebox.showerror("Error", f"Could not clean file:\n{e}")
            return
        messagebox.showinfo("Done", f"Cleaned copy saved as:\n{out}")
        self.show_result(core.analyze(out))
        self.file_label.config(text=out.name)


root = tk.Tk()
App(root)
root.mainloop()
