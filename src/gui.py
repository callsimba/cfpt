import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox
from ttkthemes import ThemedTk
from user_agent_manager import get_random_user_agent, add_user_agent, list_user_agents
from proxies import add_proxy, remove_proxy, list_proxies, get_random_proxy
from mnemonics import add_mnemonic, remove_mnemonic, list_mnemonics
from report import log_activity, send_report_to_telegram
import threading
import time
import subprocess
import os
import random
import pickle

# Replace with your actual bot token and chat ID
BOT_TOKEN = '7147301992:AAGvyk8lQ6uOj9uyRzdStokZTU4UfgETpNY'
CHAT_ID = '6067013209'

# Globals for rotation
rotation_interval = 1  # Default to 1 minute
rotation_thread = None
rotation_running = False
active_proxy = None

# File to save settings
SETTINGS_FILE = "settings.pkl"

def start_rotation():
    global rotation_thread, rotation_running
    rotation_running = True
    rotation_thread = threading.Thread(target=rotate_user_agents)
    rotation_thread.start()

def stop_rotation():
    global rotation_running
    rotation_running = False
    if rotation_thread:
        rotation_thread.join()

def rotate_user_agents():
    while rotation_running:
        user_agent = get_random_user_agent()
        log_activity(f"Rotating User Agent: {user_agent}")
        send_report_to_telegram(BOT_TOKEN, CHAT_ID, f"Rotating User Agent: {user_agent}")
        time.sleep(rotation_interval * 60)  # Convert minutes to seconds

def save_settings():
    settings = {
        'user_agents': list_user_agents(),
        'proxies': list_proxies(),
        'mnemonics': list_mnemonics(),
        'rotation_interval': rotation_interval
    }
    with open(SETTINGS_FILE, 'wb') as f:
        pickle.dump(settings, f)
    log_activity("Settings saved")

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'rb') as f:
            settings = pickle.load(f)
        for ua in settings['user_agents']:
            add_user_agent(ua)
        for proxy in settings['proxies']:
            parts = proxy.split(':')
            if len(parts) == 3:
                ip, port, proxy_type = parts
                add_proxy(ip, port, proxy_type)
        for mnemonic in settings['mnemonics']:
            add_mnemonic(mnemonic)
        global rotation_interval
        rotation_interval = settings['rotation_interval']
        log_activity("Settings loaded")

