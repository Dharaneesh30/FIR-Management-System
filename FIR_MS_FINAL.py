import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import csv
import os
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

file_path = 'fir_data.csv'
password_entry = None
login_win = None
root = None
open_windows = []

BG_DARK = '#182848'
BG_LIGHT = '#27408b'
ACCENT = '#00cfff'
FG_TEXT = '#ffffff'
BTN_BG = '#00cfff'
BTN_FG = '#182848'
ENTRY_BG = '#223366'
ENTRY_FG = '#ffffff'
FONT_MAIN = ("Segoe UI", 14)
FONT_TITLE = ("Segoe UI", 28, "bold")


def set_treeview_style():
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Treeview",
                    background=BG_LIGHT,
                    foreground=FG_TEXT,
                    rowheight=32,
                    fieldbackground=BG_LIGHT,
                    font=FONT_MAIN)
    style.map('Treeview', background=[('selected', ACCENT)])
    style.configure("Treeview.Heading", background=ACCENT, foreground=BTN_FG, font=("Segoe UI", 16, "bold"))


def read_csv_data():
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)
            return rows
    except FileNotFoundError:
        return []


def login():
    global login_win, root
    if password_entry.get() == 'policeofficer':
        login_win.destroy()
        root = tk.Tk()
        root.attributes('-fullscreen', True)
        root.bind('<Escape>', lambda e: root.attributes('-fullscreen', False))
        open_homepage()
    else:
        messagebox.showerror("Login Failed", "Invalid Password!")


def open_homepage():
    set_treeview_style()
    root.title("FIR Management System")
    root.configure(bg=BG_DARK)

    center_frame = tk.Frame(root, bg=BG_DARK)
    center_frame.place(relx=0.5, rely=0.5, anchor='center')

    heading = tk.Label(center_frame, text="FIR MANAGEMENT SYSTEM", font=FONT_TITLE, bg=BG_DARK, fg=ACCENT)
    heading.pack(pady=40)

    btn_add = tk.Button(center_frame, text="➕  Add FIR", width=25, height=2, command=open_add_page, bg=BTN_BG, fg=BTN_FG, font=FONT_MAIN, bd=0, relief='flat', activebackground=ACCENT)
    btn_add.pack(pady=16)

    btn_display = tk.Button(center_frame, text="📋  Display FIR", width=25, height=2, command=open_display_page, bg=BTN_BG, fg=BTN_FG, font=FONT_MAIN, bd=0, relief='flat', activebackground=ACCENT)
    btn_display.pack(pady=16)

    btn_analytics = tk.Button(center_frame, text="📊  Crime Analytics", width=25, height=2, command=open_analytics_menu, bg=BTN_BG, fg=BTN_FG, font=FONT_MAIN, bd=0, relief='flat', activebackground=ACCENT)
    btn_analytics.pack(pady=16)

    btn_logout = tk.Button(center_frame, text="🚪  Logout", width=25, height=2, command=logout, bg="#ff4c4c", fg=FG_TEXT, font=FONT_MAIN, bd=0, relief='flat', activebackground="#ff6f6f")
    btn_logout.pack(pady=30)

    root.mainloop()


