import base64
import os

from crypto_utils import (
    encrypt_message,
    decrypt_message,
    encrypt_session_key,
    decrypt_session_key,
    sign_message,
    verify_signature
)

from user_manager import (
    get_public_key,
    get_private_key
)

from server import store_message


def send_message(sender, recipient, message):
    """
    Encrypt, sign, and send a message.
    """

    print("\n[1] Generating AES-256 session key...")

    # Generate a random 256-bit AES key
    aes_key = os.urandom(32)

    print("[2] Encrypting message using AES-256-GCM...")

    # Encrypt the plaintext
    nonce, encrypted_data = encrypt_message(
        message,
        aes_key
    )

    print("[3] Encrypting AES session key using RSA-OAEP...")

    # Get recipient's public key
    recipient_public_key = get_public_key(
        recipient
    )

    # Protect AES session key using recipient's public key
    encrypted_aes_key = encrypt_session_key(
        aes_key,
        recipient_public_key
    )

    # --------------------------------------------------------
    # DIGITAL SIGNATURE
    # --------------------------------------------------------

    print("[4] Creating RSA-PSS digital signature...")

    # Get sender's private key
    sender_private_key = get_private_key(
        sender
    )

    # Data that will be signed
    data_to_sign = (
        nonce +
        encrypted_data +
        encrypted_aes_key
    )

    # Create RSA-PSS signature
    signature = sign_message(
        data_to_sign,
        sender_private_key
    )

    # --------------------------------------------------------
    # CREATE MESSAGE PACKAGE
    # --------------------------------------------------------

    message_package = {

    "encryption_algorithm": "AES-256-GCM",

    "key_encryption_algorithm": "RSA-OAEP-SHA256",

    "signature_algorithm": "RSA-PSS-SHA256",

    "nonce": base64.b64encode(
        nonce
    ).decode("utf-8"),

    "ciphertext": base64.b64encode(
        encrypted_data
    ).decode("utf-8"),

    "encrypted_session_key": base64.b64encode(
        encrypted_aes_key
    ).decode("utf-8"),

    "signature": base64.b64encode(
        signature
    ).decode("utf-8")
}

    print("[5] Sending encrypted and signed package to server...")

    message_id = store_message(
        sender,
        recipient,
        message_package
    )

    print("\nMessage encrypted and signed successfully.")

    print(
        "Message ID:",
        message_id
    )

    return message_id


def decrypt_received_message(message_data):
    """
    Verify the sender's RSA-PSS signature,
    then decrypt the received message.
    """

    username = message_data["recipient"]

    sender = message_data["sender"]

    package = message_data["encrypted_message"]

    # --------------------------------------------------------
    # LOAD KEYS
    # --------------------------------------------------------

    print("\n[1] Loading recipient private key...")

    recipient_private_key = get_private_key(
        username
    )

    print("[2] Loading sender public key...")

    sender_public_key = get_public_key(
        sender
    )

    # --------------------------------------------------------
    # DECODE MESSAGE DATA
    # --------------------------------------------------------

    encrypted_aes_key = base64.b64decode(
        package["encrypted_session_key"]
    )

    nonce = base64.b64decode(
        package["nonce"]
    )

    encrypted_data = base64.b64decode(
        package["ciphertext"]
    )

    signature = base64.b64decode(
        package["signature"]
    )

    # --------------------------------------------------------
    # VERIFY DIGITAL SIGNATURE
    # --------------------------------------------------------

    print("[3] Verifying RSA-PSS digital signature...")

    data_to_verify = (
        nonce +
        encrypted_data +
        encrypted_aes_key
    )

    signature_valid = verify_signature(
        data_to_verify,
        signature,
        sender_public_key
    )

    if not signature_valid:

        print("\nSIGNATURE VERIFICATION FAILED!")

        raise ValueError(
            "Invalid digital signature."
        )

    print("Signature verification successful.")

    # --------------------------------------------------------
    # RECOVER AES SESSION KEY
    # --------------------------------------------------------

    print(
        "[4] Decrypting AES session key using RSA-OAEP..."
    )

    aes_key = decrypt_session_key(
        encrypted_aes_key,
        recipient_private_key
    )

    # --------------------------------------------------------
    # DECRYPT MESSAGE
    # --------------------------------------------------------

    print(
        "[5] Decrypting message using AES-256-GCM..."
    )

    plaintext = decrypt_message(
        nonce,
        encrypted_data,
        aes_key
    )

    return plaintext