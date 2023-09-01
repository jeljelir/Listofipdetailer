import requests
import csv
import os
from datetime import datetime
import random
from time import sleep


# List of IPs
ip_list = """
1.1.1.1
"""

# Virus Total API keys
vt_apis = [
    ''
]

sleep_time = 5


def virus_total(ip):
    clean = []
    infected = []

    headers = {"accept": "application/json", 'x-apikey': random.choice(vt_apis)}
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"

    try:
        # Set a timeout value in seconds
        response = requests.get(url, headers=headers, timeout=10)
        # Raise an exception for HTTP errors
        response.raise_for_status()
        response = response.json()

        if response:
            results = response['data']['attributes']['last_analysis_results']
            print(results)
            for result in results.values():
                print(result)
                if result['result'] in ('clean', 'unrated'):
                    clean.append(result['engine_name'])
                else:
                    infected.append(result['engine_name'])

    except requests.exceptions.RequestException as e:
        print(f"      ERROR: {e}")

    return [clean, infected]


def get_ip_details(ip):
    url = f"http://ip-api.com/json/{ip}"
    try:
        # Set a timeout value in seconds
        response = requests.get(url, timeout=10)
        status_code = response.status_code
        # Raise an exception for HTTP errors
        response.raise_for_status()
        response = response.json()
    except requests.exceptions.RequestException as e:
        print(f"      ERROR: {e}")
        response = ""
        status_code = 0

    clean, infected = virus_total(ip)

    ip_whois = {
        'status': status_code,
        'ip': ip,
        'continent': response['continent'] if 'continent' in response else None,
        'continent_code': response['continentCode'] if 'continentCode' in response else None,
        'country': response['country'] if 'country' in response else None,
        'country_code': response['countryCode'] if 'countryCode' in response else None,
        'region': response['regionName'] if 'regionName' in response else None,
        'district': response['district'] if 'district' in response else None,
        'city': response['city'] if 'city' in response else None,
        'zip_code': response['zip'] if 'zip' in response else None,
        'latitude': response['lat'] if 'lat' in response else None,
        'longitude': response['lon'] if 'lon' in response else None,
        'timezone': response['timezone'] if 'timezone' in response else None,
        'time_offset': response['offset'] if 'offset' in response else None,
        'isp': response['isp'] if 'isp' in response else None,
        'organization': response['org'] if 'org' in response else None,
        'as_number': response['as'] if 'as' in response else None,
        'as_name': response['asname'] if 'asname' in response else None,
        'reverse_dns': response['reverse'] if 'reverse' in response else None,
        'is_mobile': response['mobile'] if 'mobile' in response else None,
        'is_hosting': response['hosting'] if 'hosting' in response else None,
        'is_proxy': response['proxy'] if 'proxy' in response else None,
        'infected_rate': len(infected),
        'clean_rate': len(clean),
        'infected_list': infected,
        'clean_list': clean,
    }

    return ip_whois


def main():
    ips = [line.strip() for line in ip_list.strip().split('\n') if line.strip()]
    unique_ips = list(dict.fromkeys(ips))

    data = []
    counter = 0

    for ip_address in unique_ips:
        counter += 1
        ip_details = get_ip_details(ip_address)

        if ip_details.get('status'):
            print(f"  [+] {ip_details['ip']}   (# {counter}/{len(unique_ips)})")
            print(f"      {ip_details['country_code']} - {ip_details['city']} - {ip_details['isp']}")
            print(f"      {ip_details['reverse_dns']}")
            print(f"      M: {ip_details['is_mobile']} - P: {ip_details['is_proxy']} - H: {ip_details['is_hosting']}")

            data.append(ip_details)

            sleep(sleep_time)

    # write into the CSV file
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file_path = os.path.join(os.path.expanduser("~"), "Desktop", f"ip_details_{now}.csv")

    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
        csv_writer.writeheader()
        csv_writer.writerows(data)


if __name__ == "__main__":
    main()
