import re
import pandas as pd
import csv
import sys

log_file_path='D:\Programs\Python\VRV\sample.log'

with open(log_file_path, 'r') as file:
    log_lines = file.readlines()

#ip addresses
ip_addresses = []
ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'

for line in log_lines:
    found_ips = re.findall(ip_pattern, line)
    ip_addresses.extend(found_ips)

ip_df = pd.DataFrame(ip_addresses, columns=['IP Address'])
request_counts = ip_df['IP Address'].value_counts().reset_index()
request_counts.columns = ['IP Address', 'Request Count']
request_counts = request_counts.sort_values(by='Request Count',ascending=False)
print(request_counts,'\n')

#Endpoints
endpoints = []
endpoint_pattern = r'(GET |POST |PUT |DELETE )(/[^ ]*)'

for line in log_lines:
    found_endpoints = re.findall(endpoint_pattern, line)
    endpoints.extend([path[1] for path in found_endpoints])

endpoint_df = pd.DataFrame(endpoints, columns=['Endpoints'])
endpoint_counts = endpoint_df['Endpoints'].value_counts().reset_index()
endpoint_counts.columns = ['Endpoint', 'Access Count']
endpoint_counts = endpoint_counts.sort_values(by='Access Count', ascending=False)
most_accessed_endpoint = endpoint_counts.iloc[0]
print(f"Most Frequently used Endpoint:\n {most_accessed_endpoint['Endpoint']}, Access Count: {most_accessed_endpoint['Access Count']}\n")

#Invalid credentials
invalids = []
invalid_pattern = r'(?i)(\b(?:\d{1,3}\.){3}\d{1,3}\b).*?(Invalid credentials.*)'

for line in log_lines:
    found_invalids = re.findall(invalid_pattern, line)
    invalids.extend([ ip[0]for ip in found_invalids])
invalid_df = pd.DataFrame(invalids, columns=['IP Address'])
invalid_counts = invalid_df['IP Address'].value_counts().reset_index()
invalid_counts.columns = ['IP Address', 'Failed Login Attempts']
invalid_counts = invalid_counts.sort_values(by='Failed Login Attempts',ascending=False)
print(invalid_counts,'\n')

#CSV File
with open('log_analysis_results.csv','w',newline='') as csvfile:
    writer = csv.writer(csvfile)
    stdout=sys.stdout
    sys.stdout=csvfile
    print(request_counts,'\n')
    print(f"Most Frequently used Endpoint:\n {most_accessed_endpoint['Endpoint']}, Access Count: {most_accessed_endpoint['Access Count']}\n")
    print(invalid_counts,'\n')
    sys.stdout=stdout
    