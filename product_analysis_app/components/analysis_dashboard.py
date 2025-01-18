# components/analysis_dashboard.py
class AnalysisDashboard:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.service = ProductAnalysisService()

    def render_filters(self):
        with st.sidebar:
            st.markdown("### Filters")
            price_filter = st.multiselect(
                "Price Rating",
                options=['AAA', 'AA', 'A', 'B'],
                default=['AAA', 'AA', 'A', 'B']
            )
            volume_filter = st.multiselect(
                "Volume Rating",
                options=['High Volume', 'Medium Volume', 'Standard Volume'],
                default=['High Volume', 'Medium Volume', 'Standard Volume']
            )
            return price_filter, volume_filter

    def render_metrics(self, product_data: ProductRecommendation):
        metrics_col1, metrics_col2 = st.columns(2)
        
        with metrics_col1:
            st.markdown(
                self._get_price_metric_html(product_data),
                unsafe_allow_html=True
            )
        
        with metrics_col2:
            st.markdown(
                self._get_volume_metric_html(product_data),
                unsafe_allow_html=True
            )

    def _get_price_metric_html(self, data: ProductRecommendation) -> str:
        return f"""
            <div class='metric-card'>
                <h3>Price Analysis</h3>
                <div class='metric-header'>
                    <h2>${data.avg_price:,.2f}</h2>
                    {self._get_rating_badge(data.price_rating)}
                </div>
                <div class='strategy-box'>
                    <p class="strategy-text">💡 {data.price_strategy}</p>
                </div>
            </div>
        """
