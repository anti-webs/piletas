# Utility functions for the application

def format_currency(value):
    """Format a number as currency in Euro format"""
    if isinstance(value, (int, float)):
        return f"€{value:,.2f}"
    return value
