import os

from crypto_utils import (
    generate_rsa_key_pair,
    save_private_key,
    save_public_key,
    load_private_key,
    load_public_key
)


USERS_FOLDER = "users"


def initialize_users_folder():
    """
    Create users directory if it does not exist.
    """

    if not os.path.exists(USERS_FOLDER):
        os.makedirs(USERS_FOLDER)


def create_user(username):
    """
    Create an RSA key pair for a new user.
    """

    initialize_users_folder()

    user_folder = os.path.join(
        USERS_FOLDER,
        username
    )

    if os.path.exists(user_folder):
        print(f"User '{username}' already exists.")
        return False

    os.makedirs(user_folder)

    private_key, public_key = generate_rsa_key_pair()

    private_key_path = os.path.join(
        user_folder,
        "private_key.pem"
    )

    public_key_path = os.path.join(
        user_folder,
        "public_key.pem"
    )

    save_private_key(
        private_key,
        private_key_path
    )

    save_public_key(
        public_key,
        public_key_path
    )

    print(f"User '{username}' created successfully.")

    return True


def get_private_key(username):
    """
    Load user's private key.
    """

    path = os.path.join(
        USERS_FOLDER,
        username,
        "private_key.pem"
    )

    return load_private_key(path)


def get_public_key(username):
    """
    Load user's public key.
    """

    path = os.path.join(
        USERS_FOLDER,
        username,
        "public_key.pem"
    )

    return load_public_key(path)


def user_exists(username):
    """
    Check whether a user exists.
    """

    path = os.path.join(
        USERS_FOLDER,
        username
    )

    return os.path.exists(path)