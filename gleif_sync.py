import requests
import json

def fetch_gleif_data(name):
    # Using the GLEIF v1 API to search by legal name
    url = f"https://api.gleif.org/api/v1/lei-records?filter[entity.legalName]={name}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def sync():
    with open('records_audit.json', 'r') as f:
        local_data = json.load(f)
    
    sync_results = []
    print(f"{'ENTITY':<30} | {'GLEIF STATUS':<15} | {'LEI':<20}")
    print("-" * 70)

    for record in local_data:
        entity_name = record.get('entity')
        # We only want to sync corporate entities
        if "Travis Private Bank" in entity_name or "David" in entity_name:
            continue
            
        data = fetch_gleif_data(entity_name)
        if data and data.get('data'):
            attributes = data['data'][0]['attributes']
            lei = attributes.get('lei')
            status = attributes['entity']['status']
            print(f"{entity_name:<30} | {status:<15} | {lei:<20}")
            sync_results.append({
                "entity": entity_name,
                "lei": lei,
                "global_status": status,
                "last_sync": "2026-04-20"
            })
        else:
            print(f"{entity_name:<30} | NOT FOUND       | N/A")

    with open('gleif_audit_results.json', 'w') as f:
        json.dump(sync_results, f, indent=4)

if __name__ == "__main__":
    sync()
