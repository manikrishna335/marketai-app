import httpx
import os

UNSPLASH_KEY = "uzuoQOhJhBAPA3oZLUrM5caab91nTcIwrB92kEbX87k"
PEXELS_KEY = os.environ.get("PEXELS_KEY", "")

async def get_unsplash_image(query: str, w: int = 1200, h: int = 628, orientation: str = "landscape") -> str:
    """Fetch real image URL from Unsplash API"""
    try:
        url = "https://api.unsplash.com/photos/random"
        params = {
            "query": query,
            "orientation": orientation,
            "client_id": UNSPLASH_KEY
        }
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(url, params=params)
            if r.status_code == 200:
                data = r.json()
                img_url = data.get("urls", {}).get("regular", "")
                if img_url:
                    # Add size params
                    return f"{img_url}&w={w}&h={h}&fit=crop&crop=center"
    except Exception as e:
        print(f"Unsplash error: {e}")
    
    # Fallback to Picsum with seed based on query
    seed = abs(hash(query)) % 1000
    return f"https://picsum.photos/seed/{seed}/{w}/{h}"

async def get_multiple_images(queries: list, w: int = 1200, h: int = 628, orientation: str = "landscape") -> list:
    """Get multiple images for different queries"""
    import asyncio
    tasks = [get_unsplash_image(q, w, h, orientation) for q in queries]
    return await asyncio.gather(*tasks)
