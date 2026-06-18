from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client
import os

app = FastAPI(title="Benzene Control Plane - Mock Drill")

# Replace these with environment variables or temporary string credentials for dev
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class WorkerRegister(BaseModel):
    worker_ip: str
    port: int
    gpu_model: str
    vram_gb: int

class JobSubmit(BaseModel):
    client_name: str
    dataset_size_mb: int
    task_type: str  # e.g., "BATCH_LLM" or "INTERACTIVE_GAMING"

@app.post("/register-node")
def register_node(worker: WorkerRegister):
    data, count = supabase.table("nodes").insert(worker.dict()).execute()
    return {"status": "SUCCESS", "node_data": data[1][0]}

@app.post("/submit-job")
def submit_job(job: JobSubmit):
    # 1. Fetch available worker nodes from database
    nodes_query = supabase.table("nodes").select("*").eq("status", "IDLE").execute()
    available_nodes = nodes_query.data
    
    if len(available_nodes) < 1:
        raise HTTPException(status_code=400, detail="No available GPU nodes found to scale workload.")
    
    # 2. Simple Mock Orchestrator Assignment Logic
    assigned_worker = available_nodes[0]
    
    # If processing parallel loops, assign a master coordinator node (Simulated loop)
    assigned_master_id = assigned_worker["id"] if job.task_type == "BATCH_LLM" else None
    
    job_data = {
        "client_name": job.client_name,
        "dataset_size_mb": job.dataset_size_mb,
        "task_type": job.task_type,
        "status": "ASSIGNED",
        "worker_node_id": assigned_worker["id"],
        "master_node_id": assigned_master_id
    }
    
    # 3. Store structural layout in database and update node assignment states
    inserted_job = supabase.table("jobs").insert(job_data).execute()
    supabase.table("nodes").update({"status": "BUSY"}).eq("id", assigned_worker["id"]).execute()
    
    return {
        "message": "Orchestrator assigned computation layout successfully.",
        "assigned_layout": {
            "target_worker_ip": assigned_worker["worker_ip"],
            "target_port": assigned_worker["port"],
            "requires_consensus_master": True if assigned_master_id else False
        }
    }
