from fastapi import status
from fastapi.exceptions import HTTPException

NotAvailableDB = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail='Data not available')

AddConflict = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Conflict when adding')

UpdateConflict = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Conflict when editing')

DeleteConflict = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Conflict when deleting')
