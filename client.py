import requests
import time


SERVER_URL = "http://127.0.0.1:5001"


def send_message() -> None:
    message = input("Enter your message: ")
    response = requests.post(f'{SERVER_URL}/messages', json={'message': message})

    if response.status_code == 201:
        print("Message sent successfully.")
    else:
        print("Failed to send message.")


def display_messages() -> None:
    response = requests.get(f'{SERVER_URL}/messages')

    if response.status_code == 200:
        messages = response.json()

        if messages:
            print("\nChat Messages:")

            for msg in messages:
                print(f"[{msg['timestamp']}] {msg['text']}")
        else:
            print("No messages yet.")
    else:
        print("Failed to retrieve messages.")


def get_message_count() -> None:
    response = requests.get(f'{SERVER_URL}/messages/count')

    if response.status_code == 200:
        count = response.json().get('message_count', 0)
        print(f"Total number of messages: {count}")
    else:
        print("Failed to retrieve message count.")


def measure_response_time() -> None:
    start_time = time.time()
    requests.get(f'{SERVER_URL}/messages/count')
    end_time = time.time()
    response_time = (end_time - start_time) * 1000  # convert to milliseconds
    print(f"Response time is {response_time:.2f} ms")
    return response_time


def main() -> None:

    while True:
        print("\n1. Send a message")
        print("2. Display all messages")
        print("3. Get message count")
        print("4. Measure response time")
        print("5. Exit\n")

        choice = input("Choose an option: ")

        if choice == '1':
            send_message()
        elif choice == '2':
            display_messages()
        elif choice == '3':
            get_message_count()
        elif choice == '4':
            measure_response_time()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
