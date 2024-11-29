# import subprocess
# import sys
# import os
# import ctypes
# import tkinter as tk
# from tkinter import messagebox
# import threading


# def is_admin():
#     """Check if the script is running with administrator privileges."""
#     try:
#         return ctypes.windll.shell32.IsUserAnAdmin()
#     except:
#         return False


# def run_as_admin():
#     """Re-run the script with administrator privileges if not already."""
#     try:
#         script = os.path.abspath(sys.argv[0])
#         ctypes.windll.shell32.ShellExecuteW(
#             None, "runas", sys.executable, script, None, 1
#         )
#         sys.exit(0)
#     except Exception as e:
#         messagebox.showerror("Admin Error", f"Failed to get admin privileges: {e}")
#         sys.exit(1)


# def check_server_address(server_address):
#     """Check if the VPN server address resolves properly."""
#     try:
#         result = subprocess.run(
#             ["nslookup", server_address], capture_output=True, text=True
#         )
#         if "Non-existent domain" in result.stdout or result.returncode != 0:
#             messagebox.showerror(
#                 "DNS Error", f"Cannot resolve VPN server address: {server_address}"
#             )
#             return None
#         else:
#             # Extract the resolved IP address from the nslookup output
#             for line in result.stdout.split("\n"):
#                 if "Address:" in line:
#                     return line.split(":")[1].strip()
#             return server_address
#     except Exception as e:
#         messagebox.showerror("DNS Error", f"Error checking server address: {e}")
#         return None


# def vpn_exists(vpn_name):
#     """Check if the VPN connection already exists."""
#     try:
#         result = subprocess.run(
#             ["powershell", "-Command", f"Get-VpnConnection -Name '{vpn_name}'"],
#             capture_output=True,
#             text=True,
#         )
#         return result.returncode == 0
#     except Exception as e:
#         messagebox.showerror("VPN Error", f"Failed to check VPN connection: {e}")
#         return False


# def create_vpn(vpn_name, vpn_server):
#     """Create a VPN connection."""
#     if not check_server_address(vpn_server):
#         return False

#     if vpn_exists(vpn_name):
#         messagebox.showinfo("VPN Status", f"VPN '{vpn_name}' already exists.")
#         return True

#     try:
#         create_command = (
#             f'powershell.exe -Command "Add-VpnConnection '
#             f"-Name '{vpn_name}' "
#             f"-ServerAddress '{vpn_server}' "
#             f"-TunnelType L2tp "
#             f"-EncryptionLevel Required "
#             f"-AuthenticationMethod MSChapv2 "
#             f"-AllUserConnection "
#             f'-Force"'
#         )
#         result = subprocess.run(
#             create_command, shell=True, capture_output=True, text=True
#         )
#         if result.returncode != 0:
#             messagebox.showerror(
#                 "VPN Creation Error",
#                 f"Failed to create VPN:\n{result.stderr or result.stdout}",
#             )
#             return False

#         messagebox.showinfo("VPN Status", f"VPN '{vpn_name}' created successfully!")
#         return True
#     except Exception as e:
#         messagebox.showerror("VPN Error", f"Unexpected error creating VPN: {e}")
#         return False


# def start_vpn(vpn_name, vpn_username, vpn_password):
#     """Start the VPN connection."""
#     try:
#         result = subprocess.run(
#             f"rasdial {vpn_name} {vpn_username} {vpn_password}",
#             shell=True,
#             capture_output=True,
#             text=True,
#         )
#         if result.returncode == 0:
#             messagebox.showinfo("VPN Status", f"VPN '{vpn_name}' started successfully!")
#         else:
#             messagebox.showerror(
#                 "VPN Connection Error",
#                 f"Failed to start VPN:\n{result.stderr or result.stdout}",
#             )
#     except Exception as e:
#         messagebox.showerror("VPN Error", f"Unexpected error starting VPN: {e}")


