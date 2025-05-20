import platform
import socket
import uuid
import psutil
import requests
import os
import pkg_resources
from datetime import datetime

def get_system_info():
    return {
        "OS": platform.system(),
        "OS Version": platform.version(),
        "Architecture": platform.machine(),
        "Processor": platform.processor(),
        "CPU Cores": psutil.cpu_count(logical=False),
        "Logical CPUs": psutil.cpu_count(logical=True),
        "RAM (GB)": round(psutil.virtual_memory().total / (1024 ** 3), 2),
    }

def get_network_info():
    hostname = socket.gethostname()
    try:
        ip_address = socket.gethostbyname(hostname)
    except socket.gaierror:
        ip_address = "Unavailable"
    mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff)
                            for i in range(0, 8*6, 8)][::-1])
    return {
        "Hostname": hostname,
        "IP Address": ip_address,
        "MAC Address": mac_address,
    }

def get_disk_info():
    disk_usage = psutil.disk_usage('/')
    return {
        "Total Disk Space (GB)": round(disk_usage.total / (1024 ** 3), 2),
        "Used Disk Space (GB)": round(disk_usage.used / (1024 ** 3), 2),
        "Free Disk Space (GB)": round(disk_usage.free / (1024 ** 3), 2),
        "Disk Usage (%)": disk_usage.percent
    }

def get_installed_packages():
    return [f"{pkg.key}=={pkg.version}" for pkg in pkg_resources.working_set]

def get_location_info():
    try:
        response = requests.get('https://ipinfo.io/json', timeout=5)
        return response.json()
    except requests.RequestException:
        return {"error": "Could not retrieve location info"}

def save_info_to_txt(info):
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(script_dir, "output")
        os.makedirs(output_dir, exist_ok=True)

        filepath = os.path.join(output_dir, "Device-Log.txt")

        with open(filepath, "w", encoding="utf-8") as f:
            for section, content in info.items():
                f.write(f"=== {section} ===\n")
                if isinstance(content, dict):
                    for key, value in content.items():
                        f.write(f"{key}: {value}\n")
                elif isinstance(content, list):
                    for item in content:
                        f.write(f"{item}\n")
                f.write("\n")
    except:
        pass  # Silent fail

def main():
    info = {
        "System Info": get_system_info(),
        "Network Info": get_network_info(),
        "Disk Info": get_disk_info(),
        "Location Info": get_location_info(),
        "Installed Packages": get_installed_packages()
    }

    save_info_to_txt(info)

if __name__ == "__main__":
    main()
