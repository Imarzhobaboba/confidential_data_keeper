from fastapi import APIRouter, Depends, Response
from typing import Annotated
from secret.schemas import SecretCreateSchema
from secret.service import SecretService
import dependency

# from secret.scheduler import scheduler_manager

router = APIRouter(prefix='/secret', tags=['secret'])

@router.post('/')
async def create_secret(
    secret_schema: SecretCreateSchema,
    secret_service: Annotated[SecretService, Depends(dependency=dependency.secret_service_dep)]
):
    access_key = secret_service.create_secret_and_return_access_key(body=secret_schema)
    return {'access_key': access_key}    

# @router.get('/get_by_id/{id}')
# async def get_secret_by_id(
#     secret_service: Annotated[SecretService, Depends(dependency=dependency.secret_service_dep)],
#     id: int
# ):
#     secret = secret_service.get_secret_by_id(id=id)
#     return {'secret': secret}

@router.get('/get_by_access_key/{access_key}')
async def get_secret_by_access_key(
    secret_service: Annotated[SecretService, Depends(dependency=dependency.secret_service_dep)],
    access_key: str
):
    secret = secret_service.get_secret_by_access_key(access_key=access_key)
    return {'secret': secret}

@router.delete('/{access_key}')
async def delete_secret(
    secret_service: Annotated[SecretService, Depends(dependency=dependency.secret_service_dep)],
    access_key: str
) -> Response:
    secret_service.delete_secret(access_key=access_key)
    return Response(status_code=204)

# @router.get("/scheduler/check/{access_key}")
# def check_job(access_key: str):
#     from secret.scheduler import scheduler
#     job = scheduler.get_job(f"secret_{access_key}")
#     return {
#         "exists": job is not None,
#         "next_run": job.next_run_time if job else None
#     }