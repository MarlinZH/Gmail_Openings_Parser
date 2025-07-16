from notion_client import Client
import os
from typing import Dict, List, Optional
from datetime import datetime
import 

class NotionDatabase:
    def __init__(self, api_key: str, database_id: str):
        """
        Initialize Notion database connection
        Args:
            api_key: Notion API key
            database_id: ID of the Notion database to connect to
        """
        self.notion = Client(auth=api_key)
        self.database_id = database_id

    def create_page(self, email_data: Dict) -> Dict:
        """
        Create a new page in the Notion database
        Args:
            email_data: Dictionary containing email information
        Returns:
            Created page data
        """
        properties = {
            "Subject": {
                "title": [
                    {
                        "text": {
                            "content": email_data.get("subject", "")
                        }
                    }
                ]
            },
            "From": {
                "rich_text": [
                    {
                        "text": {
                            "content": email_data.get("from", "")
                        }
                    }
                ]
            },
            "Date": {
                "date": {
                    "start": email_data.get("date", datetime.now().isoformat())
                }
            },
            "Content": {
                "rich_text": [
                    {
                        "text": {
                            "content": email_data.get("content", "")
                        }
                    }
                ]
            },
            "Vector": {
                "rich_text": [
                    {
                        "text": {
                            "content": str(email_data.get("vector", []))
                        }
                    }
                ]
            }
        }
        
        return self.notion.pages.create(
            parent={"database_id": self.database_id},
            properties=properties
        )

    def get_pages(self, filter_criteria: Optional[Dict] = None) -> List[Dict]:
        """
        Get pages from the Notion database
        Args:
            filter_criteria: Optional filter criteria
        Returns:
            List of pages
        """
        response = self.notion.databases.query(
            database_id=self.database_id,
            filter=filter_criteria
        )
        return response.get("results", [])

    def update_page(self, page_id: str, properties: Dict) -> Dict:
        """
        Update an existing page
        Args:
            page_id: ID of the page to update
            properties: Properties to update
        Returns:
            Updated page data
        """
        return self.notion.pages.update(
            page_id=page_id,
            properties=properties
        )

    def delete_page(self, page_id: str) -> Dict:
        """
        Delete a page from the database
        Args:
            page_id: ID of the page to delete
        Returns:
            Response from Notion API
        """
        return self.notion.pages.update(
            page_id=page_id,
            archived=True
        ) 