import tkinter as tk
from tkinter import ttk
import threading
import socket
import json
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class EVClientApp:
    def __init__(self, master):
        self.master = master
        self.master.title("EV - ISO 15118 + OCPP Simulation")
        self.master.geometry("500x500")
        self.auth_token = tk.StringVar()
        self.status_text = tk.StringVar(value="Enter token and click Start")
        self.battery_level = 0
        self.charging = False
        self.stop_charging = False

        tk.Label(master, text="EV Authentication Token:").pack(pady=5)
        tk.Entry(master, textvariable=self.auth_token).pack(pady=5)
        tk.Button(master, text="Start Charging", command=self.send_auth_request).pack(pady=10)
        tk.Label(master, textvariable=self.status_text).pack(pady=5)

        self.fig, self.ax = plt.subplots(figsize=(5, 2))
        self.ax.set_ylim(0, 100)
        self.ax.set_title("Battery Level (%)")
        self.line, = self.ax.plot([], [], color='green')
        self.canvas = FigureCanvasTkAgg(self.fig, master)
        self.canvas.get_tk_widget().pack(pady=10)
        self.x_data = []
        self.y_data = []

    def send_auth_request(self):
        token = self.auth_token.get().strip()
        if not token:
            self.status_text.set("Please enter an authentication token.")
            return

        self.status_text.set("Connecting to Charging Station...")
        thread = threading.Thread(target=self.connect_to_station, args=(token,))
        thread.start()

    def connect_to_station(self, token):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('localhost', 9090))
                request = json.dumps({"auth_token": token})
                s.sendall(request.encode())

                response = s.recv(1024).decode()
                data = json.loads(response)
                if data["status"] == "authorized":
                    self.status_text.set("Authentication successful. Charging started...")
                    self.charging = True
                    self.stop_charging = False
                    self.update_charging()
                elif data["status"] == "unauthorized":
                    self.status_text.set("Authentication failed.")
                else:
                    self.status_text.set("Server error or unavailable.")
        except Exception as e:
            self.status_text.set(f"Error: {e}")

    def update_charging(self):
        def charging_loop():
            while self.battery_level < 100 and not self.stop_charging:
                time.sleep(1)
                self.battery_level += 5
                self.x_data.append(len(self.x_data))
                self.y_data.append(self.battery_level)
                self.line.set_data(self.x_data, self.y_data)
                self.ax.set_xlim(0, len(self.x_data))
                self.canvas.draw()
                if self.battery_level >= 100:
                    self.status_text.set("Charging complete.")
                    self.charging = False
        threading.Thread(target=charging_loop).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = EVClientApp(root)
    root.mainloop()
