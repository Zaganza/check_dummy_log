import random
import datetime

# List of example hostnames
hostnames = ["example.com", "dummyhost.net", "test.org", "localhost", "demo.biz"]

# Reported IPs:
specified_ips = [
    '177.12.2.75',
    '170.106.107.252',
    '193.189.100.195',
    '192.42.116.216',
    '192.42.116.184',
    '170.64.222.171',
    '43.153.44.198',
    '41.38.197.45',
    '1.238.106.229',
    '198.235.24.227'
]


# generate a random IP
def generate_random_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))


# generate a dummy log entry
def generate_log_entry():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Randomly choose between specified IPs and random IPs
    if random.random() < 0.5 or len(specified_ips) == 0:
        ip = generate_random_ip()
    else:
        ip = specified_ips.pop(random.randint(0, len(specified_ips) - 1))

    hostname = random.choice(hostnames)
    return f"{timestamp} - {ip} - {hostname}"


# Num of log entries
num_entries = 30

# Create a filename for the text file
filename = "dummy_logs.txt"

# Open the file in write mode and generate log entries
with open(filename, 'w') as file:
    for _ in range(num_entries):
        log_entry = generate_log_entry()
        file.write(log_entry + "\n")

print(f"Generated {num_entries} log entries in {filename}.")