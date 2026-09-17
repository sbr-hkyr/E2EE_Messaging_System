import os

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding

# ============================================================
# RSA KEY GENERATION
# ============================================================

def generate_rsa_key_pair():
    """
    Generate an RSA-2048 public/private key pair.
    """

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    public_key = private_key.public_key()

    return private_key, public_key


# ============================================================
# SAVE RSA PRIVATE KEY
# ============================================================

def save_private_key(private_key, filename):
    """
    Save RSA private key to a PEM file.
    """

    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    with open(filename, "wb") as file:
        file.write(pem)


# ============================================================
# SAVE RSA PUBLIC KEY
# ============================================================

def save_public_key(public_key, filename):
    """
    Save RSA public key to a PEM file.
    """

    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open(filename, "wb") as file:
        file.write(pem)


# ============================================================
# LOAD RSA PRIVATE KEY
# ============================================================

def load_private_key(filename):
    """
    Load an RSA private key from a PEM file.
    """

    with open(filename, "rb") as file:
        private_key = serialization.load_pem_private_key(
            file.read(),
            password=None
        )

    return private_key


# ============================================================
# LOAD RSA PUBLIC KEY
# ============================================================

def load_public_key(filename):
    """
    Load an RSA public key from a PEM file.
    """

    with open(filename, "rb") as file:
        public_key = serialization.load_pem_public_key(
            file.read()
        )

    return public_key


# ============================================================
# AES-256-GCM ENCRYPTION
# ============================================================

def encrypt_message(message, aes_key):
    """
    Encrypt a plaintext message using AES-256-GCM.
    """

    aes = AESGCM(aes_key)

    # 96-bit random nonce
    nonce = os.urandom(12)

    plaintext = message.encode("utf-8")

    encrypted_data = aes.encrypt(
        nonce,
        plaintext,
        None
    )

    return nonce, encrypted_data


# ============================================================
# AES-256-GCM DECRYPTION
# ============================================================

def decrypt_message(nonce, encrypted_data, aes_key):
    """
    Decrypt AES-256-GCM encrypted data.
    """

    aes = AESGCM(aes_key)

    plaintext = aes.decrypt(
        nonce,
        encrypted_data,
        None
    )

    return plaintext.decode("utf-8")


# ============================================================
# RSA-OAEP ENCRYPTION
# ============================================================

def encrypt_session_key(aes_key, recipient_public_key):
    """
    Encrypt AES session key using recipient's RSA public key.
    """

    encrypted_key = recipient_public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(
                algorithm=hashes.SHA256()
            ),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return encrypted_key


# ============================================================
# RSA-OAEP DECRYPTION
# ============================================================

def decrypt_session_key(encrypted_key, private_key):
    """
    Recover AES session key using recipient's RSA private key.
    """

    aes_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(
                algorithm=hashes.SHA256()
            ),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return aes_key
# ============================================================
# RSA-PSS DIGITAL SIGNATURE
# ============================================================

def sign_message(data, private_key):
    """
    Create an RSA-PSS digital signature.

    The sender signs the protected message data
    using their RSA private key.
    """

    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    return signature


# ============================================================
# RSA-PSS SIGNATURE VERIFICATION
# ============================================================

def verify_signature(data, signature, public_key):
    """
    Verify an RSA-PSS digital signature.

    Returns True if the signature is valid.
    Returns False if the signature is invalid.
    """

    try:

        public_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        return True

    except Exception:

        return False