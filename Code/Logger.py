import os
import csv
import datetime
from collections import defaultdict

# Configuration
LOG_FOLDER = "/storage/emulated/0/Documents/call_logs/"
OUTPUT_FOLDER = "/storage/emulated/0/Documents/consolidated_logs/"
TODAY = datetime.datetime.now().strftime("%Y-%m-%d")

def process_logs():
    try:
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        unique_numbers = set()
        output_path = f"{OUTPUT_FOLDER}consolidated_{TODAY}.csv"
        
        with open(output_path, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(["Water Bottles", "Number", "Time", "Name"])
            
            for filename in os.listdir(LOG_FOLDER):
                if filename.endswith(".txt"):
                    with open(f"{LOG_FOLDER}{filename}", 'r') as infile:
                        for line in infile:
                            line = line.strip()
                            if not line:
                                continue
                            
                            parts = line.split()
                            if len(parts) < 3 or parts[1] == '?':
                                continue
                            
                            number = parts[1]
                            if number not in unique_numbers:
                                unique_numbers.add(number)
                                writer.writerow([
                                    int(parts[0]) if parts[0].isdigit() else 0,
                                    number,
                                    parts[2],
                                    ' '.join(parts[3:]) if len(parts) > 3 else '?'
                                ])
        
        # Clean up processed files
        for filename in os.listdir(LOG_FOLDER):
            if filename.endswith(".txt"):
                os.remove(f"{LOG_FOLDER}{filename}")
        
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    if process_logs():
        print("Logs processed successfully")
    else:
        print("Processing failed")
