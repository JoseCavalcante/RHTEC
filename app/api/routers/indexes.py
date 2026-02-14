from fastapi import APIRouter
from app.services.index_service import create_index, list_index, detail_index

router = APIRouter()

# Note: index_service.py functions seem to be sync (wrappers around Pinecone). 
# If they are blocking, they should be wrapped in run_in_executor or refactored to async.
# For this sprint, we prioritize candidate operations, but let's check index_service validity.

@router.post('/api/index/create', summary='create index from pinecone', tags=["Indexes"])
async def create_index_router(name_index : str):
    # Potential blocking call
    response = create_index(name_index)
    return {f"the index {response}"}

@router.get('/api/index/list', summary='list index from pinecone', tags=["Indexes"])
async def list_index_router():
    # Potential blocking call
    response = list_index()
    return response

@router.post('/api/index/detail', summary='detail index from pinecone', tags=["Indexes"])
async def detail_index_router(name_index:str):
    # Potential blocking call
    response = detail_index(name_index)
    return response
