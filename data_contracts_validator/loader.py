import pandas as pd
from pathlib import Path
from typing import Union, Optional

class DataLoader:
    """Loader for different data file formats (CSV, JSON, Parquet)."""
    
    @staticmethod
    def load_data(file_path: str) -> pd.DataFrame:
        """Load data from various file formats into a pandas DataFrame."""
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Data file not found: {file_path}")
            
        suffix = path.suffix.lower()
        
        try:
            if suffix == '.csv':
                return pd.read_csv(file_path)
            elif suffix == '.json':
                return pd.read_json(file_path)
            elif suffix == '.parquet':
                return pd.read_parquet(file_path)
            else:
                raise ValueError(f"Unsupported file format: {suffix}")
        except Exception as e:
            raise ValueError(f"Error loading data file {file_path}: {str(e)}")
            
    @staticmethod
    def validate_dataframe(df: pd.DataFrame, schema: pd.DataFrameSchema) -> tuple[bool, Optional[dict]]:
        """Validate a DataFrame against a Pandera schema."""
        try:
            schema.validate(df)
            return True, None
        except pa.errors.SchemaError as e:
            return False, {
                'error_type': 'SchemaError',
                'message': str(e),
                'details': e.failure_cases.to_dict() if hasattr(e, 'failure_cases') else None
            }
        except Exception as e:
            return False, {
                'error_type': type(e).__name__,
                'message': str(e)
            } 