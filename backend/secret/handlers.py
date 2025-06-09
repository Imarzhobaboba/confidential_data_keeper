from fastapi import APIRouter, Depends, Response
from typing import Annotated
from secret.schemas import SecretCreateSchema, SecretUpdateSchema
from secret.service import SecretService
import dependency


router = APIRouter(prefix='/secret', tags=['secret'])

@router.post('/')
async def create_secret(
    secret_schema: SecretCreateSchema,
    secret_service: Annotated[SecretService, Depends(dependency=dependency.secret_service_dep)]
):
    access_key = secret_service.create_secret_and_return_access_key(body=secret_schema)
    return {'access_key': access_key}    


@router.get('/{access_key}')
async def get_secret_by_access_key(
    secret_service: Annotated[SecretService, Depends(dependency=dependency.secret_service_dep)],
    access_key: str
):
    secret = secret_service.get_secret_by_access_key(access_key=access_key)
    return {'secret': secret}


@router.patch('/{access_key}')
async def update_secret(
    secret_schema: SecretUpdateSchema,
    secret_service: Annotated[SecretService, Depends(dependency=dependency.secret_service_dep)]
):
    secret_service.update_secret(body=secret_schema)
    return {'data': 'secret is updated'}


@router.delete('/{access_key}')
async def delete_secret(
    secret_service: Annotated[SecretService, Depends(dependency=dependency.secret_service_dep)],
    access_key: str
) -> None:
    secret_service.delete_secret(access_key=access_key)
    return Response(status_code=204)
