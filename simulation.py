import requests
import time

BASE_URL = "http://127.0.0.1:8000"

def run_simulation():
    print(" Starting Benzene Control Plane Mock Simulation...")
    
    # Step 1: Simulate a decentralized GPU provider booting up
    print("\n[1/3] Registering isolated Worker Node (Simulated RTX 4090)...")
    worker_payload = {
        "worker_ip": "192.168.1.50",
        "port": 9000,
        "gpu_model": "NVIDIA RTX 4090",
        "vram_gb": 24
    }
    r1 = requests.post(f"{BASE_URL}/register-node", json=worker_payload)
    print("Server Response:", r1.json())
    
    time.sleep(2)
    
    # Step 2: Simulate an AI engineer submitting a large model execution script
    print("\n[2/3] Client submitting AI pipeline metadata request (4GB Dataset)...")
    job_payload = {
        "client_name": "Ravager_Client_Session",
        "dataset_size_mb": 4096,
        "task_type": "BATCH_LLM_PEFT"
    }
    r2 = requests.post(f"{BASE_URL}/submit-job", json=job_payload)
    print("Server Response:", r2.json())
    
    print("\n Simulation complete! Verify database state tracking entries inside Supabase.")

if __name__ == "__main__":
    run_simulation()
