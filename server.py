import os
import json
import uuid


STORAGE_FOLDER = "server_storage"


def initialize_server():
    """
    Create server storage directory.
    """

    if not os.path.exists(STORAGE_FOLDER):
        os.makedirs(STORAGE_FOLDER)


def store_message(sender, recipient, message_package):
    """
    Store encrypted message on the server.
    """

    initialize_server()

    message_id = str(uuid.uuid4())

    message_data = {
        "message_id": message_id,
        "sender": sender,
        "recipient": recipient,
        "encrypted_message": message_package
    }

    filename = os.path.join(
        STORAGE_FOLDER,
        message_id + ".json"
    )

    with open(filename, "w") as file:
        json.dump(message_data, file, indent=4)

    return message_id


def get_messages(recipient):
    """
    Retrieve encrypted messages for a recipient.
    """

    initialize_server()

    messages = []

    for filename in os.listdir(STORAGE_FOLDER):

        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(
            STORAGE_FOLDER,
            filename
        )

        with open(filepath, "r") as file:
            data = json.load(file)

        if data["recipient"] == recipient:
            messages.append(data)

    return messages