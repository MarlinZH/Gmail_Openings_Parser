# Gmail Openings Parser with Notion Integration

This project allows you to parse Gmail messages, vectorize their content, and store them in a Notion database with similarity search capabilities.

## Features

- Gmail API integration for fetching emails
- Email content vectorization using sentence-transformers
- Notion database integration for storing emails
- Similarity search between emails
- Configurable search criteria

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
Create a `.env` file with the following variables:
```
NOTION_API_KEY=your_notion_api_key
NOTION_DATABASE_ID=your_notion_database_id
```

3. Set up Gmail API:
- Follow the [Gmail API Quickstart](https://developers.google.com/gmail/api/quickstart/python) to set up OAuth 2.0 credentials
- Place your credentials file as `resi.json` in the project root

4. Set up Notion:
- Create a new database in Notion
- Get the database ID from the URL (the part after the workspace name and before the question mark)
- Create an integration in Notion and get the API key
- Share your database with the integration

## Usage

1. Run the main script:
```bash
python Gmail_Messages_by_Label.py
```

2. The script will:
- Authenticate with Gmail
- Search for emails matching the criteria
- Vectorize the email content
- Find similar emails in the Notion database
- Store the email in Notion

## Customization

- Modify the search query in `Gmail_Messages_by_Label.py` to change the email filtering criteria
- Adjust the similarity threshold in `email_vectorizer.py` to change how similar emails are identified
- Customize the Notion database schema in `notion_integration.py` to match your database structure

## Notes

-

- The vectorization uses the `all-MiniLM-L6-v2` model by default, which provides a good balance between performance and accuracy
- Similarity search is performed using cosine similarity
- Emails are stored in Notion with their vector embeddings for future similarity searches 