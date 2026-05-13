import asyncio

import httpx
from bs4 import BeautifulSoup


async def fetch_page(url: str) -> str | None:
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; MedRegMCP/1.0; documentation indexer)"
    }
    async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.text
        except httpx.HTTPError as e:
            print(f"  Failed to fetch {url}: {e}")
            return None


def extract_text(html: str, url: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["nav", "footer", "header", "script", "style", "aside"]):
        tag.decompose()

    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else ""

    main = soup.find("main") or soup.find("article") or soup.find("div", {"role": "main"})
    if main:
        text = main.get_text(separator="\n", strip=True)
    else:
        body = soup.find("body")
        text = body.get_text(separator="\n", strip=True) if body else soup.get_text(separator="\n", strip=True)

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    cleaned_text = "\n".join(lines)

    return {"title": title, "text": cleaned_text, "url": url}


async def crawl_sources(sources: list[dict]) -> list[dict]:
    results = []
    for source in sources:
        url = source["url"]
        print(f"  Fetching: {source['title']}")

        # Skip PDF URLs - they need different handling
        if url.endswith(".pdf"):
            print(f"  Skipping PDF (not supported in simple crawl): {url}")
            continue

        html = await fetch_page(url)
        if html:
            doc = extract_text(html, url)
            doc["org"] = source["org"]
            doc["source_title"] = source["title"]
            results.append(doc)

    return results


def crawl_sources_sync(sources: list[dict]) -> list[dict]:
    return asyncio.run(crawl_sources(sources))