# def stop_vpn():
#     """Disconnect the VPN connection."""
#     try:
#         result = subprocess.run(
#             "rasdial /disconnect", shell=True, capture_output=True, text=True
#         )
#         if result.returncode == 0:
#             messagebox.showinfo("VPN Status", "VPN disconnected successfully!")
#         else:
#             messagebox.showerror(
#                 "VPN Disconnection Error",
#                 f"Failed to disconnect VPN:\n{result.stderr or result.stdout}",
#             )
#     except Exception as e:
#         messagebox.showerror("VPN Error", f"Unexpected error stopping VPN: {e}")


# def create_gui():
#     """Create the main GUI for the VPN tool."""
#     root = tk.Tk()
#     root.title("VPN Manager")

#     vpn_name = "DemoVPN"
#     vpn_server = check_server_address("demo.vpnserver.com")
#     if vpn_server is None:
#         root.destroy()
#         return

#     vpn_username = "demo_user"
#     vpn_password = "demo_password"

#     # Ensure the VPN is created
#     if not create_vpn(vpn_name, vpn_server):
#         root.destroy()
#         return

#     tk.Button(
#         root,
#         text="Start VPN",
#         command=lambda: threading.Thread(
#             target=start_vpn, args=(vpn_name, vpn_username, vpn_password)
#         ).start(),
#         bg="green",
#         fg="white",
#         width=20,
#     ).pack(pady=10)

#     tk.Button(
#         root,
#         text="Stop VPN",
#         command=lambda: threading.Thread(target=stop_vpn).start(),
#         bg="red",
#         fg="white",
#         width=20,
#     ).pack(pady=10)

#     root.geometry("300x150")
#     root.mainloop()


# if __name__ == "__main__":
#     if not is_admin():
#         run_as_admin()
#     create_gui()


# with api

import subprocess
import sys
import os
import ctypes
import tkinter as tk
from tkinter import messagebox
import threading
import requests
import json


