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
    access_key = await secret_service.create_secret_and_return_access_key(body=secret_schema)
    return {'access_key': access_key}    


@router.get('/{access_key}')
async def get_secret(
    secret_service: Annotated[SecretService, Depends(dependency=dependency.secret_service_dep)],
    access_key: str
):
    secret = await secret_service.get_secret_by_access_key(access_key=access_key)
    return {'secret': secret}


@router.patch('/{access_key}')
async def update_secret(
    access_key: str,
    secret_schema: SecretUpdateSchema,
    secret_service: Annotated[SecretService, Depends(dependency=dependency.secret_service_dep)]
):
    await secret_service.update_secret(access_key=access_key, body=secret_schema)
    return Response(status_code=204)


@router.delete('/{access_key}')
async def delete_secret(
    secret_service: Annotated[SecretService, Depends(dependency=dependency.secret_service_dep)],
    access_key: str
) -> None:
    await secret_service.delete_secret(access_key=access_key)
    return Response(status_code=204)

@router.get('/lifetime/{access_key}')
async def get_secret_lifetime(
    secret_service: Annotated[SecretService, Depends(dependency=dependency.secret_service_dep)],
    access_key: str
):
    expires_at = await secret_service.get_secret_lifetime(access_key=access_key)
    return {'data': expires_at}
