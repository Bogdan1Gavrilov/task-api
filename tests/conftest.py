import sys
from unittest.mock import MagicMock

# Мокаем проблемный импорт
import huggingface_hub
if not hasattr(huggingface_hub, 'HfFolder'):
    # Создаем заглушку для HfFolder
    class HfFolderMock:
        @staticmethod
        def get_token():
            return None
        @staticmethod
        def save_token(token):
            pass
        @staticmethod
        def delete_token():
            pass
    
    setattr(huggingface_hub, 'HfFolder', HfFolderMock)

# Теперь импортируем приложение
from app.main import app