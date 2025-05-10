import asyncio
import logging
import tkinter as tk
from tkinter import messagebox

try:
    import websockets
except ModuleNotFoundError:
    print("This example relies on the 'websockets' package.")
    print("Please install it by running:")
    print("\n $ pip install websockets")
    import sys
    sys.exit(1)

from ocpp.v201 import ChargePoint as cp
from ocpp.v201 import call

logging.basicConfig(level=logging.INFO)

class ChargePoint(cp):
    async def send_heartbeat(self, interval):
        request = call.Heartbeat()
        while True:
            print("Sending heartbeat...")
            await self.call(request)
            await asyncio.sleep(interval)

    async def send_boot_notification(self):
        request = call.BootNotification(
            charging_station={"model": "Wallbox XYZ", "vendor_name": "anewone"},
            reason="PowerUp",
        )
        response = await self.call(request)

        if response.status == "Accepted":
            print("Connected to central system.")
            await self.send_heartbeat(response.interval)

    async def send_authorize(self, token: str):
        request = call.Authorize(
            id_token={"id_token": token, "type": "Central"}
        )
        response = await self.call(request)
        print(f"Authorization status: {response.id_token_info['status']}")

async def on_connect(host, token, heartbeat_interval, packet_speed):
    async with websockets.connect(
        f"ws://{host}:9000/CP_1", subprotocols=["ocpp2.0.1"]
    ) as ws:
        charge_point = ChargePoint("CP_1", ws)
        await asyncio.gather(
            charge_point.start(),
            charge_point.send_boot_notification(),
            charge_point.send_authorize(token),
        )

def start_client():
    host = host_entry.get()
    token = token_entry.get()
    try:
        heartbeat_interval = int(heartbeat_entry.get())
        packet_speed = int(packet_speed_entry.get())  # You can use this for additional features
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for intervals and speed.")
        return

    asyncio.run(on_connect(host, token, heartbeat_interval, packet_speed))

# GUI setup
root = tk.Tk()
root.title("OCPP Client")

tk.Label(root, text="Server Address:").grid(row=0, column=0, sticky="w")
host_entry = tk.Entry(root, width=30)
host_entry.grid(row=0, column=1)
host_entry.insert(0, "localhost")

tk.Label(root, text="Authorization Token:").grid(row=1, column=0, sticky="w")
token_entry = tk.Entry(root, width=30)
token_entry.grid(row=1, column=1)
token_entry.insert(0, "VALID123")

tk.Label(root, text="Heartbeat Interval (seconds):").grid(row=2, column=0, sticky="w")
heartbeat_entry = tk.Entry(root, width=30)
heartbeat_entry.grid(row=2, column=1)
heartbeat_entry.insert(0, "10")

tk.Label(root, text="Packet Speed (Mbps):").grid(row=3, column=0, sticky="w")
packet_speed_entry = tk.Entry(root, width=30)
packet_speed_entry.grid(row=3, column=1)
packet_speed_entry.insert(0, "100")

tk.Button(root, text="Start Client", command=start_client).grid(row=4, columnspan=2)

root.mainloop()
