import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from app.services.pinecone_service import PineconeService

@pytest.fixture
def mock_index():
    return MagicMock()

@pytest.fixture
def service(mock_index):
    with patch('app.services.pinecone_service.index', mock_index):
        svc = PineconeService()
        svc.index = mock_index
        return svc

@pytest.mark.asyncio
async def test_upsert_candidate(service, mock_index):
    # Arrange
    # Since embed and upsert are called via run_in_executor, 
    # we patch the calls themselves or the functions.
    # We patch 'app.services.pinecone_service.embed' because it's called inside the service.
    with patch('app.services.pinecone_service.embed', return_value=[0.1, 0.2, 0.3]) as mock_embed:
        candidate_id = "test-id"
        rich_text = "Name: John | Seniority: Senior | Skills: Python | Summary: Test"
        metadata = {"name": "John Doe"}

        # Act
        result_id = await service.upsert_candidate(rich_text, metadata, candidate_id)

        # Assert
        assert result_id == candidate_id
        mock_embed.assert_called_once_with(rich_text)
        assert mock_index.upsert.called

@pytest.mark.asyncio
async def test_get_candidate(service, mock_index):
    # Arrange
    candidate_id = "test-id"
    expected_vector = {"id": candidate_id, "values": [0.1, 0.2], "metadata": {"name": "John"}}
    
    mock_fetch_result = MagicMock()
    mock_fetch_result.vectors = {candidate_id: expected_vector}
    mock_index.fetch.return_value = mock_fetch_result

    # Act
    result = await service.get_candidate(candidate_id)

    # Assert
    assert result == expected_vector
    mock_index.fetch.assert_called_once_with(ids=[candidate_id])

@pytest.mark.asyncio
async def test_delete_candidate(service, mock_index):
    # Arrange
    candidate_id = "test-id"

    # Act
    result = await service.delete_candidate(candidate_id)

    # Assert
    assert result is True
    mock_index.delete.assert_called_once_with(ids=[candidate_id])

@pytest.mark.asyncio
async def test_search_candidates(service, mock_index):
    # Arrange
    with patch('app.services.pinecone_service.embed', return_value=[0.1, 0.2, 0.3]) as mock_embed:
        query = "find me"
        
        mock_query_result = MagicMock()
        mock_match = MagicMock()
        mock_match.score = 0.95
        mock_match.to_dict.return_value = {"id": "match-1", "score": 0.95}
        mock_query_result.matches = [mock_match]
        mock_index.query.return_value = mock_query_result

        # Act
        results = await service.search_candidates(query)

        # Assert
        assert len(results) == 1
        assert results[0]["id"] == "match-1"
        mock_embed.assert_called_once_with(query)
        assert mock_index.query.called
