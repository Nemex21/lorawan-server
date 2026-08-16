"""
Encryption service for message content
"""

from cryptography.fernet import Fernet
from app.config import settings
import base64


class EncryptionService:
    """Service for encrypting and decrypting message content"""
    
    def __init__(self):
        """Initialize encryption service with key from settings"""
        # Use settings key or generate new one
        self.key = settings.ENCRYPTION_KEY.encode() if isinstance(settings.ENCRYPTION_KEY, str) else settings.ENCRYPTION_KEY
        self.cipher = Fernet(self.key)
    
    def encrypt(self, content: str) -> str:
        """Encrypt content"""
        if not content:
            return content
        
        try:
            # Encode string to bytes
            content_bytes = content.encode('utf-8')
            # Encrypt
            encrypted = self.cipher.encrypt(content_bytes)
            # Return as string
            return encrypted.decode('utf-8')
        except Exception as e:
            raise ValueError(f"Encryption failed: {str(e)}")
    
    def decrypt(self, content: str) -> str:
        """Decrypt content"""
        if not content:
            return content
        
        try:
            # Encode string to bytes
            content_bytes = content.encode('utf-8')
            # Decrypt
            decrypted = self.cipher.decrypt(content_bytes)
            # Return as string
            return decrypted.decode('utf-8')
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")
    
    @staticmethod
    def generate_key() -> str:
        """Generate a new encryption key"""
        return Fernet.generate_key().decode('utf-8')


# Initialize encryption service
encryption_service = EncryptionService()
