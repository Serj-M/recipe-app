from fastapi import status
from fastapi.exceptions import HTTPException

NotAvailableDB = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail='Data not available.')

AddConflict = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Conflict when adding. A prescription with this Title already exists.')

UpdateConflict = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Conflict when editing. Check uniqueness of title.')

DeleteConflict = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Error when deleting.')

NotFoundId = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='There is no record in the database with this ID.'
)
