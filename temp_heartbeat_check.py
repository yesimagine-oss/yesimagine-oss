from gep_a2a_client import GAPA2AClient
import os

# Create client with node credentials
client = GAPA2AClient(
    node_id="node_cdd0bc78f3a6d99b",
    node_key="9f5136963d7298805e33d7e1e2773dfdb50e71cad434a9ce5789611af3339711",
    base_url="https://evomap.ai"
)

# Send heartbeat request
response = client.heartbeat()
print("Heartbeat response:")
print(json.dumps(response, indent=2))

# Check status
status = client.hello()
print("\nNode status:")
print(json.dumps(status, indent=2))