import os
import re
import csv
import json

class JudicialPrintAuditor:
    def __init__(self, log_dir, output_dir):
        self.log_dir = log_dir
        self.output_dir = output_dir
        self.log_pattern = re.compile(
            r'(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)\s+'
            r'(?P<host>[\w\.-]+)\s+'
            r'RICOH_[\w_-]+:?\s+JobId=(?P<job_id>\d+)\s+'
            r'User=(?P<user>[\w\.-]+)\s+'
            r'Status=(?P<status>\w+)\s+'
            r'Docs=(?P<doc_count>\d+)\s+'
            r'CaseRef=(?P<case_ref>[\w-]+)?'
        )
        
    def parse_syslogs(self):
        audit_results = []
        anomaly_count = 0

        if not os.path.exists(self.log_dir):
            print(f"[-] Target log directory missing: {self.log_dir}")
            return {"error": f"Directory not found"}

        for file_name in os.listdir(self.log_dir):
            file_path = os.path.join(self.log_dir, file_name)
            if not os.path.isfile(file_path):
                continue
                
            with open(file_path, 'r', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    if "@remote" in line.lower() or "admin_console" in line.lower():
                        anomaly_count += 1
                        audit_results.append({
                            "type": "CRITICAL_ADMIN_ACCESS",
                            "file": file_name,
                            "line": line_num,
                            "raw": line.strip()
                        })
                        continue

                    match = self.log_pattern.search(line)
                    if match:
                        data = match.groupdict()
                        if data['status'] == 'SPOOL_SHARED' and not data['case_ref']:
                            anomaly_count += 1
                            data['type'] = 'UNTRACKED_SHARED_SPOOL'
                            audit_results.append(data)

        self._export_results(audit_results)
        print(f"[+] Forensic parse complete. Identified anomalies: {anomaly_count}")
        return {"status": "Complete", "processed_anomalies": anomaly_count}

    def _export_results(self, data):
        os.makedirs(self.output_dir, exist_ok=True)
        with open(os.path.join(self.output_dir, "audit_report.json"), 'w') as jf:
            json.dump(data, jf, indent=4)

if __name__ == "__main__":
    auditor = JudicialPrintAuditor(log_dir="./logs/cts_central", output_dir="./audit_output")
    auditor.parse_syslogs()
