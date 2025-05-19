import click
from pathlib import Path
from typing import Optional
from .schema import SchemaParser
from .loader import DataLoader
from .formatters import (
    ValidationResult,
    JSONFormatter,
    MarkdownFormatter,
    ConsoleFormatter
)

def get_formatter(output_format: str):
    """Get the appropriate formatter based on output format."""
    formatters = {
        'json': JSONFormatter(),
        'markdown': MarkdownFormatter(),
        'console': ConsoleFormatter()
    }
    if output_format not in formatters:
        raise ValueError(f"Unsupported output format: {output_format}")
    return formatters[output_format]

@click.command()
@click.option(
    '--data-file',
    required=True,
    type=click.Path(exists=True),
    help='Path to data file (CSV/JSON/Parquet)'
)
@click.option(
    '--contract',
    required=True,
    type=click.Path(exists=True),
    help='Path to contract file (YAML/JSON)'
)
@click.option(
    '--output-format',
    default='console',
    type=click.Choice(['json', 'markdown', 'console']),
    help='Output format (json|markdown|console)'
)
@click.option(
    '--strict',
    is_flag=True,
    help='Treat warnings as errors'
)
@click.option(
    '--batch',
    is_flag=True,
    help='Enable batch validation mode'
)
def main(
    data_file: str,
    contract: str,
    output_format: str,
    strict: bool,
    batch: bool
):
    """Validate data files against schema contracts."""
    try:
        # Load and parse the schema
        schema = SchemaParser.create_schema(contract)
        
        # Load the data
        df = DataLoader.load_data(data_file)
        
        # Validate the data
        is_valid, error_details = DataLoader.validate_dataframe(df, schema)
        
        # Create validation result
        result = ValidationResult(
            data_file=data_file,
            contract_file=contract,
            is_valid=is_valid,
            total_rows=len(df),
            error_details=error_details
        )
        
        # Format and output the result
        formatter = get_formatter(output_format)
        output = formatter.format(result)
        
        # Print the output
        click.echo(output)
        
        # Exit with appropriate status code
        exit_code = 0 if is_valid else 1
        if strict and error_details:
            exit_code = 1
        raise SystemExit(exit_code)
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise SystemExit(1)

if __name__ == '__main__':
    main() 