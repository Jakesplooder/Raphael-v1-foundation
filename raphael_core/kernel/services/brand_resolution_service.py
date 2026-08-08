import logging
from typing import List, Dict, Any

from raphael_core.world_model import load_model
from raphael_core.legacy import load_config

logger = logging.getLogger("kernel.services.brand_resolution")

class BrandResolutionService:
    def __init__(self, config=None):
        self.config = config or load_config(Path(r"C:\Users\cyber\Downloads\RalphaelOS\config.json"))
        self.model = load_model(self.config)

    def _log_resolution(self, input_type: str, input_val: str, traversal: List[str], excluded: List[str], result_count: int, reason: str = "No COVERS relationship"):
        """
        Emits the Execution Explanation Log as requested by the user.
        """
        log_lines = [
            "=== Graph Resolution ===",
            f"Input:\n{input_type} = {input_val}",
            f"\nTraversal:"
        ]
        if traversal:
            for t in traversal:
                log_lines.append(t)
        else:
            log_lines.append("None")
            
        log_lines.append(f"\nExcluded:")
        if excluded:
            for e in excluded:
                log_lines.append(e)
        else:
            log_lines.append("None")
            
        log_lines.append(f"Reason:\n{reason}")
        log_lines.append(f"\nResult:\n{result_count} matches")
        log_lines.append("========================\n")
        
        print("\n".join(log_lines))
        logger.info("\n".join(log_lines))

    def resolve_brands_for_category(self, category_name: str) -> List[Dict[str, Any]]:
        """
        Given a category name, return all Brand nodes that COVER it.
        Also resolves ambiguity (e.g. 'AI Marketing' vs 'AI').
        """
        # Find exact category node by name
        target_category_ids = []
        all_brands = []
        
        for node in self.model.get("nodes", []):
            if node["node_type"] == "Category" and node["name"].casefold() == category_name.casefold():
                target_category_ids.append(node["node_id"])
            if node["node_type"] == "Brand":
                all_brands.append(node)
                
        if not target_category_ids:
            self._log_resolution(
                input_type="Category",
                input_val=category_name,
                traversal=[],
                excluded=[b["name"] for b in all_brands],
                result_count=0,
                reason="Category not found in World Model"
            )
            return []

        # Find relationships pointing to these categories with type 'COVERS'
        brand_ids = set()
        traversal_log = []
        
        for rel in self.model.get("relationships", []):
            if rel["relationship_type"] == "COVERS" and rel["to_node"] in target_category_ids:
                brand_ids.add(rel["from_node"])
                
        matched_brands = []
        excluded_brands = []
        
        for brand in all_brands:
            if brand["node_id"] in brand_ids:
                matched_brands.append(brand)
                traversal_log.append(f"{brand['name']} -> COVERS -> {category_name}")
            else:
                excluded_brands.append(brand["name"])
                
        self._log_resolution(
            input_type="Category",
            input_val=category_name,
            traversal=traversal_log,
            excluded=excluded_brands,
            result_count=len(matched_brands)
        )
        
        return matched_brands

    def resolve_categories_for_brand(self, brand_name: str) -> List[Dict[str, Any]]:
        target_brand_ids = []
        all_cats = []
        
        for node in self.model.get("nodes", []):
            if node["node_type"] == "Brand" and node["name"].casefold() == brand_name.casefold():
                target_brand_ids.append(node["node_id"])
            if node["node_type"] == "Category":
                all_cats.append(node)
                
        if not target_brand_ids:
            return []
            
        cat_ids = set()
        for rel in self.model.get("relationships", []):
            if rel["relationship_type"] == "COVERS" and rel["from_node"] in target_brand_ids:
                cat_ids.add(rel["to_node"])
                
        matched_cats = [c for c in all_cats if c["node_id"] in cat_ids]
        return matched_cats

    def resolve_brand_contexts(self, category_name: str) -> List[Any]:
        # To be implemented for Phase 2B
        # This will turn matched_brands into BrandContext objects
        brands = self.resolve_brands_for_category(category_name)
        return brands
