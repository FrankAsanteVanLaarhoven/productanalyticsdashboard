# config/styles.py
CUSTOM_STYLES = """
<style>
    /* Apple-inspired Theme Variables */
    :root {
        /* Core colors matching view ratings */
        --aaa-color: #007AFF;  /* Maintain premium pricing - Apple Blue */
        --aa-color: #5856D6;   /* Consider optimization - Apple Purple */
        --a-color: #FF9500;    /* Review strategy - Apple Orange */
        --b-color: #FF3B30;    /* Evaluate position - Apple Red */
        
        /* Volume colors matching view cases */
        --high-volume: #34C759;    /* Maintain inventory - Apple Green */
        --medium-volume: #FF9F0A;  /* Monitor stock - Apple Yellow */
        --standard-volume: #64D2FF; /* Review stock - Apple Light Blue */
        
        /* Theme colors */
        --background: #F5F5F7;
        --card-bg: rgba(255, 255, 255, 0.95);
        --text: #1D1D1F;
        --shadow: rgba(0, 0, 0, 0.1);
    }

    /* Dark Mode - Apple Dark Theme */
    [data-theme="dark"] {
        --background: #000000;
        --card-bg: rgba(28, 28, 30, 0.95);
        --text: #F5F5F7;
        --shadow: rgba(255, 255, 255, 0.05);
    }

    /* Smooth Scrolling */
    html {
        scroll-behavior: smooth;
    }

    /* Base Animations */
    * {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Modern App Container */
    .stApp {
        background: var(--background);
        color: var(--text);
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Glass-morphism Cards */
    .metric-card {
        background: var(--card-bg);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px var(--shadow);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transform: translateY(0);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px var(--shadow);
    }

    /* Interactive Rating Badges - Matching view CASE logic */
    .rating-badge {
        padding: 0.6rem 1.2rem;
        border-radius: 20px;
        font-weight: 600;
        text-align: center;
        margin: 0.25rem;
        animation: badgeSlide 0.5s ease-out;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .rating-badge:hover {
        transform: scale(1.05);
        filter: brightness(1.1);
    }
    
    /* Rating Colors - Matching view cases exactly */
    .price-AAA { background: var(--aaa-color); color: white; }
    .price-AA { background: var(--aa-color); color: white; }
    .price-A { background: var(--a-color); color: white; }
    .price-B { background: var(--b-color); color: white; }

    /* Volume Badges - Matching view cases */
    .volume-high { background: var(--high-volume); color: white; }
    .volume-medium { background: var(--medium-volume); color: white; }
    .volume-standard { background: var(--standard-volume); color: white; }

    /* Modern Data Table */
    .dataframe {
        border: none !important;
        border-radius: 20px;
        overflow: hidden;
        animation: tableSlide 0.5s ease-out;
        background: var(--card-bg);
        width: 100%;
    }
    
    .dataframe thead th {
        background: var(--card-bg);
        padding: 1rem !important;
        font-weight: 600;
        position: sticky;
        top: 0;
        z-index: 10;
        border-bottom: 2px solid var(--shadow);
    }
    
    .dataframe tbody tr {
        transition: all 0.2s ease;
    }
    
    .dataframe tbody tr:hover {
        background: var(--shadow);
        transform: scale(1.01);
    }

    /* Infinite Scroll Container */
    .scroll-container {
        max-height: 80vh;
        overflow-y: auto;
        padding-right: 1rem;
        scrollbar-width: thin;
        scrollbar-color: var(--shadow) transparent;
    }

    /* Custom Scrollbar */
    .scroll-container::-webkit-scrollbar {
        width: 6px;
    }
    
    .scroll-container::-webkit-scrollbar-track {
        background: transparent;
    }
    
    .scroll-container::-webkit-scrollbar-thumb {
        background: var(--shadow);
        border-radius: 3px;
    }

    /* Advanced Animations */
    @keyframes badgeSlide {
        from { transform: translateX(-20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes tableSlide {
        from { transform: translateY(20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }

    /* Mobile Optimizations */
    @media (max-width: 768px) {
        .metric-card {
            padding: 1rem;
            margin: 0.5rem 0;
        }
        
        .rating-badge {
            padding: 0.4rem 0.8rem;
            font-size: 0.875rem;
        }
        
        .dataframe {
            font-size: 0.875rem;
        }
        
        .scroll-container {
            max-height: 60vh;
        }
    }

    /* Navigation Menu */
    .nav-menu {
        background: var(--card-bg);
        border-radius: 20px;
        padding: 0.5rem;
        margin: 1rem 0;
        display: flex;
        gap: 0.5rem;
        overflow-x: auto;
        scrollbar-width: none;
    }
    
    .nav-item {
        padding: 0.75rem 1.5rem;
        border-radius: 15px;
        cursor: pointer;
        white-space: nowrap;
        transition: all 0.3s ease;
    }
    
    .nav-item:hover, .nav-item.active {
        background: var(--aaa-color);
        color: white;
    }
</style>
"""