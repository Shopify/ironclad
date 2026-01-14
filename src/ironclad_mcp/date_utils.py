"""
Date parsing utilities for consistent timezone-aware datetime handling
"""
from datetime import datetime, timezone
from typing import Optional, Tuple
import re


class DateParser:
    """Utility class for parsing dates into timezone-aware datetime objects"""
    
    @staticmethod
    def parse_date(date_str: Optional[str]) -> Optional[datetime]:
        """
        Parse a date string into a timezone-aware datetime object
        
        Handles various formats:
        - ISO 8601: 2025-12-31T23:59:59Z or 2025-12-31T23:59:59+00:00
        - Date only: 2025-12-31 (assumes start of day UTC)
        
        Args:
            date_str: Date string to parse
        
        Returns:
            Timezone-aware datetime object, or None if date_str is None/empty
        """
        if not date_str:
            return None
        
        date_str = date_str.strip()
        
        # Try ISO format with timezone first
        try:
            # Handle Z suffix (Zulu time = UTC)
            if date_str.endswith('Z'):
                date_str = date_str[:-1] + '+00:00'
            
            # Try parsing with fromisoformat
            dt = datetime.fromisoformat(date_str)
            
            # If no timezone info, assume UTC
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            
            return dt
        except ValueError:
            pass
        
        # Try date-only format (YYYY-MM-DD)
        try:
            # Parse the date components
            match = re.match(r'(\d{4})-(\d{2})-(\d{2})', date_str)
            if match:
                year, month, day = map(int, match.groups())
                # Create timezone-aware datetime at start of day UTC
                return datetime(year, month, day, 0, 0, 0, tzinfo=timezone.utc)
        except ValueError:
            pass
        
        raise ValueError(f"Could not parse date: {date_str}")
    
    @staticmethod
    def parse_date_range(
        date_from: Optional[str],
        date_to: Optional[str]
    ) -> Tuple[Optional[datetime], Optional[datetime]]:
        """
        Parse a date range into timezone-aware datetime objects
        
        Args:
            date_from: Start date string
            date_to: End date string
        
        Returns:
            Tuple of (start_datetime, end_datetime)
        """
        date_from_obj = DateParser.parse_date(date_from) if date_from else None
        date_to_obj = DateParser.parse_date(date_to) if date_to else None
        
        # If only date_to is provided, set it to end of day
        if date_to_obj and not date_from_obj:
            date_to_obj = date_to_obj.replace(hour=23, minute=59, second=59)
        
        # If only date_from is provided, set date_to to end of day
        if date_from_obj and not date_to_obj:
            date_to_obj = date_from_obj.replace(hour=23, minute=59, second=59)
        
        # If date_to is provided but has time 00:00:00, set to end of day
        if date_to_obj and date_to_obj.hour == 0 and date_to_obj.minute == 0 and date_to_obj.second == 0:
            date_to_obj = date_to_obj.replace(hour=23, minute=59, second=59)
        
        return date_from_obj, date_to_obj







