import requests

def check_gleif_status(entity_name):
    # The API filter key must be 'entity.legalName' (without the trailing .name)
    url = "https://api.gleif.org/api/v1/lei-records"
    params = {"filter[entity.legalName]": entity_name}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        print(f"\n--- AUDIT REPORT FOR: {entity_name} ---")
        
        if not data.get('data'):
            print("STATUS: 404 (Not Found)")
            print("NOTICE: Entity is not yet indexed in the GLEIF Global Registry.")
            return

        for record in data['data']:
            attr = record['attributes']
            print(f"ENTITY: {attr['entity']['legalName']['name']}")
            print(f"LEI:    {attr['lei']}")
            print(f"STATUS: {attr['registration']['status']}")
            print("-" * 40)
            
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    # Check for your specific trust name
    check_gleif_status("Travis Ryle Private Bank Estate and Trust")
