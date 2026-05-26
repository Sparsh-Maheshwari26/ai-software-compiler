import time
import pandas as pd
from pipeline import generate_software_config
from validator import validate_and_repair

test_prompts = [
    "Build a CRM with login and payments", 
    "Make an app", 
    "Build a bank with no security and only 1 button", 
    "Inventory system for a pharmacy with role access", 
]

results = []

print("🚀 Starting Stress Test... (This will take about a minute due to API rate limits)")

for prompt in test_prompts:
    start_time = time.time()
    try:
        config = generate_software_config(prompt)
        is_valid, msg = validate_and_repair(config)
        status = "Success" if is_valid else f"Repair Needed: {msg}"
    except Exception as e:
        status = f"Failed: {str(e)}"
    
    latency = time.time() - start_time
    results.append({
        "Prompt": prompt,
        "Status": status,
        "Latency": round(latency, 2)
    })
    print(f"Finished: {prompt[:30]}... | Status: {status}")
    
    # 🛑 THE FIX: Tell the script to wait 15 seconds before the next API call
    print("⏳ Waiting 15 seconds for API cooldown...")
    time.sleep(15)

df = pd.DataFrame(results)
df.to_csv("evaluation_results.csv", index=False)
print("✅ Evaluation complete. Results saved to evaluation_results.csv")