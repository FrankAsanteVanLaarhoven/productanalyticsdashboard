import streamlit as st
from langchain import OpenAI, ConversationChain

class ProductAnalystBot:
    def __init__(self):
        self.llm = OpenAI(temperature=0)
        self.conversation = ConversationChain(llm=self.llm)
    
    def get_response(self, user_input):
        return self.conversation.predict(input=user_input)