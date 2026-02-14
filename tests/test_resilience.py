import asyncio
import sys
import os
import unittest
from unittest.mock import AsyncMock, patch
import openai

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.base import BaseAIService
from app.core.exceptions import AppError

class TestAIResilience(unittest.IsolatedAsyncioTestCase):
    
    async def test_retry_on_rate_limit(self):
        """Tests if the service retries on OpenAI RateLimitError."""
        service = BaseAIService()
        mock_func = AsyncMock()
        
        # Simulate 2 failures followed by a success
        mock_response = AsyncMock()
        mock_response.headers = {}
        
        mock_func.side_effect = [
            openai.RateLimitError("Rate limit exceeded", response=mock_response, body={}),
            openai.RateLimitError("Rate limit exceeded", response=mock_response, body={}),
            "Success"
        ]

        
        with patch('app.services.base.logger') as mock_logger:
            result = await service.call_with_retry(mock_func)
            
            self.assertEqual(result, "Success")
            self.assertEqual(mock_func.call_count, 3)
            # Check if it logged the sleep/retry
            # (Tenacity logs via before_sleep_log)
            print("✅ Retry logic verified: 2 failures followed by success.")

    async def test_global_error_definition(self):
        """Verifies AppError structure."""
        err = AppError("Test Error")
        self.assertEqual(str(err), "Test Error")
        print("✅ AppError definition verified.")

if __name__ == "__main__":
    unittest.main()
