import requests
import argparse
import json



class OSV_API:
    """A class to interact with the OSV API for fetching vulnerabilities related to specific package versions."""

    def __init__(self, base_url="https://api.osv.dev/v1/query"):
        """Initializes the OSV_API class with a base URL for the OSV API."""

        self.base_url = base_url

    def get_vulnerabilities_by_package_version(self, package_name:str, package_version:str, ecosystem:str) -> dict | None:
        """
        Fetches vulnerabilities for a specific package version from the OSV API.
        Args:
            package_name (str): The name of the package.
            package_version (str): The version of the package.
            ecosystem (str): The ecosystem of the package (e.g., "PyPI", "npm").
        Returns:
            dict: A dictionary containing the vulnerabilities data, or None if an error occurred.
        """

        # Construct the payload for the API request
        payload = {
            "package": {
                "name": package_name,
                "ecosystem": ecosystem
            },
            "version": package_version
        }

        try:
            response = requests.post(self.base_url, json=payload)
            response.raise_for_status() # Raise an exception for HTTP errors
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching vulnerabilities: {e}")
            return None

    def get_vulnerabilities_by_payload(self, payload:dict) -> dict | None:
        """
        Fetches vulnerabilities based on a custom payload from the OSV API.
        Args:
            payload (dict): A dictionary containing the request payload.
        Returns:
            dict: A dictionary containing the vulnerabilities data, or None if an error occurred.
        """

        try:
            response = requests.post(self.base_url, json=payload)
            response.raise_for_status() # Raise an exception for HTTP errors
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching vulnerabilities: {e}")
            return None



def main():
    """Main function to parse command-line arguments and fetch vulnerabilities using the OSV API."""

    parser = argparse.ArgumentParser(description="Fetch vulnerabilities for a specific package version from the OSV API.",
                                     usage="python main.py -n <package_name> -v <package_version> -s <ecosystem> | python main.py -p <payload> -u <base_url>",
                                     epilog="Example: python main.py -n jinja2 -v 2.4.1 -s PyPI | python main.py -p '{\"package\": {\"name\": \"jinja2\", \"ecosystem\": \"PyPI\"}, \"version\": \"2.4.1\"}' -u https://api.osv.dev/v1/query")
    parser.add_argument("-V", "--version", action="version", version="OSV API Client 1.0")
    parser.add_argument("-n", "--name", help="The name of the package.")
    parser.add_argument("-v", "--package-version", help="The version of the package.")
    parser.add_argument("-s", "--ecosystem", help="The ecosystem of the package (e.g., 'PyPI', 'npm').")
    parser.add_argument("-p", "--payload", help="A JSON string representing the request payload.")
    parser.add_argument("-u", "--base-url", default="https://api.osv.dev/v1/query", help="The base URL of the OSV API (default: https://api.osv.dev/v1/query).")

    args = parser.parse_args()

    osv_api = OSV_API(base_url=args.base_url)

    if args.payload:
        # If a payload is provided, use it to fetch vulnerabilities
        try:
            payload_dict = json.loads(args.payload)
        except json.JSONDecodeError as e:
            print(f"Error parsing payload JSON: {e}")
            return
        vulnerabilities = osv_api.get_vulnerabilities_by_payload(payload_dict)
    else:
        # If no payload is provided, use the traditional method
        if not (args.name and args.package_version and args.ecosystem):
            parser.error("Cannot find specified packages. Please provide name, version and ecosystem")
        vulnerabilities = osv_api.get_vulnerabilities_by_package_version(args.name, args.package_version, args.ecosystem)

    if "vulns" not in vulnerabilities or not vulnerabilities["vulns"]:
        print("No known vulnerabilities found for the specified package version on the particular ecosystem.")
    else:
        print(f"Warning: {len(vulnerabilities['vulns'])} known vulnerabilities found for the specified package version:\n")
        for vuln in vulnerabilities["vulns"]:
            severity_rating = "N/A"
            v_id = vuln.get("id", "N/A")
            v_summary = vuln.get("summary", "No summary available.")
            v_details = vuln.get("details", "No details available.")
            v_aliases = vuln.get("aliases", [])
            v_references = vuln.get("references", [])

            # Check for severity in the vulnerability data
            if "severity" in vuln and isinstance(vuln["severity"], list):
                for sev_entry in vuln["severity"]:
                    if isinstance(sev_entry, dict) and "score" in sev_entry:
                        severity_rating = str(sev_entry["score"]).upper()
                        break
            elif severity_rating == "N/A" and "database_specific" in vuln:
                db_specific = vuln["database_specific"]
                if "severity" in db_specific and isinstance(db_specific["severity"], dict):
                    severity_rating = str(db_specific["severity"]).upper()

            print(f"Vulnerability ID: {v_id}")
            print(f"Aliases: {', '.join(v_aliases) if v_aliases else 'None'}")
            print(f"Severity Rating: {severity_rating}")
            print(f"Summary: {v_summary}")
            print(f"Details: {v_details}")
            if v_references:
                print("References:")
                for ref in v_references:
                    ref_type = ref["type"] if "type" in ref else "N/A"
                    ref_url = ref["url"] if "url" in ref else "N/A"
                    print(f"  - Type: {ref_type}, URL: {ref_url}")
            print("\n" + "-"*140 + "\n")


if __name__ == "__main__":
    main()
