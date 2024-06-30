import tkinter as tk
from tkinter import filedialog, messagebox
import json

class FishingDataGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Fishing Data Viewer")
        
        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)
        
        self.load_button = tk.Button(self.frame, text="Load .fson File", command=self.load_file)
        self.load_button.grid(row=0, column=0, padx=5)
        
        self.listbox_frame = tk.Frame(self.frame)
        self.listbox_frame.grid(row=1, column=0, columnspan=3, pady=10)

        self.scrollbar = tk.Scrollbar(self.listbox_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(self.listbox_frame, width=100, height=20, selectmode=tk.EXTENDED, yscrollcommand=self.scrollbar.set)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.scrollbar.config(command=self.listbox.yview)

        self.listbox.bind('<<ListboxSelect>>', self.update_average_pull)
        
        self.fish_button = tk.Button(self.frame, text="FISH", command=lambda: self.label_entries(True))
        self.fish_button.grid(row=2, column=0, padx=5)
        
        self.no_fish_button = tk.Button(self.frame, text="NO FISH", command=lambda: self.label_entries(False))
        self.no_fish_button.grid(row=2, column=1, padx=5)
        
        self.save_button = tk.Button(self.frame, text="Save", command=self.save_file)
        self.save_button.grid(row=2, column=2, padx=5)
        
        self.play_button = tk.Button(self.frame, text="▶️", command=self.start_playing)
        self.play_button.grid(row=2, column=3, padx=5)
        
        self.pause_button = tk.Button(self.frame, text="⏸️", command=self.pause_playing)
        self.pause_button.grid(row=2, column=4, padx=5)
        
        self.average_label = tk.Label(self.frame, text="Average Pull: N/A", font=("Helvetica", 16))
        self.average_label.grid(row=1, column=3, padx=20)
        
        self.data = []
        self.file_path = None
        self.playing = False
    
    def load_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("FSON files", "*.fson")])
        if self.file_path:
            try:
                with open(self.file_path, 'r') as file:
                    self.data = json.load(file)
                    self.display_data()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")
    
    def display_data(self, scroll_position=None, selected_indices=None):
        self.listbox.delete(0, tk.END)
        for idx, entry in enumerate(self.data):
            coords = entry.get("coords", {})
            lon = coords.get("lon", "N/A")
            lat = coords.get("lat", "N/A")
            pull = entry.get("pull", "N/A")
            label = entry.get("label", "N/A")
            emoji = "🐟" if label is True else "❌" if label is False else ""
            entry_str = f"{emoji} Entry {idx + 1}: Lon={lon}, Lat={lat}, Pull={pull}, Label={label}"
            self.listbox.insert(tk.END, entry_str)
            if label is None:
                self.listbox.itemconfig(tk.END, {'bg': 'red'})
        
        if scroll_position:
            self.listbox.yview_moveto(scroll_position)
        if selected_indices:
            for idx in selected_indices:
                self.listbox.selection_set(idx)
    
    def label_entries(self, is_fish):
        selected_indices = self.listbox.curselection()
        if not selected_indices:
            return
        
        scroll_position = self.listbox.yview()[0]
        for idx in selected_indices:
            self.data[idx]["label"] = is_fish
        self.display_data(scroll_position, selected_indices)
        self.update_average_pull()
    
    def save_file(self):
        if self.file_path:
            try:
                with open(self.file_path, 'w') as file:
                    json.dump(self.data, file, indent=4)
                messagebox.showinfo("Success", "File saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")
    
    def update_average_pull(self, event=None):
        selected_indices = self.listbox.curselection()
        if selected_indices:
            total_pull = 0
            count = 0
            for idx in selected_indices:
                pull = self.data[idx].get("pull", 0.0)
                total_pull += pull
                count += 1
            average_pull = total_pull / count if count else 0
            self.average_label.config(text=f"Average Pull: {average_pull:.2f}")
        else:
            self.average_label.config(text="Average Pull: N/A")

    def start_playing(self):
        self.playing = True
        selected_indices = self.listbox.curselection()
        start_idx = selected_indices[0] if selected_indices else 0
        self.auto_select_entries(start_idx)
    
    def pause_playing(self):
        self.playing = False
    
    def auto_select_entries(self, current_idx):
        if self.playing and current_idx < len(self.data):
            self.listbox.selection_set(current_idx)
            self.listbox.see(current_idx)
            self.update_average_pull()
            self.root.after(150, self.auto_select_entries, current_idx + 1)

if __name__ == "__main__":
    root = tk.Tk()
    app = FishingDataGUI(root)
    root.mainloop()