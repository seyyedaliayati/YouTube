#!/usr/bin/env python3
import os
import sys
import requests
from typing import Optional
from dotenv import load_dotenv
from pathlib import Path

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
    load_dotenv()
    api_key = os.getenv(API_KEY_ENV)
    
    if not api_key:
        print(f"Error: Please create a .env file with {API_KEY_ENV} variable")
        sys.exit(1)
        
    contract_data = get_contract_source(contract_address, api_key)
    
    if not contract_data:
        print("Failed to fetch contract data")
        sys.exit(1)
        
    if not contract_data["SourceCode"]:
        print("No source code available for this contract")
        sys.exit(1)
        
    # Create contracts directory if it doesn't exist
    contracts_dir = Path("contracts")
    contracts_dir.mkdir(exist_ok=True)
    
    # Save source code to file
    output_file = contracts_dir / f"{contract_address}.sol"
    try:
        with open(output_file, "w") as f:
            f.write(contract_data["SourceCode"])
        print(f"Contract source code saved to {output_file}")
    except IOError as e:
        print(f"Error saving contract source: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
