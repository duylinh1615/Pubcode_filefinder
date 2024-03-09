import os
import fnmatch
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

def delete_files_with_pattern():
    folder_path = folder_path_var.get()
    pattern = pattern_var.get()
    
    if not os.path.isdir(folder_path):
        result_label.config(text="Invalid folder path!", fg="red")
        return

    if not pattern:
        result_label.config(text="Pattern can't be empty!", fg="red")
        return
    
    confirmed = messagebox.askyesno("Confirmation", f"Are you sure you want to delete files with pattern '{pattern}'?")
    if not confirmed:
        return
    
    deleted_files_count = 0
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if fnmatch.fnmatch(filename, pattern):
                file_path = os.path.join(root, filename)
                os.remove(file_path)
                deleted_files_count += 1
    
    result_label.config(text=f"Deleted {deleted_files_count} file(s) with pattern '{pattern}'", fg="green")

def list_files_with_pattern():
    folder_path = folder_path_var.get()
    pattern = pattern_var.get()
    files_text.delete("1.0", tk.END)
    
    if not os.path.isdir(folder_path):
        result_label.config(text="Invalid folder path!", fg="red")
        return

    if not pattern:
        result_label.config(text="Pattern can't be empty!", fg="red")
        return
    
    files_found = []
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if fnmatch.fnmatch(filename, pattern):
                file_path = os.path.join(root, filename)
                files_text.insert(tk.END, file_path + '\n')
                files_found.append(file_path)
    
    if not files_found:
        result_label.config(text="No files found with the specified pattern.", fg="blue")
    else:
        result_label.config(text=f"Found {len(files_found)} file(s) with the specified pattern.", fg="green")

def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path_var.set(folder_selected)

def copy_files_to_destination():
    folder_path = folder_path_var.get()
    pattern = pattern_var.get()
    
    if not os.path.isdir(folder_path):
        result_label.config(text="Invalid source folder path!", fg="red")
        return

    if not pattern:
        result_label.config(text="Pattern can't be empty!", fg="red")
        return
    
    destination_path = filedialog.askdirectory()
    if not destination_path:
        return
    
    files_copied_count = 0
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if fnmatch.fnmatch(filename, pattern):
                source_file_path = os.path.join(root, filename)
                destination_file_path = os.path.join(destination_path, filename)
                shutil.copy2(source_file_path, destination_file_path)
                files_copied_count += 1
    
    result_label.config(text=f"Copied {files_copied_count} file(s) with pattern '{pattern}' to '{destination_path}'", fg="green")

def cut_files_to_destination():
    folder_path = folder_path_var.get()
    pattern = pattern_var.get()
    
    if not os.path.isdir(folder_path):
        result_label.config(text="Invalid source folder path!", fg="red")
        return

    if not pattern:
        result_label.config(text="Pattern can't be empty!", fg="red")
        return
    
    destination_path = filedialog.askdirectory()
    if not destination_path:
        return
    
    files_moved_count = 0
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if fnmatch.fnmatch(filename, pattern):
                source_file_path = os.path.join(root, filename)
                destination_file_path = os.path.join(destination_path, filename)
                shutil.move(source_file_path, destination_file_path)
                files_moved_count += 1
    
    result_label.config(text=f"Moved {files_moved_count} file(s) with pattern '{pattern}' to '{destination_path}'", fg="green")

# GUI
root = tk.Tk()
root.title("Name File Finder")

folder_path_var = tk.StringVar()
pattern_var = tk.StringVar()

folder_label = tk.Label(root, text="Source Folder Path:")
folder_label.grid(row=0, column=0, padx=5, pady=5)

folder_entry = tk.Entry(root, textvariable=folder_path_var, state='readonly', width=50)
folder_entry.grid(row=0, column=1, padx=5, pady=5)

pattern_label = tk.Label(root, text="Pattern:")
pattern_label.grid(row=1, column=0, padx=5, pady=5)

pattern_entry = tk.Entry(root, textvariable=pattern_var, width=30)
pattern_entry.grid(row=1, column=1, padx=5, pady=5)

select_folder_button = tk.Button(root, text="Select Source Folder", command=select_folder)
select_folder_button.grid(row=0, column=2, padx=5, pady=5)

list_button = tk.Button(root, text="List Files", command=list_files_with_pattern)
list_button.grid(row=1, column=2, padx=5, pady=5)

copy_button = tk.Button(root, text="Copy Files", command=copy_files_to_destination)
copy_button.grid(row=2, column=0, padx=5, pady=5)

cut_button = tk.Button(root, text="Cut Files", command=cut_files_to_destination)
cut_button.grid(row=2, column=1, padx=5, pady=5)

delete_button = tk.Button(root, text="Delete Files", command=delete_files_with_pattern)
delete_button.grid(row=2, column=2, padx=5, pady=5)

files_text_frame = tk.Frame(root)
files_text_frame.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

files_text_scrollbar = tk.Scrollbar(files_text_frame, orient=tk.VERTICAL)
files_text = tk.Text(files_text_frame, yscrollcommand=files_text_scrollbar.set, wrap=tk.WORD)
files_text_scrollbar.config(command=files_text.yview)
files_text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
files_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

result_label = tk.Label(root, text="", fg="green")
result_label.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

root.mainloop()
