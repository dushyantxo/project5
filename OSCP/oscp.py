import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import csv

class EV:
    def __init__(self, ev_id, required_kwh):
        self.id = ev_id
        self.required_kwh = required_kwh
        self.charged = 0

class OSCP_GUI:
    def __init__(self, master):
        self.master = master
        master.title("Realistic OSCP 24-Hour EV Charging Simulation")

        self.ev_list = []  # Active EVs
        self.ev_charging_profile = [0] * 24
        self.capacity_forecast = [random.randint(100, 200) for _ in range(24)]  # Initial capacity forecast
        self.hour = 0
        self.ev_counter = 0  # To assign unique EV IDs
        self.day_counter = 0  # Track the day

        self.figure, self.ax = plt.subplots(figsize=(10, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master)
        self.canvas.get_tk_widget().pack()

        self.log = tk.Text(master, height=12, width=80)
        self.log.pack(pady=10)

        self.start_btn = ttk.Button(master, text="Start Simulation", command=self.start_simulation)
        self.start_btn.pack()

    def save_to_csv(self, day):
        """Save the red and blue data for the current day to a CSV file."""
        with open('charging_data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            for i in range(24):
                writer.writerow([i, self.ev_charging_profile[i], self.capacity_forecast[i]])

    def read_csv_and_predict_blue(self):
        """Read past data from the CSV file, calculate the average red data and update the blue data."""
        past_red_data = [[] for _ in range(24)]  # Store red data for each hour

        try:
            with open('charging_data.csv', mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    hour = int(row[0])
                    red = float(row[1])
                    past_red_data[hour].append(red)
        except FileNotFoundError:
            # If the CSV doesn't exist yet, skip
            pass

        # Calculate the average red data for each hour from the previous day
        predicted_blue_data = []
        for i in range(24):
            if past_red_data[i]:
                avg_red = sum(past_red_data[i]) / len(past_red_data[i])
            else:
                avg_red = 0

            # Predict blue data: Average red from previous day + 5
            predicted_blue = avg_red + 50
            predicted_blue_data.append(predicted_blue)

        return predicted_blue_data

    def simulate_hour(self):
        if self.hour >= 24:
            # At the end of the day, record the charging profile and adjust for the next day
            self.save_to_csv(self.day_counter)

            # Predict the blue data for the next day based on past data
            self.capacity_forecast = self.read_csv_and_predict_blue()

            self.log.insert(tk.END, f"\n✅ Day {self.day_counter + 1} complete!\n")
            self.day_counter += 1
            self.hour = 0
            self.ev_charging_profile = [0] * 24  # Reset charging profile for the next day

            if self.day_counter >= 7:  # Let's say the simulation ends after 7 days
                self.log.insert(tk.END, "\n✅ Simulation ended after 7 days!\n")
                return

        # 🔄 Randomly generate 0 to 3 new EVs
        new_evs = random.randint(0, 3)
        for _ in range(new_evs):
            required_kwh = random.randint(10, 30)
            ev = EV(f"EV{self.ev_counter}", required_kwh)
            self.ev_list.append(ev)
            self.ev_counter += 1
            self.log.insert(tk.END, f"[Hour {self.hour}] New EV arrived: {ev.id} needs {ev.required_kwh} kWh\n")

        available_capacity = self.capacity_forecast[self.hour]
        active_evs = [ev for ev in self.ev_list if ev.charged < ev.required_kwh]

        if active_evs:
            total_used = 0
            random.shuffle(active_evs)  # Simulate a bit of chaos
            for ev in active_evs:
                if available_capacity <= 0:
                    break
                max_charge_this_hour = min(7, ev.required_kwh - ev.charged, available_capacity)
                ev.charged += max_charge_this_hour
                available_capacity -= max_charge_this_hour
                total_used += max_charge_this_hour
                self.log.insert(tk.END, f"[Hour {self.hour}] {ev.id} charged {max_charge_this_hour} kWh (Total: {ev.charged}/{ev.required_kwh})\n")

            # Ensure that the total charging used does not exceed the forecasted capacity
            self.ev_charging_profile[self.hour] = min(total_used, self.capacity_forecast[self.hour])
        else:
            self.log.insert(tk.END, f"[Hour {self.hour}] No EVs to charge.\n")

        self.draw_chart()
        self.hour += 1
        self.master.after(1000, self.simulate_hour)

    def draw_chart(self):
        self.ax.clear()
        hours = list(range(24))
        self.ax.bar(hours, self.capacity_forecast, color='skyblue', label='Forecasted Capacity')
        self.ax.bar(hours, self.ev_charging_profile, color='red', label='EV Charging Used', alpha=0.7)

        self.ax.set_ylim(0, 220)
        self.ax.set_xlabel("Hour")
        self.ax.set_ylabel("Amps / Energy")
        self.ax.set_title("OSCP - Realistic EV Charging Over 24 Hours")
        self.ax.legend()
        self.canvas.draw()

    def start_simulation(self):
        self.start_btn.config(state="disabled")
        self.simulate_hour()

if __name__ == "__main__":
    root = tk.Tk()
    app = OSCP_GUI(root)
    root.mainloop()
