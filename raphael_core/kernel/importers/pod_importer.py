import json
from pathlib import Path
import logging
from ..repositories.commerce_repository import CommerceRepository
from ..models.commerce import Product, ProductType, ProductStatus, Asset, AssetType

logger = logging.getLogger("rrk.importers.pod")

def migrate_legacy_podflows(os_root: Path):
    """
    One-time script to migrate legacy PODFLOW-*.json files
    into the new CommerceRepository structure.
    """
    legacy_dir = os_root / "PODStudio" / "workflows"
    commerce_dir = os_root / "CommerceStudio"
    
    if not legacy_dir.exists():
        logger.info("No legacy PODFLOW directory found.")
        return
        
    repository = CommerceRepository(commerce_dir)
    
    count = 0
    for file_path in legacy_dir.glob("PODFLOW-*.json"):
        try:
            data = json.loads(file_path.read_text(encoding="utf-8"))
            workflow_id = data.get("workflow_id", file_path.stem)
            
            # Check if it was completed
            current_stage = data.get("current_stage", 0)
            status = ProductStatus.ARCHIVED if current_stage >= 13 else ProductStatus.DRAFT
            
            product_id = f"PROD-{workflow_id.replace('PODFLOW-', '')}"
            
            # Create Product
            p = Product(
                product_id=product_id,
                product_type=ProductType.POD,
                name=f"Legacy POD {workflow_id}",
                concept=data.get("request", ""),
                status=status,
                workflow_id=workflow_id
            )
            repository.upsert_product(p)
            
            # Look for assets in the data
            if "generated_image_paths" in data:
                for img_path in data["generated_image_paths"]:
                    a = Asset(
                        asset_id=f"ASSET-{hash(img_path)}",
                        product_id=product_id,
                        asset_type=AssetType.PNG,
                        file_path=img_path,
                    )
                    repository.upsert_asset(a)
                    p.assets.append(a.asset_id)
            
            # Save product again with linked assets
            repository.upsert_product(p)
            count += 1
        except Exception as e:
            logger.error(f"Failed to migrate {file_path}: {e}")
            
    logger.info(f"Successfully migrated {count} legacy POD workflows into Commerce products.")
    
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        migrate_legacy_podflows(Path(sys.argv[1]))
    else:
        print("Usage: python pod_importer.py <os_root_path>")
