import collections
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory

histories = collections.defaultdict(ChatMessageHistory)


def get_history(x: str):
    return histories[x]
