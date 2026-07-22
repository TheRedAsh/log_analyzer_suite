#!/usr/bin/env python3
import os
import re
import time
import sys

# ANSI Terminal Colors for Security Alert UI
RED = "\033[1;31m"
YELLOW = "\033[1;33m"
GREEN = "\033[1;32m"
RESET = "\033[0m"

print(f"""
============================================================
   🛡️  AUTOMATED REAL-TIME BRUTE-FORCE DETECTION SYSTEM 🛡️
============================================================
""")

# Configurations
LOG_FILE = "sandbox_auth.log"
FAILED_THRESHOLD = 5  # Alert trigger limit
failed_attempts_tracker = {}  # State Table to log IP counters

# Regex pattern to match standard Linux SSH failed login logs
# Sample: Feb 20 14:21:05 server sshd[1]: Failed password for root from 192.168.1.45 ...
FAILED_LOG_PATTERN = r"Failed password for.*from\s+([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})"

def monitor_log_stream():
    """Simulates 'tail -f' core mechanics to read real-time additions."""
    if not os.path.exists(LOG_FILE):
        print(f"[*] Waiting for log file '{LOG_FILE}' to be initialized...")
        while not os.path.exists(LOG_FILE):
            time.sleep(1)

    print(f"[+] Active Connection Established with {LOG_FILE}")
    print(f"[*] Monitoring infrastructure thresholds (Max Allowed Fails: {FAILED_THRESHOLD})...\n")

    with open(LOG_FILE, "r") as f:
        # Move pointer directly to the end of the current file
        f.seek(0, os.SEEK_END)
        
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)  # Sleep briefly to preserve CPU registers
                continue
                
            process_log_line(line)

def process_log_line(log_line):
    """Parses line against regex definitions and increments risk metrics."""
    match = re.search(FAILED_LOG_PATTERN, log_line)
    
    if match:
        source_ip = match.group(1)
        
        # Update State Table
        if source_ip not in failed_attempts_tracker:
            failed_attempts_tracker[source_ip] = 1
        else:
            failed_attempts_tracker[source_ip] += 1
            
        current_fails = failed_attempts_tracker[source_ip]
        print(f"{YELLOW}[!] Failed attempt detected from {source_ip} | Total: {current_fails}/{FAILED_THRESHOLD}{RESET}")
        
        # Check Alert Condition Matrix
        if current_fails >= FAILED_THRESHOLD:
            print(f"\n{RED}[🚨 ALERT] CRITICAL BRUTE-FORCE ATTACK DETECTED!{RESET}")
            print(f"{RED}[🚨 TARGET IP] : {source_ip}{RESET}")
            print(f"{RED}[🚨 ACTION]    : Suggesting immediate firewall block rules for {source_ip}{RESET}\n")
            # Reset counter after alert execution to avoid loop flood
            failed_attempts_tracker[source_ip] = 0
    else:
        if "Accepted" in log_line:
            print(f"{GREEN}[+] Legitimate user successfully authenticated via SSH.{RESET}")

if __name__ == "__main__":
    try:
        monitor_log_stream()
    except KeyboardInterrupt:
        print("\n[-] Log Monitoring Engine stopped safely by administrator command.")
        sys.exit(0)
