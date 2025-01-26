#!/usr/bin/env python3
import os
import sys
import requests
from typing import Optional

ETHERSCAN_API_URL = "https://api.etherscan.io/api"
API_KEY_ENV = "ETHERSCAN_API_KEY"

def get_contract_source(address: str, api_key: str) -> Optional[dict]:
    """Fetch contract source code from Etherscan API"""
    params = {
        "module": "contract",
        "action": "getsourcecode",
        "address": address,
        "apikey": api_key
    }
    
    try:
        response = requests.get(ETHERSCAN_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data["status"] != "1":
            print(f"Error: {data.get('message', 'Unknown error')}")
            return None
            
        return data["result"][0]
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <contract_address>")
        sys.exit(1)
        
    contract_address = sys.argv[1]
    api_key = os.getenv(API_KEY_ENV)
    
    if not api_key:
        print(f"Error: Please set {API_KEY_ENV} environment variable")
        sys.exit(1)
        
    contract_data = get_contract_source(contract_address, api_key)
    
    if not contract_data:
        print("Failed to fetch contract data")
        sys.exit(1)
        
    if contract_data["SourceCode"]:
        print("Contract Source Code:")
        print(contract_data["SourceCode"])
    else:
        print("No source code available for this contract")

if __name__ == "__main__":
    main()