def open_add_page():
    add_window = tk.Toplevel(root)
    add_window.attributes('-fullscreen', True)
    add_window.bind('<Escape>', lambda e: add_window.attributes('-fullscreen', False))
    open_windows.append(add_window)
    add_window.title("Add FIR Record")
    add_window.configure(bg=BG_LIGHT)

    fields = ["FIR_ID", "Name", "Date", "Crime_Type", "Location", "Status", "Officer"]
    entries = {}

    form_frame = tk.Frame(add_window, bg=BG_LIGHT)
    form_frame.place(relx=0.5, rely=0.5, anchor='center')

    for idx, field in enumerate(fields):
        label = tk.Label(form_frame, text=field, bg=BG_LIGHT, fg=ACCENT, font=FONT_MAIN)
        label.grid(row=idx, column=0, padx=18, pady=16, sticky='e')
        entry = tk.Entry(form_frame, width=36, font=FONT_MAIN, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=ACCENT, bd=1, relief='flat')
        entry.grid(row=idx, column=1, padx=18, pady=16)
        entries[field] = entry

    def save_data():
        data = [entry.get().strip() for entry in entries.values()]
        if all(data):
            file_exists = os.path.exists(file_path)
            try:
                with open(file_path, mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    if not file_exists:
                        writer.writerow(fields)
                    writer.writerow(data)
                messagebox.showinfo("Success", "FIR record added successfully!")
                add_window.destroy()
                open_windows.remove(add_window)
                open_display_page()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save FIR record: {e}")
        else:
            messagebox.showwarning("Validation Error", "All fields must be filled!")

    save_button = tk.Button(form_frame, text="💾 Save FIR", command=save_data, bg=ACCENT, fg=BTN_FG, font=FONT_MAIN, bd=0, relief='flat', activebackground=BTN_BG)
    save_button.grid(row=len(fields), column=1, pady=24)

    # Back Button
    back_button = tk.Button(form_frame, text="← Back", command=lambda: close_window(add_window), bg="#ff4c4c", fg=FG_TEXT, font=FONT_MAIN, bd=0, relief='flat', activebackground="#ff6f6f")
    back_button.grid(row=len(fields), column=0, pady=24)


def open_display_page():
    rows = read_csv_data()
    if len(rows) <= 1:
        messagebox.showinfo("No Data", "No FIR records available to display.")
        return

    headers = rows[0]
    data_rows = rows[1:]

    display_window = tk.Toplevel(root)
    display_window.attributes('-fullscreen', True)
    display_window.bind('<Escape>', lambda e: display_window.attributes('-fullscreen', False))
    open_windows.append(display_window)
    display_window.title("FIR Records")
    display_window.configure(bg=BG_DARK)

    heading = tk.Label(display_window, text="FIR Records", font=FONT_TITLE, bg=BG_DARK, fg=ACCENT)
    heading.pack(pady=24)

    search_label = tk.Label(display_window, text="Search by FIR_ID or Name:", bg=BG_DARK, fg=FG_TEXT, font=FONT_MAIN)
    search_label.pack(pady=8)

    search_entry = tk.Entry(display_window, font=FONT_MAIN, width=38, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=ACCENT, bd=1, relief='flat')
    search_entry.pack(pady=8)

    def search_fir():
        query = search_entry.get().lower()
        filtered_data = [row for row in data_rows if query in row[0].lower() or query in row[1].lower()]
        update_tree_view(filtered_data)

    search_button = tk.Button(display_window, text="🔍 Search", command=search_fir, bg=ACCENT, fg=BTN_FG, font=FONT_MAIN, bd=0, relief='flat', activebackground=BTN_BG)
    search_button.pack(pady=8)

    tree_frame = tk.Frame(display_window, bg=BG_DARK)
    tree_frame.pack(padx=20, pady=20, fill='both', expand=True)

    tree_scroll = tk.Scrollbar(tree_frame)
    tree_scroll.pack(side='right', fill='y')

    tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode='browse')
    tree.pack(fill='both', expand=True)
    tree_scroll.config(command=tree.yview)

    tree['columns'] = headers
    tree['show'] = 'headings'

    for header in headers:
        tree.heading(header, text=header)
        tree.column(header, anchor='center', width=160)

    def update_tree_view(filtered_data):
        for row in tree.get_children():
            tree.delete(row)
        for row in filtered_data:
            tree.insert("", "end", values=row)

    update_tree_view(data_rows)

    def delete_fir():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select an FIR to delete.")
            return

        confirm = messagebox.askyesno("Delete FIR", "Are you sure you want to delete this FIR?")
        if not confirm:
            return

        selected_fir = tree.item(selected_item[0])['values']
        fir_id_to_delete = str(selected_fir[0])

        all_rows = read_csv_data()
        headers = all_rows[0]
        data_rows_all = all_rows[1:]

        new_data_rows = [row for row in data_rows_all if str(row[0]) != fir_id_to_delete]

        if len(new_data_rows) == len(data_rows_all):
            messagebox.showerror("Delete Error", "Could not find the FIR in the data file.")
            return

        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(new_data_rows)

        messagebox.showinfo("Success", "FIR deleted successfully!")
        update_tree_view(new_data_rows)

    def edit_fir():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select an FIR to edit.")
            return

        selected_fir = tree.item(selected_item[0])['values']
        fir_id_to_edit = str(selected_fir[0])

        all_rows = read_csv_data()
        headers = all_rows[0]
        data_rows_all = all_rows[1:]

        for idx, row in enumerate(data_rows_all):
            if str(row[0]) == fir_id_to_edit:
                edit_index = idx
                break
        else:
            messagebox.showerror("Edit Error", "Could not find the FIR in the data file.")
            return

        edit_window = tk.Toplevel(display_window)
        edit_window.title(f"Edit FIR {fir_id_to_edit}")
        edit_window.configure(bg=BG_LIGHT)
        edit_window.geometry("600x500")

        fields = headers
        entries = {}

        form_frame = tk.Frame(edit_window, bg=BG_LIGHT)
        form_frame.pack(padx=20, pady=20, fill='both', expand=True)

        for idx, field in enumerate(fields):
            label = tk.Label(form_frame, text=field, bg=BG_LIGHT, fg=ACCENT, font=FONT_MAIN)
            label.grid(row=idx, column=0, padx=10, pady=10, sticky='e')
            entry = tk.Entry(form_frame, width=30, font=FONT_MAIN, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=ACCENT, bd=1, relief='flat')
            entry.grid(row=idx, column=1, padx=10, pady=10)
            entry.insert(0, row[idx])
            if field == "FIR_ID":
                entry.config(state='disabled')
            entries[field] = entry

        def update_data():
            new_data = [entries[field].get().strip() for field in fields]
            if all(new_data):
                data_rows_all[edit_index] = new_data
                with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(headers)
                    writer.writerows(data_rows_all)
                messagebox.showinfo("Success", "FIR record updated successfully!")
                edit_window.destroy()
                update_tree_view(data_rows_all)
            else:
                messagebox.showwarning("Validation Error", "All fields must be filled!")

        update_button = tk.Button(form_frame, text="Update FIR", command=update_data, bg=ACCENT, fg=BTN_FG, font=FONT_MAIN, bd=0, relief='flat', activebackground=BTN_BG)
        update_button.grid(row=len(fields), column=1, pady=20)

        # Back Button for edit window
        back_button = tk.Button(form_frame, text="← Back", command=lambda: close_window(edit_window), bg="#ff4c4c", fg=FG_TEXT, font=FONT_MAIN, bd=0, relief='flat', activebackground="#ff6f6f")
        back_button.grid(row=len(fields), column=0, pady=20)

    delete_button = tk.Button(display_window, text="🗑️ Delete FIR", command=delete_fir, bg="#ff4c4c", fg=FG_TEXT, font=FONT_MAIN, bd=0, relief='flat', activebackground="#ff6f6f")
    delete_button.pack(pady=8)

    edit_button = tk.Button(display_window, text="✏️ Edit FIR", command=edit_fir, bg=ACCENT, fg=BTN_FG, font=FONT_MAIN, bd=0, relief='flat', activebackground=BTN_BG)
    edit_button.pack(pady=8)

    # Back Button for display window
    back_button = tk.Button(display_window, text="← Back", command=lambda: close_window(display_window), bg="#ff4c4c", fg=FG_TEXT, font=FONT_MAIN, bd=0, relief='flat', activebackground="#ff6f6f")
    back_button.pack(pady=10)


