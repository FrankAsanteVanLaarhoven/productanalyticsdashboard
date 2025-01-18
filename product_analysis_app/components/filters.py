import streamlit as st
from typing import Tuple, List

class FilterComponent:
    @staticmethod
    def render_filters(df) -> Tuple[List[str], List[str]]:
        """Render sidebar filters matching view ratings"""
        with st.sidebar:
            st.markdown("### Filters")
            
            price_filter = st.multiselect(
                "Price Rating",
                options=['AAA', 'AA', 'A', 'B'],
                default=['AAA', 'AA', 'A', 'B'],
                help="Filter by price rating"
            )
            
            volume_filter = st.multiselect(
                "Volume Rating",
                options=['High Volume', 'Medium Volume', 'Standard Volume'],
                default=['High Volume', 'Medium Volume', 'Standard Volume'],
                help="Filter by volume rating"
            )
            
            return price_filter, volume_filter