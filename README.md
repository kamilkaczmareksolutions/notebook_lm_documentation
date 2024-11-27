# NotebookLM Documentation Scraper

This project provides a web scraper that automatically extracts and formats the complete documentation from Google's NotebookLM Help Center. The scraper generates a comprehensive Markdown file containing all documentation sections, making it easy to read and reference offline.

## What it does

The script performs the following operations:
- Navigates through the NotebookLM Help Center
- Expands all collapsible sections
- Extracts content from each documentation page
- Formats the content into a clean Markdown structure
- Saves everything to a single `notebook_lm_documentation.md` file

## Requirements

```python
selenium
beautifulsoup4
chrome/chromium browser
```

## How to use

1. Clone this repository
2. Install the required dependencies:
```bash
pip install selenium beautifulsoup4
```
3. Run the script:
```bash
python app.py
```

## Technical Details

The scraper uses:
- **Selenium** for browser automation and handling dynamic content
- **BeautifulSoup** for parsing HTML and extracting text content
- **Headless Chrome** mode for efficient scraping
- Automatic handling of expandable sections and nested lists
- Smart content formatting with proper Markdown hierarchy

## Output

The script generates a `notebook_lm_documentation.md` file that includes:
- Complete NotebookLM documentation
- Properly formatted headers (H1-H3)
- Nested lists and paragraphs
- All sections from the Help Center organized hierarchically

## Note

This is an unofficial tool for educational purposes. The generated documentation is sourced from Google's public Help Center for NotebookLM.

Citations:
[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/2507178/0a322800-ecb9-49fa-ad41-51b0e5e63109/notebook_lm_documentation.md
[2] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/2507178/3041650f-45e9-4769-871d-367e3fd88195/app.py