"""
Encryption service for message content
"""

from cryptography.fernet import Fernet
from app.config import settings
import base64
import hashlib


class EncryptionService:
    """
    Service for encrypting and decrypting message content
    """
    
    def __init__(self):
        """
        Initialize the encryption service with a key from settings
        """
        # Derive a key from the secret key in settings
        key_material = settings.SECRET_KEY.encode()
        # Use base64 encoding to create a valid Fernet key
        key = base64.urlsafe_b64encode(hashlib.sha256(key_material).digest())
        self.cipher = Fernet(key)
    
    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt plaintext string
        
        Args:
            plaintext: The string to encrypt
            
        Returns:
            Encrypted string (base64 encoded)
        """
        if not plaintext:
            return plaintext
        
        # Encode plaintext to bytes
        plaintext_bytes = plaintext.encode()
        
        # Encrypt
        encrypted_bytes = self.cipher.encrypt(plaintext_bytes)
        
        # Return as string
        return encrypted_bytes.decode()
    
    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypt ciphertext string
        
        Args:
            ciphertext: The encrypted string to decrypt
            
        Returns:
            Decrypted plaintext string
            
        Raises:
            cryptography.fernet.InvalidToken: If decryption fails
        """
        if not ciphertext:
            return ciphertext
        
        # Encode ciphertext to bytes
        ciphertext_bytes = ciphertext.encode()
        
        # Decrypt
        plaintext_bytes = self.cipher.decrypt(ciphertext_bytes)
        
        # Return as string
        return plaintext_bytes.decode()


# Create a singleton instance
encryption_service = EncryptionService()
