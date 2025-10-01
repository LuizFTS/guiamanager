from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    TOPDESK_USER = os.getenv("TOPDESK_USER")
    TOPDESK_PASSWORD = os.getenv("TOPDESK_PASSWORD")
    TOPDESK_PHONE = os.getenv("TOPDESK_PHONE")