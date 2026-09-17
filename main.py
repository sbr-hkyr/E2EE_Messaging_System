from user_manager import (
    create_user,
    user_exists
)

from messaging import (
    send_message,
    decrypt_received_message
)

from server import get_messages


def create_new_user():
    username = input(
        "Enter username: "
    ).strip()

    if not username:
        print("Username cannot be empty.")
        return

    create_user(username)


def send_new_message():

    sender = input(
        "Sender username: "
    ).strip()

    recipient = input(
        "Recipient username: "
    ).strip()

    if not user_exists(sender):
        print("Sender does not exist.")
        return

    if not user_exists(recipient):
        print("Recipient does not exist.")
        return

    message = input(
        "Enter message: "
    )

    send_message(
        sender,
        recipient,
        message
    )


def receive_messages():

    username = input(
        "Enter your username: "
    ).strip()

    if not user_exists(username):
        print("User does not exist.")
        return

    messages = get_messages(
        username
    )

    if not messages:
        print("\nNo messages found.")
        return

    print(
        f"\nYou have {len(messages)} message(s)."
    )

    for message in messages:

        print("\n------------------------------")

        print(
            "Message ID:",
            message["message_id"]
        )

        print(
            "Sender:",
            message["sender"]
        )

        try:

            plaintext = decrypt_received_message(
                message
            )

            print(
                "Decrypted message:",
                plaintext
            )

        except Exception as error:

            print(
                "ERROR: Message could not be decrypted."
            )

            print(
                "Reason:",
                type(error).__name__
            )


def main():

    while True:

        print("\n================================")
        print(" END-TO-END ENCRYPTED MESSAGING")
        print("================================")

        print("1. Create user")
        print("2. Send message")
        print("3. Receive messages")
        print("4. Exit")

        choice = input(
            "\nChoose an option: "
        )

        if choice == "1":

            create_new_user()

        elif choice == "2":

            send_new_message()

        elif choice == "3":

            receive_messages()

        elif choice == "4":

            print("Goodbye!")
            break

        else:

            print("Invalid option.")


if __name__ == "__main__":
    main()