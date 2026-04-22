import pikepdf
import sys

def extract_meta(file_path):
    try:
        with pikepdf.open(file_path) as pdf:
            meta = pdf.open_metadata()
            print(f"\n[+] Metadata for: {file_path}")
            for key, value in meta.items():
                print(f"    {key}: {value}")
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        extract_meta(sys.argv[1])
    else:
        print("Usage: python harvester.py <filename.pdf>")
