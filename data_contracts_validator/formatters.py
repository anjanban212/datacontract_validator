from typing import Dict, Any, Optional
import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from datetime import datetime

class ValidationResult:
    """Container for validation results."""
    
    def __init__(
        self,
        data_file: str,
        contract_file: str,
        is_valid: bool,
        total_rows: int,
        error_details: Optional[Dict[str, Any]] = None
    ):
        self.data_file = data_file
        self.contract_file = contract_file
        self.is_valid = is_valid
        self.total_rows = total_rows
        self.error_details = error_details
        self.timestamp = datetime.now().isoformat()

class BaseFormatter:
    """Base class for output formatters."""
    
    def format(self, result: ValidationResult) -> str:
        raise NotImplementedError

class JSONFormatter(BaseFormatter):
    """Format validation results as JSON."""
    
    def format(self, result: ValidationResult) -> str:
        output = {
            'data_file': result.data_file,
            'contract_file': result.contract_file,
            'timestamp': result.timestamp,
            'is_valid': result.is_valid,
            'total_rows': result.total_rows,
            'error_details': result.error_details
        }
        return json.dumps(output, indent=2)

class MarkdownFormatter(BaseFormatter):
    """Format validation results as Markdown."""
    
    def format(self, result: ValidationResult) -> str:
        status_emoji = "✅" if result.is_valid else "❌"
        
        output = [
            "# Validation Report\n",
            "## Summary",
            f"- File: {result.data_file}",
            f"- Contract: {result.contract_file}",
            f"- Status: {status_emoji} {'PASSED' if result.is_valid else 'FAILED'}",
            f"- Total Rows: {result.total_rows}",
            f"- Timestamp: {result.timestamp}\n"
        ]
        
        if result.error_details:
            output.extend([
                "## Error Details",
                f"### {result.error_details['error_type']}",
                f"```",
                f"{result.error_details['message']}",
                "```"
            ])
            
            if result.error_details.get('details'):
                output.extend([
                    "\n### Failure Cases",
                    "```json",
                    json.dumps(result.error_details['details'], indent=2),
                    "```"
                ])
        else:
            output.append("\n## Details\nNo validation errors found.")
            
        return "\n".join(output)

class ConsoleFormatter(BaseFormatter):
    """Format validation results for console output using Rich."""
    
    def format(self, result: ValidationResult) -> str:
        console = Console()
        
        # Create status panel
        status = "PASSED" if result.is_valid else "FAILED"
        color = "green" if result.is_valid else "red"
        status_panel = Panel(
            f"[bold {color}]{status}[/]",
            title="Validation Status",
            border_style=color
        )
        
        # Create summary table
        summary_table = Table(show_header=False, box=None)
        summary_table.add_row("Data File:", result.data_file)
        summary_table.add_row("Contract:", result.contract_file)
        summary_table.add_row("Total Rows:", str(result.total_rows))
        summary_table.add_row("Timestamp:", result.timestamp)
        
        # Create error details if present
        error_panel = None
        if result.error_details:
            error_content = [
                f"[bold red]{result.error_details['error_type']}[/]",
                result.error_details['message']
            ]
            if result.error_details.get('details'):
                error_content.append(
                    json.dumps(result.error_details['details'], indent=2)
                )
            error_panel = Panel(
                "\n".join(error_content),
                title="Error Details",
                border_style="red"
            )
        
        # Combine all elements
        output = []
        output.append(status_panel)
        output.append(summary_table)
        if error_panel:
            output.append(error_panel)
            
        return "\n".join(str(x) for x in output) 