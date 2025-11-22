"""
Utility functions and helpers.
"""
import logging
from pathlib import Path
from typing import Optional


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    format_string: Optional[str] = None
) -> None:
    """
    Set up logging configuration.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file to write logs to
        format_string: Optional custom format string
    """
    if format_string is None:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Convert string level to logging constant
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    
    # Configure logging
    handlers = [logging.StreamHandler()]
    
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=numeric_level,
        format=format_string,
        handlers=handlers
    )


def validate_url(url: str) -> bool:
    """
    Validate if a string is a valid URL.
    
    Args:
        url: URL string to validate
        
    Returns:
        True if valid, False otherwise
    """
    import re
    
    # Simple URL validation regex
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return url_pattern.match(url) is not None


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename by removing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    import re
    
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    
    # Limit length
    if len(filename) > 200:
        filename = filename[:200]
    
    return filename


def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to human-readable string.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted string (e.g., "2m 30s")
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"


def extract_urls(text: str) -> list[str]:
    """
    Extract all valid URLs from a text string.
    
    This function finds all HTTP/HTTPS URLs in the given text,
    allowing for mixed content like descriptions, comments, and URLs.
    
    Args:
        text: Text containing URLs (can be multi-line with mixed content)
        
    Returns:
        List of extracted URLs
    
    Examples:
        >>> extract_urls("Check out https://example.com and http://test.com")
        ['https://example.com', 'http://test.com']
        
        >>> extract_urls("Affiliate links\\nhttps://casino1.com\\nhttps://casino2.com")
        ['https://casino1.com', 'https://casino2.com']
    """
    import re
    
    # URL regex pattern that matches http:// or https:// URLs
    # This pattern is designed to extract URLs from mixed text
    url_pattern = re.compile(
        r'https?://'  # Match http:// or https://
        r'(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}'  # Domain name
        r'(?::[0-9]{1,5})?'  # Optional port
        r'(?:/[^\s]*)?',  # Optional path
        re.IGNORECASE
    )
    
    # Find all URLs in the text
    urls = url_pattern.findall(text)
    
    # Validate and return unique URLs
    valid_urls = []
    seen = set()
    for url in urls:
        # Remove trailing punctuation that might have been captured
        url = url.rstrip('.,;:!?)')
        if url not in seen and validate_url(url):
            valid_urls.append(url)
            seen.add(url)
    
    return valid_urls
