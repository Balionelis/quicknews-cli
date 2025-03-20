# QuickNews

A lightweight CLI tool that fetches, filters, and displays personalized news using AI curation. Combines Google News RSS feeds and Gemini AI to deliver your top 5 relevant news articles in seconds.

![License](https://img.shields.io/github/license/Balionelis/quicknews)
![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)

## Features

- 🔍 Search for news on any topic
- 🤖 AI-powered article curation using Google's Gemini
- ⚡ Fast, responsive CLI interface
- 💾 Automatic JSON export of results
- 🔄 Simple, modular codebase

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/quicknews.git
cd quicknews

# Install dependencies
pip install -r requirements.txt
```

## Usage
```bash
# Run the program
python main.py
```
When prompted, enter any topic you're interested in (e.g., "climate change", "artificial intelligence", "space exploration").

## Project Structure
```
quicknews/
│
├── config/
│   ├── __init__.py
│   └── settings.py       # API keys and configuration
│
├── utils/
│   ├── __init__.py
│   └── spinner.py        # Loading animation functionality
│
├── services/
│   ├── __init__.py
│   ├── news_service.py   # Google News RSS integration
│   └── ai_service.py     # Gemini AI integration
│
├── models/
│   ├── __init__.py
│   └── article.py        # Data structures for articles
│
├── main.py               # Main script to run the application
└── requirements.txt      # Dependencies
```

## Configuration
Before using QuickNews, you need to obtain an API key for:

1. **[Google Generative AI (Gemini)](https://ai.google.dev/)** - Free tier available

QuickNews uses environment variables to securely manage API keys:

1. Create a `.env` file in the project root directory:
    ```bash
    GEMINI_API_KEY=your_actual_gemini_api_key_here
    ```
2. This file is automatically excluded from Git via `.gitignore` to prevent accidentally exposing your API keys.

3. The application will automatically load these environment variables when running.

For developers and contributors, an `.env.example` file is provided with placeholders:
```
GEMINI_API_KEY=your_gemini_api_key_here
```
This approach keeps your API keys secure while making the setup process clear for other users.


## How It Works
1. User inputs a topic of interest
2. The app fetches recent news articles about that topic from **Google News RSS feeds**
3. Titles are sent to **Google's Gemini AI** to select the most relevant/interesting articles
4. The **TOP 5** articles are displayed in the terminal and saved to a **JSON** file

## Testing
If you want to run tests you can view this **[FILE](https://github.com/Balionelis/quicknews/blob/main/TESTING.md)** for instructions

## License

This project is licensed under the **MIT License** - see the **[LICENSE](https://github.com/Balionelis/quicknews/blob/main/LICENSE)** file for details.