def open_analytics_menu():
    analytics_menu = tk.Toplevel(root)
    analytics_menu.attributes('-fullscreen', True)
    analytics_menu.bind('<Escape>', lambda e: analytics_menu.attributes('-fullscreen', False))
    analytics_menu.title("Crime Analytics")
    analytics_menu.configure(bg=BG_DARK)
    open_windows.append(analytics_menu)

    heading = tk.Label(analytics_menu, text="Crime Analytics", font=FONT_TITLE, bg=BG_DARK, fg=ACCENT)
    heading.pack(pady=32)

    btn1 = tk.Button(analytics_menu, text="Crimes by Type", width=30, height=2, command=show_crimes_by_type, bg=BTN_BG, fg=BTN_FG, font=FONT_MAIN, bd=0, relief='flat')
    btn1.pack(pady=14)

    btn2 = tk.Button(analytics_menu, text="Crimes Over Time", width=30, height=2, command=show_crimes_over_time, bg=BTN_BG, fg=BTN_FG, font=FONT_MAIN, bd=0, relief='flat')
    btn2.pack(pady=14)

    btn3 = tk.Button(analytics_menu, text="Status Distribution", width=30, height=2, command=show_status_distribution, bg=BTN_BG, fg=BTN_FG, font=FONT_MAIN, bd=0, relief='flat')
    btn3.pack(pady=14)

    btn4 = tk.Button(analytics_menu, text="Crimes by Location", width=30, height=2, command=show_crimes_by_location, bg=BTN_BG, fg=BTN_FG, font=FONT_MAIN, bd=0, relief='flat')
    btn4.pack(pady=14)

    btn5 = tk.Button(analytics_menu, text="Crimes by Officer", width=30, height=2, command=show_crimes_by_officer, bg=BTN_BG, fg=BTN_FG, font=FONT_MAIN, bd=0, relief='flat')
    btn5.pack(pady=14)

    btn_close = tk.Button(analytics_menu, text="Close", width=30, height=2, command=analytics_menu.destroy, bg="#ff4c4c", fg=FG_TEXT, font=FONT_MAIN, bd=0, relief='flat')
    btn_close.pack(pady=14)

    # Back Button for analytics menu
    back_button = tk.Button(analytics_menu, text="← Back", command=lambda: close_window(analytics_menu), bg="#ff4c4c", fg=FG_TEXT, font=FONT_MAIN, bd=0, relief='flat', activebackground="#ff6f6f")
    back_button.pack(pady=10)


