# modern_style.py - Light theme matching demo UI

modern_style = """
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Hide Streamlit branding */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    /* Main container - Light background */
    .main {
        background: #ffffff;
        color: #1f2937;
    }
    
    div.block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Headers */
    h1 {
        color: #5b8fc9 !important;
        font-weight: 700 !important;
        font-size: 2.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    h2 {
        color: #1f2937 !important;
        font-weight: 600 !important;
        font-size: 1.5rem !important;
        margin-top: 2rem !important;
    }
    
    h3 {
        color: #374151 !important;
        font-weight: 600 !important;
        font-size: 1.3rem !important;
    }
    
    /* Subtitle text */
    .main h3 em {
        color: #6b7280 !important;
        font-weight: 400 !important;
        font-style: italic;
    }
    
    /* Dividers */
    hr {
        border-color: #e5e7eb !important;
        margin: 2rem 0 !important;
    }
    
    /* Caption text */
    .stCaption {
        color: #9ca3af !important;
    }
    
    /* Buttons - Dark slate blue matching demo */
    .stButton>button {
        width: 100%;
        padding: 0.875rem 1.5rem;
        border-radius: 8px;
        border: none;
        background: #3d5470;
        color: white !important;
        font-weight: 600;
        font-size: 0.95rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        cursor: pointer;
    }
    
    .stButton>button:hover {
        background: #2d4057;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
    
    .stButton>button:active {
        transform: translateY(0);
    }
    
    /* Primary button variant */
    .stButton>button[kind="primary"] {
        background: #3d5470;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .stButton>button[kind="primary"]:hover {
        background: #2d4057;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
    
    /* Info boxes - Clean card style */
    .stInfo {
        background: #f0f4f8;
        border: 1px solid #d1dce6;
        border-left: 4px solid #5b8fc9;
        padding: 1rem;
        border-radius: 8px;
        color: #1f2937 !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    
    .stInfo p {
        color: #1f2937 !important;
    }
    
    /* Success boxes */
    .stSuccess {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 8px;
        color: #155724 !important;
        box-shadow: 0 1px 3px rgba(40, 167, 69, 0.1);
    }
    
    .stSuccess p {
        color: #155724 !important;
    }
    
    /* Warning boxes */
    .stWarning {
        background: #fff3cd;
        border: 1px solid #ffeeba;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 8px;
        color: #856404 !important;
        box-shadow: 0 1px 3px rgba(255, 193, 7, 0.1);
    }
    
    .stWarning p {
        color: #856404 !important;
    }
    
    /* Error boxes */
    .stError {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        border-left: 4px solid #dc3545;
        padding: 1rem;
        border-radius: 8px;
        color: #721c24 !important;
        box-shadow: 0 1px 3px rgba(220, 53, 69, 0.1);
    }
    
    .stError p {
        color: #721c24 !important;
    }
    
    /* File uploader - Matching demo style */
    .stFileUploader {
        background: #2d3e50;
        border: 2px dashed #4a5f7f;
        border-radius: 12px;
        padding: 2.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    .stFileUploader:hover {
        border-color: #5b8fc9;
        background: #34495e;
    }
    
    .stFileUploader label {
        color: #ffffff !important;
        font-weight: 500;
    }
    
    .stFileUploader section > div {
        color: #b0bec5 !important;
    }
    
    /* Text inputs */
    .stTextInput>div>div>input {
        background-color: #2d3e50;
        border: 1px solid #4a5f7f;
        border-radius: 8px;
        padding: 0.875rem 1rem;
        font-size: 0.95rem;
        color: #ffffff;
        transition: all 0.3s ease;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #5b8fc9;
        background-color: #34495e;
        box-shadow: 0 0 0 3px rgba(91, 143, 201, 0.2);
        outline: none;
    }
    
    .stTextInput>div>div>input::placeholder {
        color: #8b95a0;
    }
    
    .stTextInput label {
        color: #1f2937 !important;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    
    /* Text area */
    .stTextArea>div>div>textarea {
        background-color: #2d3e50;
        border: 1px solid #4a5f7f;
        border-radius: 8px;
        padding: 0.875rem 1rem;
        font-size: 0.95rem;
        color: #ffffff;
        transition: all 0.3s ease;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    .stTextArea>div>div>textarea:focus {
        border-color: #5b8fc9;
        background-color: #34495e;
        box-shadow: 0 0 0 3px rgba(91, 143, 201, 0.2);
        outline: none;
    }
    
    .stTextArea label {
        color: #1f2937 !important;
        font-weight: 500;
    }
    
    /* Number input */
    .stNumberInput>div>div>input {
        background-color: #2d3e50;
        border: 1px solid #4a5f7f;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        color: #ffffff;
    }
    
    .stNumberInput label {
        color: #1f2937 !important;
        font-weight: 500;
    }
    
    /* Select box */
    .stSelectbox>div>div>div {
        background-color: #2d3e50;
        border: 1px solid #4a5f7f;
        border-radius: 8px;
        color: #ffffff;
    }
    
    .stSelectbox label {
        color: #1f2937 !important;
        font-weight: 500;
    }
    
    /* Multiselect */
    .stMultiSelect>div>div>div {
        background-color: #2d3e50;
        border: 1px solid #4a5f7f;
        border-radius: 8px;
    }
    
    .stMultiSelect label {
        color: #1f2937 !important;
        font-weight: 500;
    }
    
    /* Slider */
    .stSlider label {
        color: #1f2937 !important;
        font-weight: 500;
    }
    
    .stSlider>div>div>div>div {
        background-color: #5b8fc9;
    }
    
    /* Tabs - Clean rounded tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        padding: 0.5rem 0;
        border-bottom: 2px solid #e5e7eb;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 0.875rem 1.5rem;
        font-weight: 600;
        color: #6b7280;
        background-color: transparent;
        transition: all 0.3s ease;
        border: none;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #f3f4f6;
        color: #374151;
    }
    
    .stTabs [aria-selected="true"] {
        background: #3d5470;
        color: white !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Result boxes - Clean cards */
    .result-box {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        line-height: 1.7;
        color: #1f2937;
        font-size: 1rem;
        border: 1px solid #e5e7eb;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .result-box:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
        transform: translateY(-2px);
    }
    
    .answer-box {
        background: #f0f4f8;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #5b8fc9;
        line-height: 1.7;
        color: #1f2937;
        font-size: 1rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        margin: 1rem 0;
    }
    
    .comparison-box {
        background: #e8f5e9;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #4caf50;
        line-height: 1.7;
        color: #1b5e20;
        font-size: 1rem;
        box-shadow: 0 2px 8px rgba(76, 175, 80, 0.15);
        margin: 1rem 0;
    }
    
    .rag-box {
        background: #fff8e1;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #ff9800;
        line-height: 1.7;
        color: #e65100;
        font-size: 1rem;
        box-shadow: 0 2px 8px rgba(255, 152, 0, 0.15);
        margin: 1rem 0;
    }
    
    /* Expander - Clean accordion */
    .streamlit-expanderHeader {
        background: #ffffff;
        border-radius: 8px;
        font-weight: 600;
        color: #374151 !important;
        border: 1px solid #e5e7eb;
        transition: all 0.3s ease;
        padding: 0.875rem;
    }
    
    .streamlit-expanderHeader:hover {
        background: #f9fafb;
        border-color: #5b8fc9;
    }
    
    .streamlit-expanderContent {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-top: none;
        border-radius: 0 0 8px 8px;
        padding: 1rem;
    }
    
    /* Chat messages */
    .stChatMessage {
        background: #ffffff;
        border-radius: 12px;
        padding: 1.25rem;
        margin: 0.75rem 0;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
    }
    
    .stChatMessage[data-testid="user-message"] {
        background: #f0f4f8;
        border-left: 3px solid #5b8fc9;
    }
    
    .stChatMessage[data-testid="assistant-message"] {
        background: #ffffff;
        border-left: 3px solid #4caf50;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: #5b8fc9;
    }
    
    /* Download button */
    .stDownloadButton>button {
        background: #4caf50;
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        box-shadow: 0 2px 4px rgba(76, 175, 80, 0.2);
        transition: all 0.3s ease;
    }
    
    .stDownloadButton>button:hover {
        background: #45a049;
        box-shadow: 0 4px 8px rgba(76, 175, 80, 0.3);
        transform: translateY(-1px);
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: #5b8fc9 transparent transparent transparent;
    }
    
    /* Code blocks */
    code {
        background-color: #f6f8fa !important;
        color: #24292e !important;
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        font-family: 'Fira Code', monospace;
        border: 1px solid #e1e4e8;
    }
    
    pre {
        background-color: #f6f8fa !important;
        border: 1px solid #e1e4e8;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Columns */
    .row-widget.stHorizontal {
        gap: 1rem;
    }
    
    /* Markdown */
    .main p {
        color: #4b5563;
        line-height: 1.7;
    }
    
    .main a {
        color: #5b8fc9;
        text-decoration: none;
        transition: color 0.3s ease;
    }
    
    .main a:hover {
        color: #3d5470;
        text-decoration: underline;
    }
    
    /* Lists */
    .main ul, .main ol {
        color: #4b5563;
    }
    
    /* Metric */
    .stMetric {
        background: #ffffff;
        padding: 1.25rem;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
    }
    
    .stMetric label {
        color: #6b7280 !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #5b8fc9 !important;
        font-weight: 700;
    }
    
    /* Dataframe */
    .stDataFrame {
        background-color: #ffffff;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
    }
    
    /* Radio buttons */
    .stRadio label {
        color: #374151 !important;
    }
    
    /* Checkbox */
    .stCheckbox label {
        color: #374151 !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f3f5;
        border-radius: 8px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #5b8fc9;
        border-radius: 8px;
        border: 2px solid #f1f3f5;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #3d5470;
    }
    </style>
"""