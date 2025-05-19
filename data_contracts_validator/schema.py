from typing import Dict, Any, Optional
import yaml
import json
import pandera as pa
from pandera.typing import Series
from pathlib import Path

class SchemaParser:
    """Parser for YAML/JSON schema contracts into Pandera schemas."""
    
    @staticmethod
    def load_contract(contract_path: str) -> Dict[str, Any]:
        """Load a contract file (YAML or JSON) into a dictionary."""
        path = Path(contract_path)
        with open(path, 'r') as f:
            if path.suffix.lower() in ['.yaml', '.yml']:
                return yaml.safe_load(f)
            elif path.suffix.lower() == '.json':
                return json.load(f)
            else:
                raise ValueError(f"Unsupported contract file format: {path.suffix}")

    @staticmethod
    def _convert_type(type_str: str) -> pa.DataType:
        """Convert string type to Pandera data type."""
        type_map = {
            'string': pa.String,
            'integer': pa.Int,
            'float': pa.Float,
            'boolean': pa.Bool,
            'datetime': pa.DateTime,
            'date': pa.Date,
        }
        if type_str not in type_map:
            raise ValueError(f"Unsupported type: {type_str}")
        return type_map[type_str]

    @staticmethod
    def _create_field_schema(field_config: Dict[str, Any]) -> pa.Column:
        """Create a Pandera column schema from field configuration."""
        dtype = SchemaParser._convert_type(field_config['type'])
        
        # Build validation rules
        checks = []
        
        if field_config.get('required', False):
            checks.append(pa.Check.not_null())
            
        if 'min' in field_config:
            checks.append(pa.Check.greater_than_or_equal_to(field_config['min']))
            
        if 'max' in field_config:
            checks.append(pa.Check.less_than_or_equal_to(field_config['max']))
            
        if 'pattern' in field_config:
            checks.append(pa.Check.str_matches(field_config['pattern']))
            
        if 'enum' in field_config:
            checks.append(pa.Check.isin(field_config['enum']))
            
        return pa.Column(dtype, checks=checks)

    @classmethod
    def create_schema(cls, contract_path: str) -> pa.DataFrameSchema:
        """Create a Pandera schema from a contract file."""
        contract = cls.load_contract(contract_path)
        schema_config = contract.get('schema', {})
        
        if not schema_config:
            raise ValueError("No schema configuration found in contract")
            
        fields = schema_config.get('fields', {})
        if not fields:
            raise ValueError("No fields defined in schema")
            
        columns = {
            field_name: cls._create_field_schema(field_config)
            for field_name, field_config in fields.items()
        }
        
        return pa.DataFrameSchema(
            columns=columns,
            strict=True,
            coerce=True
        ) 