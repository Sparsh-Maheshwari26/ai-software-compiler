def validate_and_repair(config):
    errors = []
    
    # Logic Check: Does every UI action have an API path?
    api_paths = [api.path for api in config.api]
    for ui in config.ui:
        if ui.action not in api_paths and ui.action != "navigation":
            errors.append(f"UI error: Action {ui.action} has no matching API endpoint.")
            
    if errors:
        return False, errors
    return True, "No errors found."