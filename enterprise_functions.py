import os
import json
import requests
from datetime import datetime as pydatetime, timedelta, timezone
from typing import Optional, Callable, Any, Set
from dotenv import load_dotenv

load_dotenv()

# def fetch_datetime(
#     format_str: str = "%Y-%m-%d %H:%M:%S",    
#     unix_ts: int | None = None,
#     tz_offset_seconds: int | None = None
# ) -> str:
#     """
#     Returns either the current UTC date/time in the given format, or if unix_ts
#     is given, converts that timestamp to either UTC or local time (tz_offset_seconds).

#     :param format_str: The strftime format, e.g. "%Y-%m-%d %H:%M:%S".
#     :param unix_ts: Optional Unix timestamp. If provided, returns that specific time.
#     :param tz_offset_seconds: If provided, shift the datetime by this many seconds from UTC.
#     :return: A JSON string containing the "datetime" or an "error" key/value.
#     """
#     try:
#         # :param format_str: The strftime format, e.g. "%Y-%m-%d %H:%M:%S".
#         # format_str = "%Y-%m-%d %H:%M:%S"
        
#         if unix_ts is not None:
#             dt_utc = pydatetime.fromtimestamp(unix_ts, tz=timezone.utc)
#         else:
#             dt_utc = pydatetime.now(timezone.utc)

#         if tz_offset_seconds is not None:
#             local_tz = timezone(timedelta(seconds=tz_offset_seconds))
#             dt_local = dt_utc.astimezone(local_tz)
#             result_str = dt_local.strftime(format_str)
#         else:
#             result_str = dt_utc.strftime(format_str)

#         return json.dumps({"datetime": result_str})
#     except Exception as e:
#         return json.dumps({"error": f"Exception: {str(e)}"})
    

def fetch_datetime() -> str:
    """
    Returns either the current UTC date/time
    :return: A JSON string containing the "datetime" or an "error" key/value.
    """
    try:
        # :param format_str: The strftime format, e.g. "%Y-%m-%d %H:%M:%S".
        # format_str = "%Y-%m-%d %H:%M:%S"

        format_str: str = "%Y-%m-%d %H:%M:%S"
        unix_ts: int = None
        tz_offset_seconds: int = None
        
        if unix_ts is not None:
            dt_utc = pydatetime.fromtimestamp(unix_ts, tz=timezone.utc)
        else:
            dt_utc = pydatetime.now(timezone.utc)

        if tz_offset_seconds is not None:
            local_tz = timezone(timedelta(seconds=tz_offset_seconds))
            dt_local = dt_utc.astimezone(local_tz)
            result_str = dt_local.strftime(format_str)
        else:
            result_str = dt_utc.strftime(format_str)

        return json.dumps({"datetime": result_str})
    except Exception as e:
        return json.dumps({"error": f"Exception: {str(e)}"})

    
# make functions callable a callable set from enterprise-streaming-agent.ipynb
enterprise_fns: Set[Callable[..., Any]] = {
    # fetch_datetime,
}