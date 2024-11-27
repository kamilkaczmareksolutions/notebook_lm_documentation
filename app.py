from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from bs4 import BeautifulSoup
import time

def get_article_content(driver, url):
    try:
        driver.get(url)
        time.sleep(2)
        
        # Czekamy na załadowanie artykułu
        article = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "article"))
        )
        
        # Znajdujemy wszystkie rozwijane sekcje w artykule
        expandable_sections = article.find_elements(By.CSS_SELECTOR, "h3[role='button']")
        for section in expandable_sections:
            if section.get_attribute('aria-expanded') == 'false':
                driver.execute_script("arguments[0].scrollIntoView(true);", section)
                driver.execute_script("arguments[0].click();", section)
                time.sleep(1)
        
        # Pobieramy zaktualizowaną zawartość artykułu
        article = driver.find_element(By.TAG_NAME, "article")
        return process_content(BeautifulSoup(article.get_attribute('innerHTML'), 'html.parser'))
    except Exception as e:
        print(f"Error getting content from {url}: {str(e)}")
        return ""

def process_content(soup):
    content = []
    list_level = 0  # śledzimy poziom zagnieżdżenia list
    
    for element in soup.find_all(['h1', 'h2', 'h3', 'p', 'ul', 'li']):
        text = ' '.join(element.get_text().split())
        
        if not text or any(svg in text.lower() for svg in ['viewbox', 'path d=']):
            continue
            
        if element.name == 'h1':
            content.append(f"# {text}\n")
        elif element.name == 'h2':
            content.append(f"## {text}\n")
        elif element.name == 'h3':
            content.append(f"### {text}\n")
        elif element.name == 'p':
            if text:  # pomijamy puste paragrafy
                content.append(f"{text}\n\n")
        elif element.name == 'ul':
            list_level += 1
        elif element.name == 'li':
            # Sprawdzamy, czy element li nie zawiera zagnieżdżonej listy
            if not element.find('ul'):
                indent = "  " * (list_level - 1)
                content.append(f"{indent}* {text}\n")
        
        # Jeśli kończymy listę, zmniejszamy poziom zagnieżdżenia
        if element.name == 'ul' and element.find_next_sibling() and element.find_next_sibling().name != 'ul':
            list_level -= 1
    
    return ''.join(content)

def get_documentation():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)
    content = "# Google NotebookLM Documentation\n\n"
    
    try:
        # Otwieramy główną stronę
        print("Opening main page...")
        driver.get("https://support.google.com/notebooklm/?hl=en#topic=14287611")
        time.sleep(3)
        
        # Znajdujemy wszystkie główne sekcje
        main_sections = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "section.parent h3[role='button']"))
        )
        print(f"Found {len(main_sections)} main sections")
        
        # Zbieramy wszystkie URLe przed przetwarzaniem
        all_urls = []
        
        for section in main_sections:
            try:
                section_name = section.text
                print(f"\nCollecting URLs from section: {section_name}")
                
                # Rozwijamy sekcję jeśli nie jest rozwinięta
                if section.get_attribute('aria-expanded') == 'false':
                    driver.execute_script("arguments[0].scrollIntoView(true);", section)
                    driver.execute_script("arguments[0].click();", section)
                    time.sleep(1)
                
                # Znajdujemy wszystkie linki w rozwiniętej sekcji
                section_element = section.find_element(By.XPATH, "./..")
                links = section_element.find_elements(By.CSS_SELECTOR, "a.article-link")
                
                # Zapisujemy URLe
                section_urls = [(link.text, link.get_attribute('href')) for link in links]
                all_urls.append((section_name, section_urls))
                print(f"Found {len(section_urls)} subsections")
                
            except Exception as e:
                print(f"Error collecting URLs from section {section_name}: {str(e)}")
                continue
        
        # Przetwarzamy zebrane URLe
        for section_name, section_urls in all_urls:
            print(f"\nProcessing section: {section_name}")
            content += f"## {section_name}\n\n"
            
            for title, url in section_urls:
                print(f"Processing subsection: {title}")
                article_content = get_article_content(driver, url)
                if article_content:
                    content += f"### {title}\n{article_content}\n"
                
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        print(f"Full traceback:\n{traceback.format_exc()}")
    finally:
        driver.quit()
    
    return content

if __name__ == "__main__":
    print("Starting documentation extraction...")
    content = get_documentation()
    with open("notebook_lm_documentation.md", "w", encoding='utf-8') as f:
        f.write(content)
    print("Documentation has been saved to notebook_lm_documentation.md")