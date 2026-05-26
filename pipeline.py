from google import genai
from models import AppConfig
import json
from validator import validate_and_repair

# PASTE YOUR NEW SECURE KEY HERE BEFORE RUNNING LOCALLY, 
# BUT REMOVE IT BEFORE UPLOADING TO GITHUB
GEMINI_KEY = "AIzaSyBH3sOhn3Cge3BjzbXGw8habAm7C0oeUbc"
# Initialize the client
client = genai.Client(api_key=GEMINI_KEY)

def generate_software_config(user_prompt: str):
    prompt = f"""
    You are a software architect compiler. 
    Task: Create a structured app configuration for: {user_prompt}
    
    CRITICAL RULES:
    1. The 'action' field inside a UIComponent MUST exactly match a 'path' from your API list (e.g., '/login' or '/tasks/add'). 
    2. If a UI component doesn't call an API, its action MUST be exactly "navigation".
    3. Do NOT write sentences or descriptions in the action field.
    
    Output ONLY valid JSON matching this schema:
    {json.dumps(AppConfig.model_json_schema(), indent=2)}
    """
    
    # We are using Gemini 3.5 Flash
    response = client.models.generate_content(
        model='gemini-3.5-flash',
        contents=prompt
    )
    
    # Clean the output
    raw_json = response.text.replace("```json", "").replace("```", "").strip()
    
    # Validate the JSON against models.py rules
    return AppConfig.model_validate_json(raw_json)

def run_auto_repair_pipeline(user_prompt: str, max_retries=2):
    # Step 1: Initial attempt
    config = generate_software_config(user_prompt)
    
    for attempt in range(max_retries):
        is_valid, errors = validate_and_repair(config)
        
        if is_valid:
            # It passed! Return the good config.
            return config, is_valid
            
        print(f"⚠️ Repair triggered! Attempt {attempt + 1}. Errors: {errors}")
        
        # Step 2: The Repair Prompt
        repair_prompt = f"""
        Original Request: {user_prompt}
        
        You made the following logical errors in your last attempt:
        {errors}
        
        Regenerate the JSON and FIX these specific errors. 
        Remember: UI actions MUST map to exact API paths.
        """
        
        # Ask the AI to try again with the repair instructions
        config = generate_software_config(repair_prompt)
        
    # If it fails after max retries, we give up so it doesn't loop forever
    return config, False