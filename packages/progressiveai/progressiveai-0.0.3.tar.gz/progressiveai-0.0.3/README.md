# ProgressiveAI Python Library

Welcome to the official ProgressiveAI Python Library! This library allows you to easily connect with ProgressiveAI's powerful AI Models and integrate them into your Python projects.

## Installation

You can install the library using pip:

```bash
pip install progressiveai
```

## Getting Started

```python
# Call the official ProgressiveAI Python Library
# From the "progressiveai" library, import the "Chat" class to create a connection with ProgressiveAI's AI Models
from progressiveai import Chat

# Create a chat
chat = Chat(
    # Input your ProgressiveAI API Key
    api_key="keyid-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    text="Hello, AI!",  # Enter a question of your choice
    model="wispar"  # Mention the AI Model you want to use. Currently, we offer "WISPAR Lite", and soon "WISPAR" will also be available.
)

# Get AI response
# Fetch a response from the AI Model; if not included, the request will not be submitted and processed
response = chat.get_response()
print(response)  # Print the AI's response
```

Make sure to replace `"keyid-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"` with your actual ProgressiveAI API key.

## Help and Support

If you need help or have any questions, feel free to reach out to us:

- **[ProgressiveAI Support](https://support.progressiveai.org/)**: Visit our support platform for assistance.
- **[ProgressiveAI Documentation](https://docs.progressiveai.org/)**: Check out our documentation for detailed information and guides.
- **[GitHub Repository](https://github.com/ProgressiveAI/progressiveai-python)**: Report issues or contribute to the development on GitHub.

We're here to help you make the most of ProgressiveAI's AI capabilities!
