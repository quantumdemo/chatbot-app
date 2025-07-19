# User Guide: WhatsApp Chatbot

## Introduction

This guide provides instructions on how to manage and deploy your WhatsApp chatbot. The chatbot is designed to be easy to update and maintain, even for users with limited technical knowledge.

## How to Add/Update Questions and Answers

The chatbot's knowledge base is stored in the `data.json` file. This file contains a list of "intents," where each intent represents a specific topic or question that the chatbot can understand.

To add new questions and answers or update existing ones, you need to modify the `data.json` file. Here's the structure of an intent:

```json
{
  "tag": "your_intent_tag",
  "patterns": [
    "A question a user might ask",
    "Another way a user might ask the same question"
  ],
  "responses": [
    "A possible response from the chatbot",
    "Another possible response"
  ]
}
```

- `tag`: A unique identifier for the intent.
- `patterns`: A list of sample user messages that should trigger this intent. The more patterns you provide, the better the chatbot will be at understanding user requests.
- `responses`: A list of possible responses that the chatbot can send back to the user. The chatbot will choose a random response from this list.

### Example

To add a new intent for questions about your business hours, you could add the following to the `intents` list in `data.json`:

```json
{
  "tag": "business_hours",
  "patterns": [
    "What are your business hours?",
    "When are you open?",
    "What are your opening times?"
  ],
  "responses": [
    "We are open from 9 AM to 5 PM, Monday to Friday.",
    "Our business hours are 9 AM to 5 PM, Monday to Friday."
  ]
}
```

### Retraining the Model

After you have modified the `data.json` file, you need to retrain the chatbot's model so that it can learn the new intents. To do this, run the following command in your terminal:

```bash
python training.py
```

This will update the `model.h5` file with the new knowledge. You don't need to restart the application after retraining the model.

## Deployment

This guide provides instructions for deploying the chatbot to Heroku.

### Prerequisites

- A Heroku account
- The Heroku CLI installed on your computer
- A MySQL database (you can use Heroku's ClearDB add-on)

### Deployment Steps

1. **Create a Heroku App:**
   ```bash
   heroku create your-app-name
   ```

2. **Add a Procfile:**
   Create a file named `Procfile` in the root of your project with the following content:
   ```
   web: gunicorn app:app
   ```

3. **Install Gunicorn:**
   ```bash
   pip install gunicorn
   ```

4. **Push to Heroku:**
   ```bash
   git add .
   git commit -m "Add Procfile and gunicorn"
   git push heroku master
   ```

### Setting Environment Variables

You need to set the following environment variables on Heroku for the chatbot to work correctly:

- `DB_HOST`: The hostname of your MySQL database.
- `DB_USER`: The username for your MySQL database.
- `DB_PASSWORD`: The password for your MySQL database.
- `DB_NAME`: The name of your MySQL database.
- `WHATSAPP_ACCESS_TOKEN`: Your WhatsApp Business API access token.
- `WHATSAPP_PHONE_NUMBER_ID`: The phone number ID of your WhatsApp Business account.
- `VERIFY_TOKEN`: The verify token you set up in the WhatsApp Developer Console.

You can set these variables in the Heroku dashboard under your app's "Settings" tab in the "Config Vars" section.

## Integration with WhatsApp

To connect your chatbot to a WhatsApp number, you need to use the WhatsApp Cloud API. Here's a summary of the steps involved:

1. **Set up a Meta Developer Account:** If you don't have one already, create a Meta Developer account and a new app.

2. **Configure the WhatsApp Product:** In your app's dashboard, add the "WhatsApp" product and configure it.

3. **Get Your Credentials:** You'll need the following credentials from the WhatsApp Developer Console:
   - **Access Token:** A temporary or permanent access token.
   - **Phone Number ID:** The ID of the phone number you want to use for the chatbot.

4. **Set up a Webhook:** In the WhatsApp Developer Console, you need to set up a webhook that points to your deployed chatbot's `/whatsapp` endpoint. The URL will be something like `https://your-app-name.herokuapp.com/whatsapp`.

5. **Verify Your Webhook:** When you set up the webhook, WhatsApp will send a verification request to your application. You need to have the `VERIFY_TOKEN` environment variable set to the same value you enter in the WhatsApp Developer Console.

6. **Subscribe to Message Events:** In the WhatsApp Developer Console, subscribe to the "messages" event to receive incoming messages from users.

For more detailed instructions, please refer to the official Meta for Developers documentation.
