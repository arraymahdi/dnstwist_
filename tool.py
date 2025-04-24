import subprocess
import json
import os

def run_dnstwist(domain):
    try:
        # Path to dnstwist.py
        dnstwist_path = os.path.join(os.getcwd(), "dnstwist.py")

        # Command to run dnstwist with JSON output
        result = subprocess.run(
            ['python', dnstwist_path, '--tld', 'dictionaries/common_tlds.dict', '--registered', '--format', 'json', domain],
            capture_output=True,
            text=True,
            cwd=os.getcwd()  # ensures dnstwist runs in the same folder
        )

        if result.returncode != 0:
            print("Error from dnstwist:\n", result.stderr)
            return []

        # Parse JSON output
        domains = json.loads(result.stdout)
        print(domains)
        return domains

    except Exception as e:
        print("Unexpected error:", e)
        return []

def analyze_domain(domain):
    domains = run_dnstwist(domain)

    # Filter & display useful fields
    results = []
    for entry in domains:
        info = {
            "domain": entry.get("domain"),
            "dns_a": entry.get("dns_a"),
            "dns_ns": entry.get("dns_ns"),
            "dns_mx": entry.get("dns_mx"),
            "fuzzer": entry.get("fuzzer"),
        }
        results.append(info)
    return results

# Example usage
if __name__ == "__main__":
    domain = "arrayworld.online"
    data = analyze_domain(domain)

    print(json.dumps(data, indent=2))
