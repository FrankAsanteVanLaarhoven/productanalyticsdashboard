# /Users/frankvanlaarhoven/airflow_project/product_analysis_app/pages/chat.py
import streamlit as st
from services.product_service import ProductService

def show():
    st.title("Product Analysis Chat")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about product analysis..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Get data from view for context
        df = ProductService.get_recommendations()
        
        # Generate response based on view data
        response = f"Based on our product analysis:\n\n"
        if df is not None:
            response += f"- We have {len(df)} products under analysis\n"
            response += f"- Price ratings range from {df['price_rating'].min()} to {df['price_rating'].max()}\n"
            response += f"- Volume ratings include {', '.join(df['volume_rating'].unique())}\n"
        
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    show()