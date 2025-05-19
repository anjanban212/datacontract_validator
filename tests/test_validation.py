import os
import json
import pandas as pd
from pathlib import Path

# Create test data directory
TEST_DIR = Path(__file__).parent / "test_data"
TEST_DIR.mkdir(exist_ok=True)

# Example contract
CONTRACT = {
    "schema": {
        "name": "users",
        "fields": {
            "user_id": {
                "type": "integer",
                "required": True
            },
            "email": {
                "type": "string",
                "required": True,
                "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
            },
            "age": {
                "type": "integer",
                "min": 0,
                "max": 120
            },
            "status": {
                "type": "string",
                "enum": ["active", "inactive", "pending"]
            }
        }
    }
}

# Example valid data
VALID_DATA = pd.DataFrame({
    "user_id": [1, 2, 3],
    "email": ["user1@example.com", "user2@example.com", "user3@example.com"],
    "age": [25, 30, 35],
    "status": ["active", "inactive", "pending"]
})

# Example invalid data
INVALID_DATA = pd.DataFrame({
    "user_id": [1, 2, 3],
    "email": ["invalid-email", "user2@example.com", "user3@example.com"],
    "age": [25, 150, -5],  # Invalid ages
    "status": ["active", "invalid", "pending"]  # Invalid status
})

def setup_test_files():
    """Create test files for validation."""
    # Save contract
    contract_path = TEST_DIR / "contract.yaml"
    with open(contract_path, "w") as f:
        json.dump(CONTRACT, f, indent=2)
    
    # Save valid data
    valid_data_path = TEST_DIR / "valid_data.csv"
    VALID_DATA.to_csv(valid_data_path, index=False)
    
    # Save invalid data
    invalid_data_path = TEST_DIR / "invalid_data.csv"
    INVALID_DATA.to_csv(invalid_data_path, index=False)
    
    return {
        "contract": str(contract_path),
        "valid_data": str(valid_data_path),
        "invalid_data": str(invalid_data_path)
    }

if __name__ == "__main__":
    # Create test files
    test_files = setup_test_files()
    print("Test files created:")
    for name, path in test_files.items():
        print(f"- {name}: {path}")
    
    print("\nTo test the validator, run:")
    print(f"validate-contract --data-file {test_files['valid_data']} --contract {test_files['contract']} --output-format markdown")
    print(f"validate-contract --data-file {test_files['invalid_data']} --contract {test_files['contract']} --output-format markdown") 