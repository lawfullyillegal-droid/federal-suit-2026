import json
import os

# Updated to look inside the directory for any JSON file
source_dir = os.path.expanduser('~/lm_source')
output_dir = os.path.join(source_dir, 'parsed')

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Automatically finds the first JSON file in the folder
json_files = [f for f in os.listdir(source_dir) if f.endswith('.json')]

if not json_files:
    print("No JSON file found in ~/lm_source. Check Step 2!")
else:
    source_file = os.path.join(source_dir, json_files[0])
    with open(source_file, 'r') as f:
        data = json.load(f)
        # Handles Google Takeout or standard list formats
        chats = data if isinstance(data, list) else data.get('conversations', [data])
        for i, chat in enumerate(chats):
            with open(f"{output_dir}/chat_{i}.md", "w") as out:
                out.write(f"# Chat {i}\n\n{json.dumps(chat, indent=2)}")
    print(f"Success! {len(chats)} chats processed into {output_dir}")
