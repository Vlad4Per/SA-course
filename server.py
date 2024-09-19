from flask import Flask, request, jsonify
from datetime import datetime
import os
import signal
import sys

app = Flask(__name__)

# Storage for messages
messages = []
messages_file = './messages/chat_messages.txt'


def save_messages_to_file() -> None:
    global messages

    # Ensure the messages directory exists
    os.makedirs('./messages', exist_ok=True)

    with open(messages_file, 'a') as file:
        for msg in messages:
            file.write(f"{msg['timestamp']} - {msg['text']}\n")

    messages.clear()


def load_messages_from_file() -> None:
    global messages
    if os.path.exists(messages_file):
        with open(messages_file, 'r') as f:
            for line in f:
                timestamp, text = line.strip().split(' - ', 1)
                messages.append({'timestamp': timestamp, 'text': text})


# Signal handler for saving messages on exit
def signal_handler(sig, frame) -> None:
    print("\nSaving messages to file...")
    save_messages_to_file()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


@app.route('/messages', methods=['GET', 'POST'])
def message_handler():
    global messages

    if request.method == 'POST':
        # Extract message from request body
        data = request.get_json()
        message_text = data.get('message', '')
        # Create a new message with the current date and time
        new_message = {
            'text': message_text,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        # Store the message in memory
        messages.append(new_message)

        # Save messages to file every 10 messages
        if len(messages) >= 10:
            save_messages_to_file()
            messages.clear()  # Clear the buffer

        return jsonify({'status': 'Message received'}), 201

    elif request.method == 'GET':
        # Return all messages, including those from the file
        save_messages_to_file()
        messages.clear()
        all_messages = []
        if os.path.exists(messages_file):
            with open(messages_file, 'r') as file:
                for line in file:
                    timestamp, text = line.strip().split(' - ', 1)
                    all_messages.append({'timestamp': timestamp, 'text': text})

        return jsonify(all_messages), 200
    else:
        return jsonify(""), 400


@app.route('/messages/count', methods=['GET'])
def message_count():
    try:
        return jsonify({'message_count': len(messages) + sum(1 for _ in open(messages_file))}), 200
    except FileNotFoundError:
        return jsonify({'message_count': len(messages)}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
