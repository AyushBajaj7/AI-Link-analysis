"""Website extraction service with streaming download and SSRF-safe redirect validation."""

import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from app.utils.url_validator import validate_url

MAX_SIZE = 2 * 1024 * 1024  # 2 MB limit
MAX_REDIRECTS = 5
MAX_CONTENT_CHARS = 15000

UNWANTED_TAGS = (
    "script",
    "style",
    "noscript",
    "svg",
    "canvas",
    "iframe",
    "header",
    "footer",
    "nav",
    "aside",
    "form",
    "dialog",
    "button",
)


async def extract_website(url: str) -> dict:
    """Fetch website HTML securely, follow validated redirects, and extract structured text."""
    timeout = httpx.Timeout(20.0)
    headers = {
        "User-Agent": "AILinkAnalysisBot/1.0"
    }

    async with httpx.AsyncClient(
        timeout=timeout,
        follow_redirects=False,
        headers=headers
    ) as client:
        current_url = str(url)

        for attempt in range(MAX_REDIRECTS + 1):
            validate_url(current_url)

            async with client.stream(
                "GET",
                current_url
            ) as response:
                if response.status_code in (301, 302, 303, 307, 308):
                    location = response.headers.get("Location")
                    if not location:
                        raise ValueError("Redirect response missing Location header")
                    current_url = urljoin(current_url, location)
                    if attempt == MAX_REDIRECTS:
                        raise ValueError("Too many redirects")
                    continue

                if response.status_code >= 400:
                    raise httpx.HTTPStatusError(
                        f"Website returned HTTP status {response.status_code}",
                        request=response.request,
                        response=response
                    )

                content_type = response.headers.get("Content-Type", "").lower()
                if content_type and not any(ct in content_type for ct in ("text/html", "application/xhtml+xml", "text/plain")):
                    raise ValueError(f"Unsupported content type: {content_type}")

                content_bytes = bytearray()
                async for chunk in response.aiter_bytes():
                    content_bytes.extend(chunk)
                    if len(content_bytes) > MAX_SIZE:
                        raise ValueError("Page size exceeds maximum allowed limit (2 MB)")

                html = content_bytes.decode("utf-8", errors="replace")
                break

    soup = BeautifulSoup(html, "html.parser")

    # Extract Title with og:title fallback
    title = ""
    if soup.title and soup.title.string:
        title = soup.title.string.strip()
    if not title:
        og_title = soup.find("meta", attrs={"property": "og:title"})
        if og_title and og_title.get("content"):
            title = og_title["content"].strip()

    # Extract Meta Description with og:description fallback
    description = ""
    desc_tag = soup.find("meta", attrs={"name": "description"}) or soup.find(
        "meta", attrs={"property": "og:description"}
    )
    if desc_tag and desc_tag.get("content"):
        description = desc_tag["content"].strip()

    # Extract Headings (h1, h2, h3)
    headings = []
    seen = set()
    for tag in soup.find_all(["h1", "h2", "h3"]):
        text = tag.get_text(separator=" ", strip=True)
        if text and (tag.name, text) not in seen:
            seen.add((tag.name, text))
            headings.append({"tag": tag.name, "text": text})

    # Remove non-content and noise tags
    for tag in soup(UNWANTED_TAGS):
        tag.decompose()

    # Extract readable text
    text = soup.get_text(separator=" ", strip=True)
    content = " ".join(text.split())[:MAX_CONTENT_CHARS]

    return {
        "url": current_url,
        "title": title,
        "description": description,
        "headings": headings,
        "content": content
    }
