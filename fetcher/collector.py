# collector.py
# This file will contain the collector implementation
# Code to be added later

import json
import httpx
import itertools
from app.models import Product, SessionLocal, engine

Product.metadata.create_all(bind=engine)

COUNTRY = "US"
LIMIT = 200
ENTITIES = {
    "software": "software",
    "movie": "movie",
    "tvSeason": "tvSeason",
    "tvEpisode": "tvEpisode",
    "musicTrack": "musicTrack",
    "album": "album",
    "ebook": "ebook",
    "podcast": "podcast",
    "hardware": "hardware"
}

def _request(term, entity, offset=0):
    url = "https://itunes.apple.com/search"
    params = {
        "term": term,
        "country": COUNTRY,
        "entity": entity,
        "limit": LIMIT,
        "offset": offset,
        "media": "software" if entity == "software" else "all"
    }
    resp = httpx.get(url, params=params, timeout=30.0)
    resp.raise_for_status()
    data = resp.json()
    return data.get("results", [])

def _normalize(item):
    return {
        "id": item.get("trackId") or item.get("collectionId") or item.get("artistId"),
        "product_type": item.get("kind") or item.get("wrapperType"),
        "name": item.get("trackName") or item.get("collectionName") or item.get("artistName"),
        "seller": item.get("sellerName") or item.get("artistName"),
        "price": item.get("price") or item.get("collectionPrice"),
        "currency": item.get("currency"),
        "min_ios": item.get("minimumOsVersion"),
        "genres": "|".join(item.get("genres", [])),
        "release_date": item.get("releaseDate"),
        "description": item.get("description") or item.get("shortDescription"),
        "raw_json": json.dumps(item, ensure_ascii=False)
    }

def collect_all():
    session = SessionLocal()
    try:
        session.query(Product).delete()
        session.commit()
        for entity_key, entity_val in ENTITIES.items():
            for term in itertools.chain(
                [chr(c) for c in range(48, 58)],  # 0‑9
                [chr(c) for c in range(97, 123)]  # a‑z
            ):
                offset = 0
                while True:
                    batch = _request(term, entity_val, offset)
                    if not batch:
                        break
                    for raw in batch:
                        data = _normalize(raw)
                        if data["id"] is None:
                            continue
                        obj = Product(**data)
                        session.add(obj)
                    session.commit()
                    offset += LIMIT
    finally:
        session.close()
    print("✅ Каталог оновлено!")

if __name__ == "__main__":
    collect_all()

