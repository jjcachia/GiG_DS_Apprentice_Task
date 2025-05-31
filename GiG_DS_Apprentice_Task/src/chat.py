import os
import sys

class Chat: 
    def __init__(self, user, chatbot):
        self.__user = user
        self.__chatbot = chatbot
        self.__chat_history = []

    def ask(self, question):
        self.__user.append_to_user_history(question)
        self.append_to_chat_history(self.__user.username, question)

        answer, doc_id = self.__chatbot.find_answer(question)
        self.append_to_chat_history("Chatbot V0.1", answer)
        return answer, doc_id
    
    def append_to_chat_history(self, name: str, line: str):
        self.__chat_history.append({"speaker": name, "text": line})
    
    def get_chat_history(self):
        return self.__chat_history
    
    def display_chat_history(self):
        for entry in self.__chat_history:
            print(f"{entry['speaker']}: {entry['text']}")

    def clear_chat(self):
        """Clears the chat history."""
        self.__chat_history.clear()

