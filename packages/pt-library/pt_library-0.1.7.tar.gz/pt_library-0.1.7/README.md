# PT Utility Package

- Time Decorator
  - decorator to calculate execution time.
  - `from pt_library import calculate_time`
- Notification
  - Currently, supports only Telegram Notifications.
  - `from pt_library import telegram_notification`
- DB Connection
  - Run Query on SQL and return records.
  - `from pt_library import run_query`
- Date time
  - Get the current month date (format: yyyy_mm_dd)
  - Get the previous month date (yyyy_mm)
  - Get the timestamp (yyyy-mm-dd HH:MM:SS) 
  - `from pt_library import get_previous_month_year, get_current_month_year, get_timestamp`