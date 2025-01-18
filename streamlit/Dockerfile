FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY streamlit/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY product_analysis_app /app/product_analysis_app

# Environment variables for Streamlit and Database
ENV PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    # Database connection for view
    DATABASE_URL="postgresql://airflow:airflow@postgres:5432/airflow" \
    POSTGRES_SCHEMA=meap \
    POSTGRES_VIEW=vw_product_recommendations \
    # Price rating strategies from view
    PRICE_STRATEGY_AAA="Maintain premium pricing" \
    PRICE_STRATEGY_AA="Consider price optimization" \
    PRICE_STRATEGY_A="Review pricing strategy" \
    PRICE_STRATEGY_DEFAULT="Evaluate market position" \
    # Volume rating strategies from view
    VOLUME_STRATEGY_HIGH="Maintain inventory levels" \
    VOLUME_STRATEGY_MEDIUM="Monitor stock levels" \
    VOLUME_STRATEGY_DEFAULT="Review stock strategy" \
    # Streamlit theme
    STREAMLIT_THEME_BASE="light" \
    STREAMLIT_THEME_PRIMARY_COLOR="#007AFF" \
    STREAMLIT_THEME_BACKGROUND_COLOR="#FFFFFF" \
    STREAMLIT_THEME_SECONDARY_BACKGROUND_COLOR="#F0F2F6" \
    STREAMLIT_THEME_TEXT_COLOR="#1d1d1f"

# Create config directory and add custom theme
RUN mkdir -p /root/.streamlit
RUN echo '\
[theme]\n\
base="light"\n\
primaryColor="#007AFF"\n\
backgroundColor="#FFFFFF"\n\
secondaryBackgroundColor="#F0F2F6"\n\
textColor="#1d1d1f"\n\
[server]\n\
enableCORS=false\n\
enableXsrfProtection=false\n\
' > /root/.streamlit/config.toml

# Expose the Streamlit port
EXPOSE 8501

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health && \
    pg_isready -h postgres -U airflow -d airflow || exit 1

# Start Streamlit with the modular app
ENTRYPOINT ["streamlit", "run"]
CMD ["/app/product_analysis_app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]