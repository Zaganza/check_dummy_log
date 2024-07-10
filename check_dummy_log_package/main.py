import os
import requests
import re


# Function to fetch log entries from file
def fetch_log_entries(file_path):
    with open(file_path, "r") as file:
        log_entries = file.readlines()
    return log_entries


# Function to extract IPs from log entries
def extract_ips(log_entries):
    ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    ips = []
    for entry in log_entries:
        match = re.search(ip_pattern, entry)
        if match:
            ips.append(match.group())
    return ips


# Function to query AbuseIPDB
def query_abuseipdb(api_key, ip):
    url = f"https://api.abuseipdb.com/api/v2/check"
    params = {
        'ipAddress': ip,
        'maxAgeInDays': 90,
        'verbose': True
    }
    headers = {
        'Key': api_key,
        'Accept': 'application/json'
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching AbuseIPDB data for {ip}: Status Code {response.status_code}")
    except Exception as e:
        print(f"Error fetching AbuseIPDB data for {ip}: {str(e)}")
    return None


# Function to write output to a text file and print to console
def write_output(file_path, results):
    with open(file_path, "w") as file:
        for result in results:
            print(result)  # Print to console
            file.write(result + "\n")  # Write to file


# Main function to fetch logs, process IPs, query AbuseIPDB, and write output
def main():
    # Get AbuseIPDB API key from user
    api_key = input("Enter your AbuseIPDB API key: ").strip()

    # Determine file paths based on current directory
    script_dir = os.path.dirname(os.path.realpath(__file__))
    log_file = os.path.join(script_dir, "dummy_logs.txt")
    output_file = os.path.join(script_dir, "abuseipdb_report.txt")

    # Fetch log entries
    log_entries = fetch_log_entries(log_file)
    ips = extract_ips(log_entries)

    output = []

    for ip in ips:
        print(f"Querying AbuseIPDB for IP: {ip}")
        result = query_abuseipdb(api_key, ip)
        if result:
            output.append(f"IP: {ip}")
            output.append(f"Abuse Confidence Score: {result['data']['abuseConfidenceScore']}")
            output.append(f"Country: {result['data']['countryCode']}")
            output.append(f"Usage Type: {result['data']['usageType']}")
            output.append(f"ISP: {result['data']['isp']}")
            output.append(f"Total Reports: {result['data']['totalReports']}")
            output.append(f"Last Reported At: {result['data']['lastReportedAt']}")
            output.append("-----------------------------")
        else:
            output.append(f"No AbuseIPDB data found for IP: {ip}")
        output.append("")  # Empty line for separation

    # Write output to file and print to console
    write_output(output_file, output)
    print(f"Output saved to {output_file}")


if __name__ == "__main__":
    main()