# How to Run This Project Locally

This document provides detailed instructions on how to set up and run this project on your local machine.

## Prerequisites

Before you begin, ensure you have the following software installed:

*   **Python 3.x**: You can download it from [python.org](https://www.python.org/downloads/).
*   **pip**: Python's package installer. It usually comes with Python.
*   **MySQL**: A relational database management system. You can download it from [mysql.com](https://www.mysql.com/downloads/).

## Installation

Follow these steps to get your project up and running:

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage project dependencies.

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies

Install all the required Python packages using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4. Set Up the MySQL Database

1.  **Start your MySQL server.**
2.  **Create a new database for the project.** You can do this using the MySQL command-line client or a graphical tool like MySQL Workbench.

    ```sql
    CREATE DATABASE chatbot;
    ```

### 5. Configure Environment Variables

This project uses environment variables to store sensitive information like database credentials. Create a `.env` file in the root of the project and add the following variables:

```
DB_HOST=localhost
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=chatbot
```

**Note:** You can also set these variables directly in your shell, but using a `.env` file is more convenient for development. The application will use default values if these are not set.

## Training the Model

Before you can run the application, you need to train the chatbot model. Run the `training.py` script:

```bash
python training.py
```

This will create three files: `model.h5`, `texts.pkl`, and `labels.pkl`. These files are required for the chatbot to function.

## Running the Application

Once you have completed the installation and training steps, you can run the Flask application:

```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000`. You can open this URL in your web browser to interact with the chatbot.

## WhatsApp Integration (Optional)

This project also includes an optional integration with WhatsApp. To enable it, you will need to set up a WhatsApp Business Account and get the following credentials:

*   `WHATSAPP_PHONE_NUMBER_ID`
*   `WHATSAPP_ACCESS_TOKEN`
*   `YOUR_VERIFY_TOKEN`

Add these to your `.env` file:

```
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
WHATSAPP_ACCESS_TOKEN=your_access_token
YOUR_VERIFY_TOKEN=your_verify_token
```

You will also need to configure the webhook in your WhatsApp Business Account to point to the `/whatsapp` endpoint of your application. Since you are running the application locally, you will need to use a tool like [ngrok](https://ngrok.com/) to expose your local server to the internet.
