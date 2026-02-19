import httpx
from bs4 import BeautifulSoup

async def fetch_url(url: str) -> str:
    """Fetch HTML content from a URL."""
    async with httpx.AsyncClient(follow_redirects=True, timeout=10.0) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text

def clean_html(html_content: str) -> str:
    """
    Extract meaningful text from HTML, prioritizing main content areas.
    Removes navigation, footers, and boilerplate.
    """
    soup = BeautifulSoup(html_content, "html.parser")

    # Remove unwanted elements
    for element in soup(["script", "style", "nav", "footer", "header", "noscript", "aside", "meta", "link"]):
        element.extract()

    # Remove elements by class/id commonly used for noise
    noise_selectors = [
        ".nav", ".footer", ".header", ".menu", ".sidebar", ".cookie-banner", ".popup",
        "#nav", "#footer", "#header", "#menu", "#sidebar", "#cookie-banner"
    ]
    for selector in noise_selectors:
        for element in soup.select(selector):
            element.extract()

    # Try to find main content
    main_content = soup.find("main") or soup.find("article") or soup.find("div", role="main")
    
    # Use main content if found, otherwise fallback to body
    target = main_content if main_content else soup.body or soup

    # Get text
    text = target.get_text()

    # Normalize whitespace
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text
