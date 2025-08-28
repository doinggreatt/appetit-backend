import logging

from fastapi import HTTPException

from config import get_module_logger




class InternalError(Exception):

    def __init__(self, message, *, module_name = None):
        self.logger: logging.Logger = get_module_logger(module_name)
        super().__init__(message)

    def handle(self):
        self.logger.error(self)
        raise HTTPException(status_code=500, detail="Error occured. Try to contact administrator.")