def run_gui():
    load_settings()

    # Use ThemedTk to apply themes
    root = ThemedTk(theme="arc")
    root.title("Cryptocurrency Fraud Protection Tool")

    # Set the window size
    root.geometry("800x600")

    # Create a notebook for tabs
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)

    # Create frames for each relevant tab
    tab_program = ttk.Frame(notebook)
    tab_user_agent = ttk.Frame(notebook)
    tab_settings = ttk.Frame(notebook)

    # Add tabs to notebook
    notebook.add(tab_program, text="Program")
    notebook.add(tab_user_agent, text="UserAgent")
    notebook.add(tab_settings, text="Settings")

    # Create the Program tab with Start and Exit buttons
    def create_program_tab(frame):
        # Add a title label
        title_label = ttk.Label(frame, text="Crypto Fraud Protection Tool", font=("Helvetica", 16))
        title_label.pack(pady=10)

        # Add a button with a command to start the tool
        def on_start():
            try:
                user_agent = get_random_user_agent()
                # Log activity
                log_activity(f"User Agent selected: {user_agent}")
                # Update the UserAgent tab with the random user agent
                user_agent_var.set(f"User Agent: {user_agent}")
                notebook.select(tab_user_agent)
                # Start a background task
                threading.Thread(target=background_task).start()
            except Exception as e:
                log_activity(f"Error starting tool: {e}")
                messagebox.showerror("Error", f"Failed to start tool: {e}")

        start_button = ttk.Button(frame, text="Start", command=on_start)
        start_button.pack(pady=20)

        # Add a quit button to exit the application
        quit_button = ttk.Button(frame, text="Exit", command=lambda: [stop_rotation(), save_settings(), root.quit()])
        quit_button.pack(pady=10)

    # Simulated background task
    def background_task():
        try:
            time.sleep(5)  # Simulate a long operation
            message = "Background task completed!"
            log_activity(message)
            send_report_to_telegram(BOT_TOKEN, CHAT_ID, message)
            messagebox.showinfo("Background Task", message)
        except Exception as e:
            log_activity(f"Error in background task: {e}")
            send_report_to_telegram(BOT_TOKEN, CHAT_ID, f"Error in background task: {e}")

    # Call function to create Program tab
    create_program_tab(tab_program)

    # Create the UserAgent tab
    def create_user_agent_tab(frame):
        global user_agent_var, user_agents
        user_agent_var = tk.StringVar()
        user_agents = list_user_agents()
        user_agent_label = ttk.Label(frame, textvariable=user_agent_var, font=("Helvetica", 12), wraplength=700, justify="left")
        user_agent_label.pack(pady=10, padx=10)

        # Frame for adding/removing user agents
        user_agent_frame = ttk.Frame(frame)
        user_agent_frame.pack(fill=tk.X, padx=10, pady=5)

        # Listbox for displaying predefined user agents
        predefined_user_agent_listbox = tk.Listbox(user_agent_frame, height=10, width=80)
        predefined_user_agent_listbox.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        for ua in user_agents:
            predefined_user_agent_listbox.insert(tk.END, ua)

        def select_user_agent_action():
            selected_user_agent = predefined_user_agent_listbox.curselection()
            if selected_user_agent:
                user_agent = predefined_user_agent_listbox.get(selected_user_agent)
                user_agent_var.set(f"Selected User Agent: {user_agent}")
                log_activity(f"User Agent selected: {user_agent}")

        def remove_user_agent_action():
            selected_user_agent = predefined_user_agent_listbox.curselection()
            if selected_user_agent:
                user_agent = predefined_user_agent_listbox.get(selected_user_agent)
                predefined_user_agent_listbox.delete(selected_user_agent)
                user_agents.remove(user_agent)
                log_activity(f"User Agent removed: {user_agent}")

        select_user_agent_button = ttk.Button(user_agent_frame, text="Select User Agent", command=select_user_agent_action)
        select_user_agent_button.grid(row=1, column=0, padx=5, pady=5)

        remove_user_agent_button = ttk.Button(user_agent_frame, text="Remove User Agent", command=remove_user_agent_action)
        remove_user_agent_button.grid(row=1, column=1, padx=5, pady=5)

        user_agent_entry = ttk.Entry(user_agent_frame, width=80)
        user_agent_entry.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        def add_user_agent_action():
            user_agent = user_agent_entry.get()
            if user_agent:
                add_user_agent(user_agent)
                user_agent_entry.delete(0, tk.END)
                predefined_user_agent_listbox.insert(tk.END, user_agent)
                log_activity(f"User Agent added: {user_agent}")

        add_user_agent_button = ttk.Button(user_agent_frame, text="Add User Agent", command=add_user_agent_action)
        add_user_agent_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    # Call function to create UserAgent tab
    create_user_agent_tab(tab_user_agent)

    # Create the Settings tab
    def create_settings_tab(frame):
        settings_notebook = ttk.Notebook(frame)
        settings_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Sub-tabs for settings
        tab_proxies = ttk.Frame(settings_notebook)
        tab_mnemonics = ttk.Frame(settings_notebook)
        tab_browsers = ttk.Frame(settings_notebook)
        tab_rotation = ttk.Frame(settings_notebook)
        settings_notebook.add(tab_proxies, text="Proxies")
        settings_notebook.add(tab_mnemonics, text="Mnemonics")
        settings_notebook.add(tab_browsers, text="Browsers")
        settings_notebook.add(tab_rotation, text="Rotation")

        # Proxies tab content
        def create_proxies_tab(frame):
            # Top section with labels and entries
            top_frame = ttk.Frame(frame)
            top_frame.pack(fill=tk.X, padx=10, pady=5)

            ttk.Label(top_frame, text="Proxy IP:").grid(row=0, column=0, padx=5, pady=5)
            ip_entry = ttk.Entry(top_frame)
            ip_entry.grid(row=0, column=1, padx=5, pady=5)

            ttk.Label(top_frame, text="Port:").grid(row=0, column=2, padx=5, pady=5)
            port_entry = ttk.Entry(top_frame)
            port_entry.grid(row=0, column=3, padx=5, pady=5)

            ttk.Label(top_frame, text="Type:").grid(row=0, column=4, padx=5, pady=5)
            type_combo = ttk.Combobox(top_frame, values=["HTTP", "HTTPS", "SOCKS4", "SOCKS5"])
            type_combo.grid(row=0, column=5, padx=5, pady=5)
            type_combo.current(0)

            def on_add_proxy():
                try:
                    ip = ip_entry.get()
                    port = port_entry.get()
                    proxy_type = type_combo.get()
                    if ip and port and proxy_type:
                        add_proxy(ip, port, proxy_type)
                        proxy_listbox.insert(tk.END, f"{ip}:{port} ({proxy_type})")
                        ip_entry.delete(0, tk.END)
                        port_entry.delete(0, tk.END)
                        type_combo.current(0)
                        log_activity(f"Proxy added: {ip}:{port} ({proxy_type})")
                        send_report_to_telegram(BOT_TOKEN, CHAT_ID, f"Proxy added: {ip}:{port} ({proxy_type})")
                except Exception as e:
                    log_activity(f"Error adding proxy: {e}")
                    messagebox.showerror("Error", f"Failed to add proxy: {e}")

            def on_remove_proxy():
                try:
                    selected_proxy = proxy_listbox.curselection()
                    if selected_proxy:
                        proxy = proxy_listbox.get(selected_proxy)
                        remove_proxy(proxy)
                        proxy_listbox.delete(selected_proxy)
                        log_activity(f"Proxy removed: {proxy}")
                        send_report_to_telegram(BOT_TOKEN, CHAT_ID, f"Proxy removed: {proxy}")
                except Exception as e:
                    log_activity(f"Error removing proxy: {e}")
                    messagebox.showerror("Error", f"Failed to remove proxy: {e}")

            def on_activate_proxy():
                global active_proxy
                selected_proxy = proxy_listbox.curselection()
                if selected_proxy:
                    proxy = proxy_listbox.get(selected_proxy)
                    active_proxy = proxy
                    log_activity(f"Proxy activated: {proxy}")
                    send_report_to_telegram(BOT_TOKEN, CHAT_ID, f"Proxy activated: {proxy}")
                    # Highlight the active proxy
                    for i in range(proxy_listbox.size()):
                        if proxy_listbox.get(i) == proxy:
                            proxy_listbox.itemconfig(i, {'bg':'lightgreen'})
                        else:
                            proxy_listbox.itemconfig(i, {'bg':'white'})

            def on_deactivate_proxy():
                global active_proxy
                if active_proxy:
                    log_activity(f"Proxy deactivated: {active_proxy}")
                    send_report_to_telegram(BOT_TOKEN, CHAT_ID, f"Proxy deactivated: {active_proxy}")
                    active_proxy = None
                    # Remove highlight from all proxies
                    for i in range(proxy_listbox.size()):
                        proxy_listbox.itemconfig(i, {'bg':'white'})

            add_button = ttk.Button(top_frame, text="Add Proxy", command=on_add_proxy)
            add_button.grid(row=0, column=6, padx=5, pady=5)
            
            remove_button = ttk.Button(top_frame, text="Remove Proxy", command=on_remove_proxy)
            remove_button.grid(row=0, column=7, padx=5, pady=5)

            activate_button = ttk.Button(top_frame, text="Activate Proxy", command=on_activate_proxy)
            activate_button.grid(row=0, column=8, padx=5, pady=5)

            deactivate_button = ttk.Button(top_frame, text="Deactivate Proxy", command=on_deactivate_proxy)
            deactivate_button.grid(row=0, column=9, padx=5, pady=5)

            # Listbox for proxy list
            proxy_listbox = tk.Listbox(frame)
            proxy_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

            # Populate the listbox with existing proxies
            for proxy in list_proxies():
                proxy_listbox.insert(tk.END, proxy)

        create_proxies_tab(tab_proxies)

        # Mnemonics tab content
        def create_mnemonics_tab(frame):
            # Top section with labels and entries
            top_frame = ttk.Frame(frame)
            top_frame.pack(fill=tk.X, padx=10, pady=5)

            ttk.Label(top_frame, text="Mnemonic:").grid(row=0, column=0, padx=5, pady=5)
            mnemonic_entry = ttk.Entry(top_frame)
            mnemonic_entry.grid(row=0, column=1, padx=5, pady=5)

            def on_add_mnemonic():
                try:
                    mnemonic = mnemonic_entry.get()
                    if mnemonic:
                        add_mnemonic(mnemonic)
                        mnemonic_listbox.insert(tk.END, mnemonic)
                        mnemonic_entry.delete(0, tk.END)
                        log_activity(f"Mnemonic added: {mnemonic}")
                except Exception as e:
                    log_activity(f"Error adding mnemonic: {e}")
                    messagebox.showerror("Error", f"Failed to add mnemonic: {e}")

            def on_remove_mnemonic():
                try:
                    selected_mnemonic = mnemonic_listbox.curselection()
                    if selected_mnemonic:
                        mnemonic = mnemonic_listbox.get(selected_mnemonic)
                        remove_mnemonic(mnemonic)
                        mnemonic_listbox.delete(selected_mnemonic)
                        log_activity(f"Mnemonic removed: {mnemonic}")
                except Exception as e:
                    log_activity(f"Error removing mnemonic: {e}")
                    messagebox.showerror("Error", f"Failed to remove mnemonic: {e}")

            add_button = ttk.Button(top_frame, text="Add Mnemonic", command=on_add_mnemonic)
            add_button.grid(row=0, column=2, padx=5, pady=5)
            
            remove_button = ttk.Button(top_frame, text="Remove Mnemonic", command=on_remove_mnemonic)
            remove_button.grid(row=0, column=3, padx=5, pady=5)

            # Listbox for mnemonic list
            mnemonic_listbox = tk.Listbox(frame)
            mnemonic_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

            # Populate the listbox with existing mnemonics
            for mnemonic in list_mnemonics():
                mnemonic_listbox.insert(tk.END, mnemonic)

        create_mnemonics_tab(tab_mnemonics)

        # Browsers tab content
        def create_browsers_tab(frame):
            top_frame = ttk.Frame(frame)
            top_frame.pack(fill=tk.X, padx=10, pady=5)

            browsers_listbox = tk.Listbox(frame)
            browsers_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

            def on_add_browser():
                browser_path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")])
                if browser_path:
                    browsers_listbox.insert(tk.END, browser_path)
                    log_activity(f"Browser added: {browser_path}")

            def on_remove_browser():
                selected_browser = browsers_listbox.curselection()
                if selected_browser:
                    browser_path = browsers_listbox.get(selected_browser)
                    browsers_listbox.delete(selected_browser)
                    log_activity(f"Browser removed: {browser_path}")

            add_browser_button = ttk.Button(top_frame, text="Add Browser", command=on_add_browser)
            add_browser_button.grid(row=0, column=0, padx=5, pady=5)

            remove_browser_button = ttk.Button(top_frame, text="Remove Browser", command=on_remove_browser)
            remove_browser_button.grid(row=0, column=1, padx=5, pady=5)

            def on_open_browser():
                selected_browser = browsers_listbox.curselection()
                if selected_browser:
                    browser_path = browsers_listbox.get(selected_browser)
                    user_agent = get_random_user_agent()
                    proxy = get_random_proxy()
                    log_activity(f"Opening browser: {browser_path} with User Agent: {user_agent} and Proxy: {proxy}")
                    try:
                        if "chrome" in browser_path.lower():
                            subprocess.Popen([browser_path, f'--proxy-server={proxy}', f'--user-agent={user_agent}'])
                        elif "firefox" in browser_path.lower():
                            proxy_parts = proxy.split(":")
                            subprocess.Popen([browser_path, '-no-remote', f'--user-agent={user_agent}', f'--proxy-server={proxy_parts[0]}:{proxy_parts[1]}'])
                        else:
                            messagebox.showerror("Error", "Unsupported browser for proxy setup")
                    except Exception as e:
                        log_activity(f"Error opening browser: {e}")
                        messagebox.showerror("Error", f"Failed to open browser: {e}")

            open_browser_button = ttk.Button(top_frame, text="Open Browser", command=on_open_browser)
            open_browser_button.grid(row=0, column=2, padx=5, pady=5)

        create_browsers_tab(tab_browsers)

        # Rotation tab content
        def create_rotation_tab(frame):
            top_frame = ttk.Frame(frame)
            top_frame.pack(fill=tk.X, padx=10, pady=5)

            ttk.Label(top_frame, text="Rotation Interval (minutes):").grid(row=0, column=0, padx=5, pady=5)
            interval_entry = ttk.Entry(top_frame)
            interval_entry.grid(row=0, column=1, padx=5, pady=5)
            interval_entry.insert(0, str(rotation_interval))

            def on_set_interval():
                global rotation_interval
                interval = interval_entry.get()
                if interval.isdigit():
                    rotation_interval = int(interval)
                    log_activity(f"Set rotation interval to {rotation_interval} minutes")
                else:
                    messagebox.showerror("Error", "Invalid interval value")

            set_interval_button = ttk.Button(top_frame, text="Set Interval", command=on_set_interval)
            set_interval_button.grid(row=0, column=2, padx=5, pady=5)

            def on_start_rotation():
                start_rotation()
                log_activity("Started user agent rotation")
                messagebox.showinfo("Rotation", "User agent rotation started")

            def on_stop_rotation():
                stop_rotation()
                log_activity("Stopped user agent rotation")
                messagebox.showinfo("Rotation", "User agent rotation stopped")

            start_rotation_button = ttk.Button(top_frame, text="Start Rotation", command=on_start_rotation)
            start_rotation_button.grid(row=1, column=0, padx=5, pady=5)

            stop_rotation_button = ttk.Button(top_frame, text="Stop Rotation", command=on_stop_rotation)
            stop_rotation_button.grid(row=1, column=1, padx=5, pady=5)

        create_rotation_tab(tab_rotation)

    # Call function to create Settings tab
    create_settings_tab(tab_settings)

    # Run the main event loop
    root.mainloop()

if __name__ == '__main__':
    run_gui()
