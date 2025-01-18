#!/bin/bash

# Create base directory if it doesn't exist
mkdir -p product_analysis_app

# Navigate to project directory
cd product_analysis_app

# Create project structure
mkdir -p {components,services,utils,config,pages}

# Create Python files with proper structure
touch __init__.py
touch app.py

# Create components
cd components
touch __init__.py
touch charts.py
touch filters.py
touch metrics.py
touch recommendations.py
cd ..

# Create services
cd services
touch __init__.py
touch product_service.py
touch data_service.py
touch analytics_service.py
cd ..

# Create utils
cd utils
touch __init__.py
touch database.py
touch data_processor.py
cd ..

# Create config
cd config
touch __init__.py
touch settings.py
touch styles.py
cd ..

# Create pages
cd pages
touch __init__.py
touch home.py
touch analytics.py
touch recommendations.py
cd ..

echo "Project structure created successfully!"