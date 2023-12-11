import uuid
from .. import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from ..database import get_db
from app.oauth2 import require_user

router = APIRouter()


# @router.get('/', response_model=schemas.ListTaskResponse)
# def get_posts(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = '', user_id: str = Depends(require_user)):
#     skip = (page - 1) * limit

#     tasks = db.query(models.Task).group_by(models.Task.id).filter(
#         models.Task.title.contains(search)).limit(limit).offset(skip).all()
#     return {'status': 'success', 'results': len(tasks), 'posts': tasks}


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.TaskResponse)
def create_task(task: schemas.CreateTaskSchema, db: Session = Depends(get_db), owner_id: str = Depends(require_user)):
    task.user_id = uuid.UUID(owner_id)
    task.status = str(schemas.TaskStatusEnum.Pending)
    new_task = models.Task(**task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


# @router.put('/{id}', response_model=schemas.TaskResponse)
# def update_post(id: str, task: schemas.UpdateTaskSchema, db: Session = Depends(get_db), user_id: str = Depends(require_user)):
#     task_query = db.query(models.Task).filter(models.Task.id == id)
#     updated_task = task_query.first()

#     if not updated_task:
#         raise HTTPException(status_code=status.HTTP_200_OK,
#                             detail=f'No post with this id: {id} found')
#     if updated_task.user_id != uuid.UUID(user_id):
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
#                             detail='You are not allowed to perform this action')
#     task.user_id = user_id
#     task_query.update(task.dict(exclude_unset=True), synchronize_session=False)
#     db.commit()
#     return updated_task


@router.get('/{id}', response_model=schemas.TaskResponse)
def get_task(id: str, db: Session = Depends(get_db), user_id: str = Depends(require_user)):
    task = db.query(models.Task).filter(models.Task.id == id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No task with this id: {id} found")
    return task

# @router.delete('/{id}')
# def delete_post(id: str, db: Session = Depends(get_db), user_id: str = Depends(require_user)):
#     task_query = db.query(models.Task).filter(models.Task.id == id)
#     task = task_query.first()
#     if not task:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f'No task with this id: {id} found')

#     if str(task.user_id) != user_id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
#                             detail='You are not allowed to perform this action')
#     task_query.delete(synchronize_session=False)
#     db.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