def show_crimes_by_type():
    try:
        df = pd.read_csv(file_path)
        if 'Crime_Type' not in df.columns:
            messagebox.showerror("Analytics Error", "Missing 'Crime_Type' column in data.")
            return
        win = tk.Toplevel(root)
        win.title("Crimes by Type")
        win.configure(bg=BG_DARK)
        fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG_DARK)
        df['Crime_Type'].value_counts().plot(kind='bar', color='#00cfff', ax=ax)
        ax.set_title("Crimes by Type", color=ACCENT, fontsize=18)
        ax.set_xlabel("Crime Type", color=FG_TEXT)
        ax.set_ylabel("Count", color=FG_TEXT)
        ax.tick_params(axis='x', colors=FG_TEXT, rotation=45)
        ax.tick_params(axis='y', colors=FG_TEXT)
        ax.set_facecolor(BG_LIGHT)
        for spine in ax.spines.values():
            spine.set_visible(False)
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

        # Back Button for this window
        back_button = tk.Button(win, text="← Back", command=lambda: close_window(win), bg="#ff4c4c", fg=FG_TEXT, font=FONT_MAIN, bd=0, relief='flat', activebackground="#ff6f6f")
        back_button.pack(pady=10)

    except Exception as e:
        messagebox.showerror("Analytics Error", f"Error generating chart: {e}")


def show_crimes_over_time():
    try:
        df = pd.read_csv(file_path)
        if 'Date' not in df.columns:
            messagebox.showerror("Analytics Error", "Missing 'Date' column in data.")
            return
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df.dropna(subset=['Date'], inplace=True)
        win = tk.Toplevel(root)
        win.title("Crimes Over Time")
        win.configure(bg=BG_DARK)
        fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG_DARK)
        df['Date'].value_counts().sort_index().plot(kind='line', marker='o', color='#ffb300', ax=ax)
        ax.set_title("Crimes Over Time", color=ACCENT, fontsize=18)
        ax.set_xlabel("Date", color=FG_TEXT)
        ax.set_ylabel("Number of Crimes", color=FG_TEXT)
        ax.tick_params(axis='x', colors=FG_TEXT, rotation=45)
        ax.tick_params(axis='y', colors=FG_TEXT)
        ax.set_facecolor(BG_LIGHT)
        for spine in ax.spines.values():
            spine.set_visible(False)
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

        # Back Button
        back_button = tk.Button(win, text="← Back", command=lambda: close_window(win), bg="#ff4c4c", fg=FG_TEXT, font=FONT_MAIN, bd=0, relief='flat', activebackground="#ff6f6f")
        back_button.pack(pady=10)

    except Exception as e:
        messagebox.showerror("Analytics Error", f"Error generating chart: {e}")


def show_status_distribution():
    try:
        df = pd.read_csv(file_path)
        if 'Status' not in df.columns:
            messagebox.showerror("Analytics Error", "Missing 'Status' column in data.")
            return
        win = tk.Toplevel(root)
        win.title("Status Distribution")
        win.configure(bg=BG_DARK)
        fig, ax = plt.subplots(figsize=(8, 8), facecolor=BG_DARK)
        colors = ['#00cfff', '#ff4c4c', '#ffb300', '#7e57c2', '#43a047']
        df['Status'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=140, ax=ax, colors=colors, textprops={'color': FG_TEXT, 'fontsize': 14})
        ax.set_title("Status Distribution", color=ACCENT, fontsize=18)
        ax.set_ylabel("")
        ax.set_facecolor(BG_LIGHT)
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

        # Back Button
        back_button = tk.Button(win, text="← Back", command=lambda: close_window(win), bg="#ff4c4c", fg=FG_TEXT, font=FONT_MAIN, bd=0, relief='flat', activebackground="#ff6f6f")
        back_button.pack(pady=10)

    except Exception as e:
        messagebox.showerror("Analytics Error", f"Error generating chart: {e}")


