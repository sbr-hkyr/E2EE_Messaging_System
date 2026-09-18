import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

from user_manager import create_user, user_exists
from messaging import send_message, decrypt_received_message
from server import get_messages


class E2EEApp:
    def __init__(self, root):
        self.root = root
        self.root.title("End-to-End Encrypted Messaging System")
        self.root.geometry("750x650")
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        # Title
        title = tk.Label(
            self.root,
            text="END-TO-END ENCRYPTED MESSAGING",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=15)

        subtitle = tk.Label(
            self.root,
            text="AES-256-GCM | RSA-OAEP | RSA-PSS",
            font=("Arial", 10)
        )
        subtitle.pack(pady=5)

        # Notebook
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=20, pady=15)

        # Create User tab
        self.create_user_tab(notebook)

        # Send Message tab
        self.create_send_tab(notebook)

        # Receive Messages tab
        self.create_receive_tab(notebook)

    # --------------------------------------------------
    # CREATE USER TAB
    # --------------------------------------------------

    def create_user_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Create User")

        ttk.Label(
            frame,
            text="Create New User",
            font=("Arial", 14, "bold")
        ).pack(pady=25)

        ttk.Label(frame, text="Username:").pack(pady=5)

        self.new_username_entry = ttk.Entry(frame, width=35)
        self.new_username_entry.pack(pady=5)

        ttk.Button(
            frame,
            text="Create User",
            command=self.create_user_gui
        ).pack(pady=20)

        ttk.Label(
            frame,
            text=(
                "A 2048-bit RSA key pair will be generated.\n"
                "The private key is used for RSA-PSS signing.\n"
                "The public key is used for signature verification."
            ),
            justify="center"
        ).pack(pady=20)

    def create_user_gui(self):
        username = self.new_username_entry.get().strip()

        if not username:
            messagebox.showwarning(
                "Input Error",
                "Please enter a username."
            )
            return

        if create_user(username):
            messagebox.showinfo(
                "Success",
                f"User '{username}' created successfully."
            )
            self.new_username_entry.delete(0, tk.END)
        else:
            messagebox.showerror(
                "Error",
                f"User '{username}' already exists."
            )

    # --------------------------------------------------
    # SEND MESSAGE TAB
    # --------------------------------------------------

    def create_send_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Send Message")

        ttk.Label(
            frame,
            text="Send Encrypted Message",
            font=("Arial", 14, "bold")
        ).pack(pady=20)

        # Sender
        ttk.Label(frame, text="Sender:").pack(pady=5)

        self.sender_entry = ttk.Entry(frame, width=40)
        self.sender_entry.pack(pady=5)

        # Recipient
        ttk.Label(frame, text="Recipient:").pack(pady=5)

        self.recipient_entry = ttk.Entry(frame, width=40)
        self.recipient_entry.pack(pady=5)

        # Message
        ttk.Label(frame, text="Message:").pack(pady=5)

        self.message_text = scrolledtext.ScrolledText(
            frame,
            width=65,
            height=10,
            wrap=tk.WORD
        )
        self.message_text.pack(pady=5)

        ttk.Button(
            frame,
            text="Encrypt & Send",
            command=self.send_message_gui
        ).pack(pady=15)

        # Status
        self.send_status = ttk.Label(
            frame,
            text="",
            wraplength=600,
            justify="center"
        )
        self.send_status.pack(pady=5)

    def send_message_gui(self):
        sender = self.sender_entry.get().strip()
        recipient = self.recipient_entry.get().strip()
        message = self.message_text.get("1.0", tk.END).strip()

        if not sender or not recipient or not message:
            messagebox.showwarning(
                "Input Error",
                "Please fill in all fields."
            )
            return

        if not user_exists(sender):
            messagebox.showerror(
                "Error",
                f"Sender '{sender}' does not exist."
            )
            return

        if not user_exists(recipient):
            messagebox.showerror(
                "Error",
                f"Recipient '{recipient}' does not exist."
            )
            return

        try:
            message_id = send_message(
                sender,
                recipient,
                message
            )

            self.send_status.config(
                text=(
                    "Message sent successfully!\n"
                    f"Message ID: {message_id}\n\n"
                    "The message was encrypted using AES-256-GCM.\n"
                    "The AES key was protected using RSA-OAEP.\n"
                    "The message was signed using RSA-PSS."
                )
            )

            self.message_text.delete("1.0", tk.END)

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"Message could not be sent.\n\n{type(error).__name__}: {error}"
            )

    # --------------------------------------------------
    # RECEIVE MESSAGES TAB
    # --------------------------------------------------

    def create_receive_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Receive Messages")

        ttk.Label(
            frame,
            text="Receive Messages",
            font=("Arial", 14, "bold")
        ).pack(pady=20)

        ttk.Label(frame, text="Username:").pack(pady=5)

        self.receive_username_entry = ttk.Entry(
            frame,
            width=40
        )
        self.receive_username_entry.pack(pady=5)

        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=10)

        ttk.Button(
            button_frame,
            text="Check Messages",
            command=self.receive_messages_gui
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear_messages
        ).pack(side=tk.LEFT, padx=5)

        self.messages_text = scrolledtext.ScrolledText(
            frame,
            width=75,
            height=22,
            wrap=tk.WORD
        )
        self.messages_text.pack(padx=15, pady=10)

    def receive_messages_gui(self):
        username = self.receive_username_entry.get().strip()

        if not username:
            messagebox.showwarning(
                "Input Error",
                "Please enter your username."
            )
            return

        if not user_exists(username):
            messagebox.showerror(
                "Error",
                f"User '{username}' does not exist."
            )
            return

        try:
            messages = get_messages(username)

            self.messages_text.delete("1.0", tk.END)

            if not messages:
                self.messages_text.insert(
                    tk.END,
                    "No messages found."
                )
                return

            self.messages_text.insert(
                tk.END,
                f"You have {len(messages)} message(s).\n"
            )
            self.messages_text.insert(
                tk.END,
                "=" * 70 + "\n\n"
            )

            for message in messages:
                self.messages_text.insert(
                    tk.END,
                    f"Message ID: {message['message_id']}\n"
                )

                self.messages_text.insert(
                    tk.END,
                    f"Sender: {message['sender']}\n"
                )

                self.messages_text.insert(
                    tk.END,
                    "-" * 70 + "\n"
                )

                try:
                    plaintext = decrypt_received_message(message)

                    self.messages_text.insert(
                        tk.END,
                        "RSA-PSS Signature: VERIFIED\n"
                    )

                    self.messages_text.insert(
                        tk.END,
                        "Message Status: DECRYPTED SUCCESSFULLY\n"
                    )

                    self.messages_text.insert(
                        tk.END,
                        f"Message: {plaintext}\n\n"
                    )

                except Exception as error:

                    self.messages_text.insert(
                        tk.END,
                        "RSA-PSS Signature: VERIFICATION FAILED\n"
                    )

                    self.messages_text.insert(
                        tk.END,
                        "Message Status: DECRYPTION FAILED\n"
                    )

                    self.messages_text.insert(
                        tk.END,
                        f"Reason: {type(error).__name__}\n\n"
                    )

                self.messages_text.insert(
                    tk.END,
                    "=" * 70 + "\n\n"
                )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"Could not retrieve messages.\n\n{type(error).__name__}: {error}"
            )

    def clear_messages(self):
        self.messages_text.delete("1.0", tk.END)


# ------------------------------------------------------
# START APPLICATION
# ------------------------------------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = E2EEApp(root)
    root.mainloop()
