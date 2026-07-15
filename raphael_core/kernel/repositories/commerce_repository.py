import json
import logging
from pathlib import Path
from typing import List, Optional, Any

from ..models.commerce import Product, Asset, Listing

logger = logging.getLogger("rrk.repositories.commerce")

class CommerceRepository:
    """Universal repository for Commerce products, assets, and listings."""
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        self.products_file = self.base_path / "products.json"
        self.assets_file = self.base_path / "assets.json"
        self.listings_file = self.base_path / "listings.json"
        
        for f in [self.products_file, self.assets_file, self.listings_file]:
            if not f.exists():
                self._write_json(f, [])

    def _read_json(self, path: Path) -> List[Any]:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []

    def _write_json(self, path: Path, data: List[Any]) -> None:
        temp = path.with_suffix(".tmp")
        temp.write_text(json.dumps(data, indent=2), encoding="utf-8")
        temp.replace(path)

    # --- Products ---
    def get_products(self) -> List[Product]:
        data = self._read_json(self.products_file)
        return [Product(**row) for row in data]

    def get_product(self, product_id: str) -> Optional[Product]:
        return next((p for p in self.get_products() if p.product_id == product_id), None)

    def save_products(self, products: List[Product]) -> None:
        self._write_json(self.products_file, [p.model_dump() for p in products])

    def upsert_product(self, product: Product) -> None:
        products = self.get_products()
        idx = next((i for i, p in enumerate(products) if p.product_id == product.product_id), -1)
        if idx >= 0:
            products[idx] = product
        else:
            products.append(product)
        self.save_products(products)

    # --- Assets ---
    def get_assets(self) -> List[Asset]:
        data = self._read_json(self.assets_file)
        return [Asset(**row) for row in data]

    def get_asset(self, asset_id: str) -> Optional[Asset]:
        return next((a for a in self.get_assets() if a.asset_id == asset_id), None)

    def save_assets(self, assets: List[Asset]) -> None:
        self._write_json(self.assets_file, [a.model_dump() for a in assets])

    def upsert_asset(self, asset: Asset) -> None:
        assets = self.get_assets()
        idx = next((i for i, a in enumerate(assets) if a.asset_id == asset.asset_id), -1)
        if idx >= 0:
            assets[idx] = asset
        else:
            assets.append(asset)
        self.save_assets(assets)

    # --- Listings ---
    def get_listings(self) -> List[Listing]:
        data = self._read_json(self.listings_file)
        return [Listing(**row) for row in data]

    def get_listing(self, listing_id: str) -> Optional[Listing]:
        return next((l for l in self.get_listings() if l.listing_id == listing_id), None)

    def save_listings(self, listings: List[Listing]) -> None:
        self._write_json(self.listings_file, [l.model_dump() for l in listings])

    def upsert_listing(self, listing: Listing) -> None:
        listings = self.get_listings()
        idx = next((i for i, l in enumerate(listings) if l.listing_id == listing.listing_id), -1)
        if idx >= 0:
            listings[idx] = listing
        else:
            listings.append(listing)
        self.save_listings(listings)