def show_crimes_by_location():
    try:
        df = pd.read_csv(file_path)
        if 'Place' not in df.columns:
            messagebox.showerror("Analytics Error", "Missing 'Location' column in data.")
            return
        win = tk.Toplevel(root)
        win.title("Crimes by Location")
        win.configure(bg=BG_DARK)
        fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG_DARK)
        df['Place'].value_counts().plot(kind='bar', color='#43a047', ax=ax)
        ax.set_title("Crimes by Location", color=ACCENT, fontsize=18)
        ax.set_xlabel("Location", color=FG_TEXT)
        ax.set_ylabel("Count", color=FG_TEXT)
        ax.tick_params(axis='x', colors=FG_TEXT, rotation=45)
        ax.tick_params(axis='y', colors=FG_TEXT)
        ax.set_facecolor(BG_LIGHT)
        for spine in ax.spines.values():
            spine.set_visible(False)
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

        # Back Button
        back_button = tk.Button(win, text="← Back", command=lambda: close_window(win), bg="#ff4c4c", fg=FG_TEXT, font=FONT_MAIN, bd=0, relief='flat', activebackground="#ff6f6f")
        back_button.pack(pady=10)

    except Exception as e:
        messagebox.showerror("Analytics Error", f"Error generating chart: {e}")


def show_crimes_by_officer():
    try:
        df = pd.read_csv(file_path)
        if 'Officer' not in df.columns:
            messagebox.showerror("Analytics Error", "Missing 'Officer' column in data.")
            return
        win = tk.Toplevel(root)
        win.title("Crimes by Officer")
        win.configure(bg=BG_DARK)
        fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG_DARK)
        df['Officer'].value_counts().plot(kind='bar', color='#7e57c2', ax=ax)
        ax.set_title("Crimes by Officer", color=ACCENT, fontsize=18)
        ax.set_xlabel("Officer", color=FG_TEXT)
        ax.set_ylabel("Count", color=FG_TEXT)
        ax.tick_params(axis='x', colors=FG_TEXT, rotation=45)
        ax.tick_params(axis='y', colors=FG_TEXT)
        ax.set_facecolor(BG_LIGHT)
        for spine in ax.spines.values():
            spine.set_visible(False)
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

        # Back Button
        back_button = tk.Button(win, text="← Back", command=lambda: close_window(win), bg="#ff4c4c", fg=FG_TEXT, font=FONT_MAIN, bd=0, relief='flat', activebackground="#ff6f6f")
        back_button.pack(pady=10)

    except Exception as e:
        messagebox.showerror("Analytics Error", f"Error generating chart: {e}")


def logout():
    global root, open_windows
    for win in open_windows:
        try:
            win.destroy()
        except:
            pass
    open_windows.clear()
    messagebox.showinfo("Logout", "You have been logged out!")
    if root:
        root.destroy()
        root = None
    login_window()


def login_window():
    global login_win, password_entry
    login_win = tk.Tk()
    login_win.attributes('-fullscreen', True)
    login_win.bind('<Escape>', lambda e: login_win.attributes('-fullscreen', False))
    login_win.title("Login")

    # Add background image to login page only, aligned over the main monitor
    try:
        login_win.update_idletasks()
        screen_width = login_win.winfo_screenwidth()
        screen_height = login_win.winfo_screenheight()
        bg_image = Image.open("bg.jpg")
        bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(login_win, image=bg_photo)
        bg_label.image = bg_photo  # Keep reference
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        login_win.configure(bg=BG_DARK)

    # Align login frame over the main monitor in the image (visually around relx=0.45, rely=0.56)
    login_frame = tk.Frame(login_win, bg='#000000', bd=0)
    login_frame.place(relx=0.45, rely=0.56, anchor='center')

    label = tk.Label(login_frame, text="Enter Password", font=FONT_TITLE, bg='#000000', fg=ACCENT)
    label.pack(pady=40)

    password_entry = tk.Entry(login_frame, show="*", font=FONT_MAIN, width=28, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=ACCENT, bd=1, relief='flat')
    password_entry.pack(pady=20)

    login_button = tk.Button(login_frame, text="🔓 Login", command=login, bg=BTN_BG, fg=BTN_FG, font=FONT_MAIN, bd=0, relief='flat', activebackground=ACCENT)
    login_button.pack(pady=30)

    login_win.mainloop()


def close_window(win):
    """Helper function to close a window and remove from open_windows if tracked."""
    if win in open_windows:
        open_windows.remove(win)
    win.destroy()


# Run the login window
login_window()

