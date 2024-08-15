from sqlalchemy.orm import declarative_base
Base = declarative_base()


from rag_backend.models import account, document
__all__ = ["account", "document"]
