# pages/chat.py
import streamlit as st
from services.product_service import ProductService

def show():
    st.title("Product Analysis Chat")
    
    service = ProductService()
    df = service.get_recommendations()
    
    if not df.empty:
        st.markdown("""
            ### Ask questions about your product data
            
            Examples:
            - How many premium (AAA) products do we have?
            - What's the distribution of volume ratings?
            - Show me products that need price optimization
        """)
        
        user_question = st.text_input("Your question:")
        if user_question:
            # Add your chat logic here
            st.info("Chat functionality coming soon!")
    else:
        st.warning("Please load data first using the main dashboard")

if __name__ == "__main__":
    show()
