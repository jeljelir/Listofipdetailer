import requests
import csv
import os
import json

def get_ip_details(ip):
    url = f"http://ip-api.com/json/{ip}"
    try:
        response = requests.get(url, timeout=10)  # Set a timeout value in seconds
        response.raise_for_status()  # Raise an exception for HTTP errors

        details = response.json()
    except requests.exceptions.RequestException as e:
        details = {'status': 'error', 'message': f"Request error: {e}"}

    return details

def main():
    ip_list = """
## list of IP-addresses
    """

    ip_lines = [line.strip() for line in ip_list.strip().split('\n') if line.strip()]
    unique_ips = list(dict.fromkeys(ip_lines))

    csv_data = []
    text_data = []

    for ip_address in unique_ips:
        ip_details = get_ip_details(ip_address)

        if ip_details.get('status') != 'error':
            csv_data.append({
                "IP": ip_details.get("query"),
                "Location": ip_details.get("city"),
                "Company": ip_details.get("org"),
                "Latitude": ip_details.get("lat"),
                "Longitude": ip_details.get("lon"),
                "Region": ip_details.get("regionName"),
                "Error": "",
            })

            text_data.append(f"IP: {ip_details.get('query')}")
            text_data.append(f"Location: {ip_details.get('city')}")
            text_data.append(f"Company: {ip_details.get('org')}")
            text_data.append(f"Latitude: {ip_details.get('lat')}")
            text_data.append(f"Longitude: {ip_details.get('lon')}")
            text_data.append(f"Region: {ip_details.get('regionName')}")
            text_data.append("=" * 40)

        else:
            csv_data.append({
                "IP": ip_address,
                "Error": "Unable to fetch details",
            })
            text_data.append(f"IP: {ip_address}")
            text_data.append(f"Error: Unable to fetch details")
            text_data.append("=" * 40)

    csv_file_path = os.path.join(os.path.expanduser("~"), "Desktop", "ip_details.csv")
    text_file_path = os.path.join(os.path.expanduser("~"), "Desktop", "ip_details.txt")

    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=csv_data[0].keys())
        csv_writer.writeheader()
        csv_writer.writerows(csv_data)

    with open(text_file_path, mode='w', encoding='utf-8') as text_file:
        text_file.write('\n'.join(text_data))

if __name__ == "__main__":
    main()
