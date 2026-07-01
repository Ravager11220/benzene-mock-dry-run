import socket
import json
import requests

# 1. Configuration
COORDINATOR_URL = "https://setting-gurgle-dropper.ngrok-free.dev"  # Update with your central server URL
MY_PUBLIC_IP = "YOUR_FRIENDS_PUBLIC_IP"        # The public IP of your friend's network
PORT = 9000                                    # Port to open for data transfer

def register_with_backend():
    payload = {
        "worker_ip": MY_PUBLIC_IP,
        "port": PORT,
        "gpu_model": "RTX 4090",
        "vram_gb": 24
    }
    try:
        response = requests.post(f"{COORDINATOR_URL}/register-node", json=payload)
        print(f"[*] Registered with Benzene Backend: {response.json()}")
    except Exception as e:
        print(f"[-] Registration failed: {e}")

'''def start_data_plane_listener():
    # Set up a reusable TCP stream socket
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(("0.0.0.0", PORT))
    server_sock.listen(1)
    
    print(f"[*] Data Plane Active: Listening for client workloads on port {PORT}...")
    
    while True:
        conn, addr = server_sock.accept()
        print(f"\n[+] Direct peer connection established from Client: {addr}")
        
        # Receive the chunk stream length-prefixed JSON header or payload
        data = conn.recv(1024)
        if data:
            print(f"[#] Received workload metadata/payload from client: {data.decode('utf-8')}")
            
            # Simulate a brief processing calculation loop
            print("[*] Processing computational workload in sandboxed runtime...")
            
            # Send the execution success status acknowledgment back over the exact same socket
            conn.sendAll(b"SUCCESS: Workload computed by Benzene Worker Daemon via direct TCP channel.")
        
        conn.close()
        print("[-] Data channel closed cleanly.")
'''

if __name__ == "__main__":
    register_with_backend()
    #start_data_plane_listener()