# Open Source Vulnerabilities API


## Overview

A Python client for searching vulnerabilities from the [OSV.dev](https://osv.dev/) vulnerability database.

The OSV API uses `POST` method to fetch **JSON** data for known vulnerabilities of a package of a particular version in a specified ecosystem.
To call the API Data from database

```bash
curl -s -X POST \
    -H "Content-Type: application/json" \
    -d "$payload" \
    "https://api.osv.dev/v1/query" | jq --indent 4 .

```

 ### Python Method

 Python uses `requests` module to get API response. It parses **JSON** data to show much readable way with counting total vunerabilities.

 ```bash
git clone https://github.com/niloydatta000/osv-python-cli-demo.git
cd osv-python-cli-demo
python3 -m pip install -r requirements.txt
python3 main.py -p "$payload"
 ```

 Alternatively package name, version and ecosystem can be delivered:

 ```bash
 python3 main.py -n "$name" -v "$version" -s "$ecosystem"
 ```

### Docker Method

To build and run Docker Image:

```bash
docker build -t osv-python-cli  .
docker run --rm osv-python-cli -p "$payload"
```

## Conclusion

This project is aimed to procure, arrange and display vulneranbilities in a structuured way on the terminal.
