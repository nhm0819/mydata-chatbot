from langchain.callbacks.streaming_aiter import AsyncIteratorCallbackHandler
from mydata_chatbot.schemas.chat import ChatResponse

# class AsyncCallbackHandler(AsyncIteratorCallbackHandler):
#     content: str = ""
#     final_answer: bool = False
#
#     def __init__(self) -> None:
#         super().__init__()
#
#     async def on_llm_new_token(self, token: str, **kwargs) -> None:
#         self.content += token
#         # if we passed the final answer, we put tokens in queue
#         if self.final_answer:
#             self.queue.put_nowait(token)
#         elif ";" in self.content:
#             self.final_answer = True
#             self.content = ""
#
#     async def on_llm_end(self, response, **kwargs) -> None:
#         if self.final_answer:
#             self.content = ""
#             self.final_answer = False
#             self.done.set()
#         else:
#             self.content = ""




class StreamingLLMCallbackHandler(AsyncIteratorCallbackHandler):
    """Callback handler for streaming LLM responses."""

    async def on_llm_start(self, serialized, prompts, **kwargs) -> None:
        self.done.clear()
        self.queue.put_nowait(ChatResponse(sender="bot", message="", type="start"))

    async def on_llm_end(self, response, **kwargs) -> None:
        # we override this method since we want the ConversationalRetrievalChain to potentially return
        # other items (e.g., source_documents) after it is completed
        pass

    async def on_llm_error(self, error: Exception | KeyboardInterrupt, **kwargs) -> None:
        self.queue.put_nowait(ChatResponse(sender="bot", message=str(error), type="error"))

    async def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.queue.put_nowait(ChatResponse(sender="bot", message=token, type="stream"))
