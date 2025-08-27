import logging

from typing import Any, Optional, Dict
from fastapi import HTTPException

class LockedError(HTTPException):
    def __init__(self, status_code: int, detail: Any = None, headers: Optional[Dict[str, Any]] = None):
        logging.fatal(msg=detail)
        super().__init__(status_code=status_code, detail=detail, headers=headers)


def get_full_name(first_name: str, last_name: str) -> str:
    """Get user full name"""

    return f"{first_name} {last_name}"
