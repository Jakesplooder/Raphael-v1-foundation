import logging
from typing import Dict, Any, List

from ..repositories.commerce_repository import CommerceRepository
from ..models.commerce import Product, ProductType, ProductStatus

logger = logging.getLogger("rrk.services.commerce")

class CommerceService:
    """Core domain logic for Commerce Products."""
    
    def __init__(self, repository: CommerceRepository):
        self.repository = repository
        from .commerce_capability_registry import ProductCapabilityRegistry
        self.registry = ProductCapabilityRegistry()

    def create_product(self, product_type: ProductType, name: str, concept: str) -> Product:
        from uuid import uuid4
        product_id = f"PROD-{uuid4().hex[:8].upper()}"
        
        p = Product(
            product_id=product_id,
            product_type=product_type,
            name=name,
            concept=concept,
            status=ProductStatus.DRAFT
        )
        self.repository.upsert_product(p)
        return p

    def get_commerce_launch_template(self, product_type: str = "shirt_design") -> List[Dict[str, Any]]:
        """
        Returns a WorkflowPlan template utilizing decoupled capabilities via the Registry.
        """
        # Determine specific providers dynamically using the Capability Registry
        design_provider = self.registry.get_provider_for(product_type)
        mockup_provider = self.registry.get_provider_for("mockup")
        seo_provider = self.registry.get_provider_for("seo")
        
        return [
            {
                "name": "Phase 1: Concept & Research",
                "action": "research_market",
                "provider": seo_provider,
                "parameters": {"strategy": "broad_search"}
            },
            {
                "name": "Phase 2: Generate Core Asset",
                "action": "generate_asset",
                "provider": design_provider,
                "parameters": {"asset_type": product_type}
            },
            {
                "name": "Phase 3: Create Mockups/Previews",
                "action": "apply_mockup",
                "provider": mockup_provider,
                "parameters": {}
            },
            {
                "name": "Phase 4: SEO & Copywriting",
                "action": "generate_listing_copy",
                "provider": "seo",
                "parameters": {"target_platform": "etsy"}
            },
            {
                "name": "Phase 6: Publish Listing",
                "action": "publish_listing",
                "provider": "etsy",
                "parameters": {"status": "draft"}
            }
        ]
