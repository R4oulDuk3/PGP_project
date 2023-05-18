from abc import ABC, abstractmethod
from enum import Enum
import rsa
from src.pgp.consts.consts import KeyType, AsymmetricEncryptionAlgorithm, SigningAlgorithm, SymmetricEncryptionAlgorithm


class Key(ABC):

    def __init__(self, key, key_type: KeyType, algorithm: Enum):
        self._key = key
        self._key_type = key_type
        self._algorithm = algorithm

    @abstractmethod
    def get_key(self):
        raise NotImplementedError()


class PrivateKey(Key, ABC):

    def __init__(self, key, algorithm: AsymmetricEncryptionAlgorithm | SigningAlgorithm):
        super().__init__(key, KeyType.PRIVATE, algorithm)


class PublicKey(Key, ABC):

    def __init__(self, key, algorithm: AsymmetricEncryptionAlgorithm | SigningAlgorithm):
        super().__init__(key, KeyType.PUBLIC, algorithm)


class SessionKey(Key, ABC):
    def __init__(self, key, algorithm: SymmetricEncryptionAlgorithm):
        super().__init__(key, KeyType.SESSION, algorithm)


class CAST128SessionKey(SessionKey):
    def __init__(self, key: bytes):
        if not isinstance(key, bytes):
            raise TypeError("key must be of type bytes")
        super().__init__(key, SymmetricEncryptionAlgorithm.CAST_128)

    def get_key(self) -> bytes:
        return self._key


class TripleDESSessionKey(SessionKey):
    def __init__(self, key: bytes):
        if not isinstance(key, bytes):
            raise TypeError("key must be of type bytes")
        if len(key) != 24:
            raise ValueError("key must be 24 bytes in length")
        super().__init__(key, SymmetricEncryptionAlgorithm.TRIPLE_DES)

    def get_key(self) -> bytes:
        return self._key


class KeyPair:

    def __init__(self, public_key: Key, private_key: Key, algorithm: AsymmetricEncryptionAlgorithm | SigningAlgorithm):
        self._public_key = public_key
        self._private_key = private_key
        self._algorithm = algorithm

    def get_public_key(self):
        return self._public_key

    def get_private_key(self):
        return self._private_key

    def get_algorithm(self):
        return self._algorithm


class RSAPrivateKey(PrivateKey):
    def __init__(self, key: rsa.PrivateKey):
        if not isinstance(key, rsa.PrivateKey):
            raise TypeError("key must be of type rsa.PrivateKey")
        super().__init__(key, AsymmetricEncryptionAlgorithm.RSA)

    def get_key(self) -> rsa.PrivateKey:
        return self._key

class RSAPublicKey(PublicKey):
    def __init__(self, key: rsa.PublicKey):
        if not isinstance(key, rsa.PublicKey):
            raise TypeError("key must be of type rsa.PublicKey")
        super().__init__(key, AsymmetricEncryptionAlgorithm.RSA)

    def get_key(self) -> rsa.PublicKey:
        return self._key
