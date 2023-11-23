"""
Module for formatting time tuples into standardized string representations.
"""

class TimeFormatter:
    """Facilitates formatting of time tuples into readable string formats."""

    def format_time(self, t):
        """
        Converts a time tuple into 'YYYY-MM-DD HH:MM:SS' format.
        """

        try:
            # Format and return the time string
            year, month, day, hour, minute, second, _, _ = t
            return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(year, month, day, hour, minute, second)
        except Exception as e:
            # Handle formatting errors
            print("Error formatting time:", e)
            return None