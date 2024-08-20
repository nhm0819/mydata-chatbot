from sqlalchemy.orm import declarative_base

Base = declarative_base()


from mydata_chatbot.models import account, document

__all__ = ["account", "document"]