def is_admin():
    """Check if the script is running with administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    """Re-run the script with administrator privileges if not already."""
    try:
        script = os.path.abspath(sys.argv[0])
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, script, None, 1
        )
        sys.exit(0)
    except Exception as e:
        messagebox.showerror("Admin Error", f"Failed to get admin privileges: {e}")
        sys.exit(1)


def check_server_address(server_address):
    """Check if the VPN server address resolves properly."""
    try:
        result = subprocess.run(
            ["nslookup", server_address], capture_output=True, text=True
        )
        if "Non-existent domain" in result.stdout or result.returncode != 0:
            messagebox.showerror(
                "DNS Error", f"Cannot resolve VPN server address: {server_address}"
            )
            return None
        else:
            # Extract the resolved IP address from the nslookup output
            for line in result.stdout.split("\n"):
                if "Address:" in line:
                    return line.split(":")[1].strip()
            return server_address
    except Exception as e:
        messagebox.showerror("DNS Error", f"Error checking server address: {e}")
        return None


def check_server_ip(server_url):
    """
    Check server IP and status using an external API.
    This function attempts to verify the server's connectivity and retrieve its IP.

    :param server_url: The base URL of the server to check
    :return: Dictionary with server status information
    """
    try:
        # First, try a health check endpoint on your server
        health_response = requests.get(f"{server_url}/health", timeout=10)

        # Try an IP checking API as a secondary verification
        ip_response = requests.get("https://api.ipify.org?format=json", timeout=10)

        server_details = {
            "server_health": health_response.status_code == 200,
            "server_health_message": (
                health_response.text
                if health_response.status_code == 200
                else "Health check failed"
            ),
            "current_public_ip": ip_response.json().get("ip", "Unable to retrieve IP"),
            "server_url": server_url,
        }

        return server_details

    except requests.RequestException as e:
        return {
            "server_health": False,
            "server_health_message": str(e),
            "current_public_ip": "Unable to retrieve IP",
            "server_url": server_url,
        }


def vpn_exists(vpn_name):
    """Check if the VPN connection already exists."""
    try:
        result = subprocess.run(
            ["powershell", "-Command", f"Get-VpnConnection -Name '{vpn_name}'"],
            capture_output=True,
            text=True,
        )
        return result.returncode == 0
    except Exception as e:
        messagebox.showerror("VPN Error", f"Failed to check VPN connection: {e}")
        return False


def create_vpn(vpn_name, vpn_server):
    """Create a VPN connection."""
    if not check_server_address(vpn_server):
        return False

    if vpn_exists(vpn_name):
        messagebox.showinfo("VPN Status", f"VPN '{vpn_name}' already exists.")
        return True

    try:
        create_command = (
            f'powershell.exe -Command "Add-VpnConnection '
            f"-Name '{vpn_name}' "
            f"-ServerAddress '{vpn_server}' "
            f"-TunnelType L2tp "
            f"-EncryptionLevel Required "
            f"-AuthenticationMethod MSChapv2 "
            f"-AllUserConnection "
            f'-Force"'
        )
        result = subprocess.run(
            create_command, shell=True, capture_output=True, text=True
        )
        if result.returncode != 0:
            messagebox.showerror(
                "VPN Creation Error",
                f"Failed to create VPN:\n{result.stderr or result.stdout}",
            )
            return False

        messagebox.showinfo("VPN Status", f"VPN '{vpn_name}' created successfully!")
        return True
    except Exception as e:
        messagebox.showerror("VPN Error", f"Unexpected error creating VPN: {e}")
        return False


def start_vpn(vpn_name, vpn_username, vpn_password):
    """Start the VPN connection."""
    try:
        result = subprocess.run(
            f"rasdial {vpn_name} {vpn_username} {vpn_password}",
            shell=True,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            messagebox.showinfo("VPN Status", f"VPN '{vpn_name}' started successfully!")
        else:
            messagebox.showerror(
                "VPN Connection Error",
                f"Failed to start VPN:\n{result.stderr or result.stdout}",
            )
    except Exception as e:
        messagebox.showerror("VPN Error", f"Unexpected error starting VPN: {e}")


def stop_vpn():
    """Disconnect the VPN connection."""
    try:
        result = subprocess.run(
            "rasdial /disconnect", shell=True, capture_output=True, text=True
        )
        if result.returncode == 0:
            messagebox.showinfo("VPN Status", "VPN disconnected successfully!")
        else:
            messagebox.showerror(
                "VPN Disconnection Error",
                f"Failed to disconnect VPN:\n{result.stderr or result.stdout}",
            )
    except Exception as e:
        messagebox.showerror("VPN Error", f"Unexpected error stopping VPN: {e}")


def create_gui():
    """Create the main GUI for the VPN tool."""
    root = tk.Tk()
    root.title("VPN Manager")

    # Configuration for your specific setup
    vpn_name = "DemoVPN"
    vpn_server = check_server_address("demo.vpnserver.com")
    vpn_server_url = "https://gempixel.com/products/premium-url-shortener"  # Replace with your actual server URL
    vpn_username = "demo_user"
    vpn_password = "demo_password"

    if vpn_server is None:
        root.destroy()
        return

    # Ensure the VPN is created
    if not create_vpn(vpn_name, vpn_server):
        root.destroy()
        return

    # Server Check Status Label
    server_status_label = tk.Label(root, text="Server Status: Checking...", fg="blue")
    server_status_label.pack(pady=5)

    def update_server_status():
        """Periodically check server status and update the label."""
        server_details = check_server_ip(vpn_server_url)

        if server_details["server_health"]:
            status_text = f"Server OK | IP: {server_details['current_public_ip']}"
            server_status_label.config(text=status_text, fg="green")
        else:
            status_text = (
                f"Server Down | Error: {server_details['server_health_message']}"
            )
            server_status_label.config(text=status_text, fg="red")

        # Optional: Schedule next check after 5 minutes
        root.after(300000, update_server_status)

    # Initial server status check
    update_server_status()

    tk.Button(
        root,
        text="Start VPN",
        command=lambda: threading.Thread(
            target=start_vpn, args=(vpn_name, vpn_username, vpn_password)
        ).start(),
        bg="green",
        fg="white",
        width=20,
    ).pack(pady=10)

    tk.Button(
        root,
        text="Stop VPN",
        command=lambda: threading.Thread(target=stop_vpn).start(),
        bg="red",
        fg="white",
        width=20,
    ).pack(pady=10)

    root.geometry("350x250")
    root.mainloop()


if __name__ == "__main__":
    if not is_admin():
        run_as_admin()
    create_gui()
