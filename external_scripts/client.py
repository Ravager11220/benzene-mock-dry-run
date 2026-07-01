import requests
import socket
import json

COORDINATOR_URL = "https://setting-gurgle-dropper.ngrok-free.dev"  

def submit_job_and_stream():
    # submit jobparameters to control plane
    job_payload = {
        "client_name": "Team Benzene Client Pro",
        "dataset_size_mb": 4096, 
        "task_type": "BATCH_LLM"
    }
    
    print("[*] Contacting Benzene Control Plane to request dynamic node routing...")
    response = requests.post(f"{COORDINATOR_URL}/submit-job", json=job_payload)
    
    if response.status_code != 200:
        print(f"[-] Orchestration request failed: {response.text}")
        return
        
    result_metadata = response.json()
    print(f"[+] Control Plane Response received:\n{json.dumps(result_metadata, indent=2)}")
    
    # extract dataplane layout
    layout = result_metadata.get("assigned_layout", {})
    worker_ip = layout.get("target_worker_ip")
    worker_port = layout.get("target_port")
    
    if not worker_ip or not worker_port:
        print("[-] Missing worker connection route details from layout metadata.")
        return
        
    # 3. Action Phase: Establish the Peer-to-Peer Data Plane connection
    '''print(f"\n[!] CONTROL PLANE DECOUPLED: Activating direct Data Channel to Worker at {worker_ip}:{worker_port}")
    
    try:
        # Create standard TCP socket and connect directly to your friend's machine
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect((worker_ip, int(worker_port)))
        
        # Simulate passing the workload task instructions or chunk metadata over the raw line
        workload_token = f"WORKLOAD_START_TOKEN:DATASET_SIZE_MB:{job_payload['dataset_size_mb']}"
        client_sock.send(workload_token.encode('utf-8'))
        print("[*] Stream data packet sent successfully over direct socket.")
        
        # Keep connection open to listen for the result status response back
        worker_reply = client_sock.recv(1024)
        print(f"[+] Message returned directly from Worker Node: {worker_reply.decode('utf-8')}")
        
    except Exception as e:
        print(f"[-] Data plane pipeline connection error: {e}")
    finally:
        client_sock.close()
        print("[*] Client execution sequence terminated.")
'''

if __name__ == "__main__":
    submit_job_and_stream()