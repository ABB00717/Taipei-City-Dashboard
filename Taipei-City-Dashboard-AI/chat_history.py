from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

conversation = {}

def getSessionConversation(session_id: str) -> BaseChatMessageHistory:
    if session_id not in conversation:
        conversation[session_id] = ChatMessageHistory()
    return conversation[session_id]

def format_chat_history(chat_history):
    formatted_history = []
    for message in chat_history.messages:  # 修改这里
        if isinstance(message, tuple):  # 处理 tuple 类型
            role, content = message
        else:
            role, content = message.type, message.content
        
        if role == "human":
            formatted_history.append(f"Human: {content}")
        elif role == "ai":
            formatted_history.append(f"AI: {content}")
    return "\n".join(formatted_history)