import os

theorems = {
    "03": "Ministerial Duty Breach",
    "04": "Nexus of Harm",
    "05": "Jurisdictional Shield"
}

print("# STATEMENT OF FACTS: THE 12-YEAR GAP (2008-2020)\n")
print("1. In 2007, the Petitioner was involved in the 'Ventura 2007 Case'.")
print("2. Judicial records confirm the final disposition was a Misdemeanor.")
print("3. From 2008 to 2020, Defendants maintained the record as a 'Felony' despite judicial determination.")

for tid, name in theorems.items():
    summary_path = f"03_Logic_Proofs/theorem_{tid}_summary.txt"
    if os.path.exists(summary_path):
        print(f"\n### Logical Verification of {name}:")
        with open(summary_path, 'r') as f:
            lines = f.readlines()
            # Skip the header/footer lines and just grab the core logic
            logic_lines = [l.strip() for l in lines if l.strip() and "=" not in l]
            for line in logic_lines:
                print(f"> {line}")

print("\n4. Conclusion: The sustained misclassification resulted in a 12-year period of 'Civil Death' and Identity Conversion.")
