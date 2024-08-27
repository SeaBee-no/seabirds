import os
import yaml
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class ConfigEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Config File Editor")
        
        # Directory selection
        self.directory_label = tk.Label(root, text="Directory:")
        self.directory_label.grid(row=0, column=0, padx=10, pady=10)
        self.directory_entry = tk.Entry(root, width=50)
        self.directory_entry.grid(row=0, column=1, padx=10, pady=10)
        self.browse_button = tk.Button(root, text="Browse", command=self.browse_directory)
        self.browse_button.grid(row=0, column=2, padx=10, pady=10)
        
        # Config file list
        self.config_listbox = tk.Listbox(root, height=20, width=50)
        self.config_listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        self.config_listbox.bind('<<ListboxSelect>>', self.load_config)
        
        # Text area for YAML content
        self.config_text = tk.Text(root, wrap="word", height=20, width=80)
        self.config_text.grid(row=1, column=3, columnspan=2, padx=10, pady=10)

        # Save button
        self.save_button = tk.Button(root, text="Save", command=self.save_config)
        self.save_button.grid(row=2, column=4, padx=10, pady=10, sticky="e")

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory_entry.delete(0, tk.END)
            self.directory_entry.insert(0, directory)
            self.load_config_files(directory)

    def load_config_files(self, directory):
        self.config_listbox.delete(0, tk.END)
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file == 'config.seabee.yaml':
                    self.config_listbox.insert(tk.END, os.path.join(root, file))

    def load_config(self, event):
        selected = self.config_listbox.curselection()
        if selected:
            file_path = self.config_listbox.get(selected[0])
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.config_text.delete(1.0, tk.END)
                self.config_text.insert(tk.END, content)
            self.current_file = file_path

    def save_config(self):
        if hasattr(self, 'current_file'):
            content = self.config_text.get(1.0, tk.END)
            try:
                yaml.safe_load(content)  # Validate YAML
                with open(self.current_file, 'w', encoding='utf-8') as file:
                    file.write(content)
                messagebox.showinfo("Success", "Config file saved successfully!")
            except yaml.YAMLError as e:
                messagebox.showerror("Error", f"Invalid YAML format: {e}")
        else:
            messagebox.showwarning("No file selected", "Please select a config file to save.")

# Create the main window
root = tk.Tk()
app = ConfigEditor(root)
root.mainloop()
