"""import tkinter as tk
from tkinter import filedialog
import pandas as pd

df = None

def upload_csv():
    global df
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])

        if file_path:
            df = pd.read_csv(file_path, sep=";")
            # label_status.config(text="File uploaded successfully!")
        else:
            # label_status.config(text="No file selected.")
            pass
    pass
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, simpledialog
import pandas as pd
import os
import io

class CSVEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV File Viewer/Editor")
        self.df = None
        self.file_path = None

        # Buttons
        self.upload_btn = tk.Button(root, text="Upload CSV", command=self.upload_csv)
        self.upload_btn.pack(pady=5)

        self.save_btn = tk.Button(root, text="Save Changes", command=self.save_csv, state=tk.DISABLED)
        self.save_btn.pack(pady=5)

        self.data_btn = tk.Button(root, text="Modify Data", command=self.data_cleanup, state=tk.DISABLED)
        self.data_btn.pack(pady=5)


        # Text area for displaying CSV contents
        self.text_area = scrolledtext.ScrolledText(root, width=100, height=30)
        self.text_area.pack(padx=10, pady=10)

    def upload_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                self.df = pd.read_csv(file_path, sep=",")
                self.file_path = file_path
                self.display_csv()
                self.save_btn.config(state=tk.NORMAL)
                self.data_btn.config(state=tk.NORMAL)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read CSV file:\n{e}")

    def display_csv(self):
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, self.df.to_csv(index=False, sep=","))

    def save_csv(self):
        if not self.file_path:
            return

        try:
            content = self.text_area.get("1.0", tk.END).strip()
            new_df = pd.read_csv(io.StringIO(content), sep=",")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to parse edited content:\n{e}")
            return

        choice = messagebox.askyesnocancel(
            "Save Options",
            f"Do you want to overwrite '{os.path.basename(self.file_path)}'?\n\n"
            "Yes: Overwrite\nNo: Save as new file\nCancel: Abort"
        )
        if choice is None:
            # Cancel
            return
        elif choice:
            # Overwrite existing file
            try:
                new_df.to_csv(self.file_path, index=False, sep=",")
                messagebox.showinfo("Success", "File overwritten successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{e}")
        else:
            # Save as new file
            new_path=filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if new_path:
                try:
                    new_df.to_csv(new_path, index=False, sep=",")
                    messagebox.showinfo("Success", f"File saved as '{os.path.basename(new_path)}'.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save file:\n{e}")

    def data_cleanup(self):
        if self.df is None:
            messagebox.showwarning("No Data", "Please upload a CSV first.")
            return

        # Create a popup window
        popup = tk.Toplevel(self.root)
        popup.title("Modify Data")
        popup.geometry("400x300")

        label = tk.Label(popup, text="This is a placeholder for data cleanup functions.", wraplength=350)
        label.pack(pady=10)

        dropna_btn = tk.Button(popup, text="Drop Rows with NaN", command=lambda: self.drop_na_rows(popup))
        dropna_btn.pack(pady=5)

        close_btn = tk.Button(popup, text="Close", command=popup.destroy)
        close_btn.pack(pady=20)

    def drop_na_rows(self, popup):
        self.df.dropna(inplace=True)
        self.display_csv()
        messagebox.showinfo("Rows Dropped", "Rows with missing values were dropped.")
        popup.destroy()




# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = CSVEditorApp(root)
    root.mainloop()