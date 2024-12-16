import unittest
from unittest.mock import patch, AsyncMock, MagicMock
from task_2 import Parser, BadRequest
import asyncio

class TestParser(unittest.TestCase):
    
    @patch.object(Parser, 'get_all_pages_urls')
    def test_parser(self, mock_get_all_pages_urls):
        # Настройка моков для requests.get
        mock_get_all_pages_urls.return_value = ['https://ru.wikipedia.org/w/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83&from=%D0%AF%D1%89']
        
        # Создание экземпляра Parser
        parser = Parser('', 10)

        result = parser.start()

        expected_result = {'Я': 17}
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()

