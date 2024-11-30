import os
from slack_sdk import WebClient
from dotenv import load_dotenv
import tweepy

# Load environment variables
load_dotenv()

# Slack setup
slack_token = os.getenv("SLACK_BOT_TOKEN_SOCIAL")
slack_channel_id = os.getenv("SLACK_CHANNEL_ID_SOCIAL")
slack_client = WebClient(token=slack_token)

# X setup
x_api_key = os.getenv("X_API_KEY")
x_api_secret = os.getenv("X_API_SECRET")
x_access_token = os.getenv("X_ACCESS_TOKEN")
x_access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")

class XBot:
    def __init__(self, api_key: str, api_secret: str, access_token: str, access_token_secret: str):
        """Initialize X bot with credentials"""
        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)
        
    def post_tweet(self, content: str) -> str:
        """
        Post a tweet
        
        Args:
            content (str): The content of the tweet
            
        Returns:
            str: Status message about the tweet
        """
        try:
            tweet = self.api.update_status(content)
            return f"Successfully posted tweet with ID: {tweet.id}"
        except tweepy.errors.TweepyException as e:
            return f"Error posting tweet: {str(e)}"

def fetch_latest_slack_message() -> str:
    """Fetch the latest message from the Slack channel."""
    try:
        response = slack_client.conversations_history(channel=slack_channel_id, limit=1)
        if response["ok"] and "messages" in response and response["messages"]:
            message = response["messages"][0]["text"]
            print(f"Latest message from Slack: {message}")
            return message
        else:
            raise Exception("Failed to fetch messages from Slack")
    except Exception as e:
        print(f"Error fetching Slack message: {e}")
        return None

def main():
    """Main function to fetch Slack message and post to X."""
    # Initialize X bot
    x_bot = XBot(
        api_key=x_api_key,
        api_secret=x_api_secret,
        access_token=x_access_token,
        access_token_secret=x_access_token_secret
    )
    
    # Fetch latest Slack message
    latest_message = fetch_latest_slack_message()
    if latest_message:
        # Post the message to X
        result = x_bot.post_tweet(latest_message)
        print(result)

if __name__ == "__main__":
    main()
