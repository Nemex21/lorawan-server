"""
Encryption service for AES-256 message encryption
"""

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import base64
import logging
from app.config import settings

logger = logging.getLogger(__name__)


class EncryptionService:
    """Service for handling AES-256 encryption/decryption"""
    
    def __init__(self, key: str = None):
        """Initialize encryption service with AES key"""
        self.key = key or settings.AES_KEY
        
        # Ensure key is 32 bytes for AES-256
        if isinstance(self.key, str):
            key_bytes = self.key.encode('utf-8')
            # If key is less than 32 bytes, pad it
            if len(key_bytes) < 32:
                key_bytes = key_bytes.ljust(32, b'0')
            # If key is more than 32 bytes, truncate it
            elif len(key_bytes) > 32:
                key_bytes = key_bytes[:32]
            self.key = key_bytes
    
    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt plaintext using AES-256-GCM
        
        Args:
            plaintext: Text to encrypt
            
        Returns:
            Base64 encoded encrypted data with IV and tag
        """
        try:
            # Generate random IV
            iv = get_random_bytes(16)
            
            # Create cipher
            cipher = AES.new(self.key, AES.MODE_GCM, nonce=iv)
            
            # Encrypt
            ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode('utf-8'))
            
            # Combine IV + ciphertext + tag and encode to base64
            encrypted_data = iv + ciphertext + tag
            return base64.b64encode(encrypted_data).decode('utf-8')
        
        except Exception as e:
            logger.error(f"Encryption error: {e}")
            raise
    
    def decrypt(self, encrypted_data: str) -> str:
        """
        Decrypt AES-256-GCM encrypted data
        
        Args:
            encrypted_data: Base64 encoded encrypted data
            
        Returns:
            Decrypted plaintext
        """
        try:
            # Decode from base64
            encrypted_bytes = base64.b64decode(encrypted_data)
            
            # Extract IV, ciphertext, and tag
            iv = encrypted_bytes[:16]
            ciphertext = encrypted_bytes[16:-16]
            tag = encrypted_bytes[-16:]
            
            # Create cipher
            cipher = AES.new(self.key, AES.MODE_GCM, nonce=iv)
            
            # Decrypt and verify
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)
            return plaintext.decode('utf-8')
        
        except Exception as e:
            logger.error(f"Decryption error: {e}")
            raise


# Global encryption service instance
encryption_service = EncryptionService()
