## Testing QuickNews
**This file provides instructions for running the unit tests for the QuickNews application.**

## Directory Structure
```
quicknews/
│
├── tests/
│   ├── __init__.py
│   ├── test_news_service.py
│   ├── test_ai_service.py
│   ├── test_article.py
│   ├── test_spinner.py
│   ├── test_main.py
│   └── run_tests.py
│
├── (the rest of the files)
```

## Required Packages
Install testing dependencies:
```bash
# Install required packages
pip install -r requirements.txt
```

## Running the Tests
```bash
# Run the tests
cd quicknews
pytest tests/
```
