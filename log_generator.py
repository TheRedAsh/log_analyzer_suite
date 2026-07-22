#!/usr/bin/env python3
import time
import random

print("[*] Mock Authentication Log Generator Started...")
print("[*] Writing live events to 'sandbox_auth.log'. Press Ctrl+C to stop.")

ips = ["192.168.1.45", "10.0.0.12", "172.16.5.9", "192.168.1.100"]

with open("sandbox_auth.log", "w") as f:
    f.write("--- SYSTEM INITIALIZED ---\n")

while True:
    time.sleep(random.uniform(0.5, 2.5)) # Simulation delay
    target_ip = random.choice(ips)
    
    # Randomly generate successful or failed attempts
    event_type = random.choices(["SUCCESS", "FAILED"], weights=[20, 80])[0]
    timestamp = time.strftime("%b %d %H:%M:%S")
    
    with open("sandbox_auth.log", "a") as f:
        if event_type == "FAILED":
            f.write(f"{timestamp} kali-server sshd[1234]: Failed password for invalid user admin from {target_ip} port 49231 ssh2\n")
        else:
            f.write(f"{timestamp} kali-server sshd[1234]: Accepted password for root from 192.168.1.1 port 51234 ssh2\n")
