"""
Helper Utilities
Common helper functions used across the application
"""
import logging
from datetime import datetime
from typing import Any, Dict

logger = logging.getLogger(__name__)

def format_datetime(dt: datetime, format_str: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    Format datetime object to string
    
    Args:
        dt: Datetime object
        format_str: Format string
        
    Returns:
        Formatted datetime string
    """
    return dt.strftime(format_str)

def safe_get(dictionary: Dict, *keys, default=None) -> Any:
    """
    Safely get nested dictionary values
    
    Args:
        dictionary: Source dictionary
        *keys: Sequence of keys to traverse
        default: Default value if key not found
        
    Returns:
        Value at the key path or default
    
    Example:
        safe_get({'a': {'b': {'c': 1}}}, 'a', 'b', 'c')  # Returns 1
        safe_get({'a': {}}, 'a', 'b', 'c', default=0)     # Returns 0
    """
    result = dictionary
    for key in keys:
        if isinstance(result, dict):
            result = result.get(key)
            if result is None:
                return default
        else:
            return default
    return result

def truncate_text(text: str, max_length: int = 100, suffix: str = '...') -> str:
    """
    Truncate text to maximum length
    
    Args:
        text: Input text
        max_length: Maximum length
        suffix: Suffix to add when truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def validate_json_keys(data: Dict, required_keys: list) -> tuple[bool, str]:
    """
    Validate that required keys exist in JSON data
    
    Args:
        data: Dictionary to validate
        required_keys: List of required keys
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not data:
        return False, 'Empty data provided'
    
    missing_keys = [key for key in required_keys if key not in data]
    if missing_keys:
        return False, f'Missing required keys: {", ".join(missing_keys)}'
    
    return True, ''
