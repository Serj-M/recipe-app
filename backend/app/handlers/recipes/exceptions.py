from fastapi import status
from fastapi.exceptions import HTTPException

NotAvailableDB = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail='Данные не доступны')

AddConflict = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Конфликт при добавлении')

UpdateConflict = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Конфликт при изменении')

DeleteConflict = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Конфликт при удалении')

ErrorAddComment = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Ошибка при добавлении комментария')

OnlyTask = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Комментарий можно добавить только задаче')

TaskForTask = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Нельзя добавлять Задачу на другую Задачу. Исключением является если Задача без Этапа')

NotFoundId = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='В БД не существует запись с таким ИД'
)
