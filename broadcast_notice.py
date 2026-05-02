import os
from signalwire.rest import Client as signalwire_client

# Pulling credentials from environment
PROJECT_ID = os.environ.get('SIGNALWIRE_PROJECT')
AUTH_TOKEN = os.environ.get('SIGNALWIRE_TOKEN')
SPACE_URL = os.environ.get('SIGNALWIRE_SPACE')

def send_notice():
    if not all([PROJECT_ID, AUTH_TOKEN, SPACE_URL]):
        print("Error: Missing SignalWire environment variables.")
        return

    client = signalwire_client(PROJECT_ID, AUTH_TOKEN, signalwire_space_url=SPACE_URL)

    with open('notice_of_default.txt', 'r') as f:
        content = f.read()

    # Final logic check before broadcast
    print("Initiating broadcast of Notice of Default...")
    
    try:
        message = client.messages.create(
            from_='+1XXXXXXXXXX',  # Your SignalWire Number
            body=content,
            to='+15626533200'      # Atkinson firm Cerritos office primary
        )
        print(f"Notice broadcasted successfully. SID: {message.sid}")
    except Exception as e:
        print(f"Broadcast failed: {e}")

if __name__ == "__main__":
    send_notice()
