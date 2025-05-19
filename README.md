# Data Contracts Validator

A Python CLI tool for validating data against YAML-defined schema contracts. This tool helps data engineers and analytics engineers enforce data contracts in modern data platforms.

## Features

- Validate data files (CSV, JSON, Parquet) against YAML/JSON schema contracts
- Support for complex validation rules (types, required fields, enums, constraints)
- Multiple output formats (JSON, Markdown, console)
- Batch validation support
- Integration capabilities with dbt, Airflow, and CI/CD pipelines

## Installation

```bash
pip install data-contracts-validator
```

## Quick Start

1. Create a data contract in YAML format:

```yaml
# contract.yaml
schema:
  name: users
  fields:
    user_id:
      type: integer
      required: true
    email:
      type: string
      required: true
      pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
    age:
      type: integer
      min: 0
      max: 120
    status:
      type: string
      enum: ["active", "inactive", "pending"]
```

2. Validate your data:

```bash
validate-contract --data-file data.csv --contract contract.yaml --output-format markdown
```

## Usage

```bash
validate-contract [OPTIONS]

Options:
  --data-file PATH     Path to data file (CSV/JSON/Parquet)
  --contract PATH      Path to contract file (YAML/JSON)
  --output-format TEXT Output format (json|markdown|console)
  --strict            Treat warnings as errors
  --batch             Enable batch validation mode
  --help              Show this message and exit
```

## Output Examples

### Console Output
```
✅ Validation passed for data.csv
└── All 1000 rows passed validation
```

### Markdown Output
```markdown
# Validation Report

## Summary
- File: data.csv
- Contract: contract.yaml
- Status: ✅ PASSED
- Total Rows: 1000
- Valid Rows: 1000
- Invalid Rows: 0

## Details
No validation errors found.
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details. 