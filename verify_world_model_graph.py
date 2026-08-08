import sys
import os
from pathlib import Path

sys.path.insert(0, r"C:\Users\cyber\Downloads\RalphaelOS")

from raphael_core.world_model import WorldModelBuilder
from raphael_core.legacy import load_config
from raphael_core.kernel.services.brand_resolution_service import BrandResolutionService

def setup_test_graph():
    config = load_config(Path(r"C:\Users\cyber\Downloads\RalphaelOS\config.json"))
    
    # We want a fresh world model for this test to avoid noise.
    # To be safe, we'll override the world model directory
    config.os_root = Path(r"C:\Users\cyber\Downloads\RalphaelOS\sandbox_www\test_wm")
    config.vault = config.os_root / "vault"
    config.approved_write_folders.append(config.os_root)
    
    builder = WorldModelBuilder(config)
    
    # 1. Create Brands
    fm_id = builder.add_node("Brand", "Focus Marketing", "Brand", source_reference="test")
    mm_id = builder.add_node("Brand", "MentorMap", "Brand", source_reference="test")
    ros_id = builder.add_node("Brand", "Raphael OS", "Brand", source_reference="test")
    
    # 2. Create Categories
    ai_mktg_id = builder.add_node("Category", "AI Marketing", "Cat", source_reference="test")
    content_mktg_id = builder.add_node("Category", "Content Marketing", "Cat", source_reference="test")
    career_adv_id = builder.add_node("Category", "Career Advice", "Cat", source_reference="test")
    sw_eng_id = builder.add_node("Category", "Software Engineering", "Cat", source_reference="test")
    ai_id = builder.add_node("Category", "AI", "Cat", source_reference="test")
    
    # 3. Create COVERS relationships
    builder.add_relationship(fm_id, ai_mktg_id, "COVERS", "Test", source_reference="test")
    builder.add_relationship(fm_id, content_mktg_id, "COVERS", "Test", source_reference="test")
    
    builder.add_relationship(mm_id, ai_mktg_id, "COVERS", "Test", source_reference="test")
    builder.add_relationship(mm_id, career_adv_id, "COVERS", "Test", source_reference="test")
    
    builder.add_relationship(ros_id, ai_mktg_id, "COVERS", "Test", source_reference="test")
    builder.add_relationship(ros_id, sw_eng_id, "COVERS", "Test", source_reference="test")
    
    # Add an AI relationship to Raphael OS to test ambiguity (AI vs AI Marketing)
    builder.add_relationship(ros_id, ai_id, "COVERS", "Test", source_reference="test")
    
    builder.build()
    return config

def run_tests():
    config = setup_test_graph()
    service = BrandResolutionService(config)
    
    print("\n\n--- RUNNING PHASE 2A TESTS ---\n")
    
    # 1. Multi-Brand Test
    print("[TEST 1: MULTI-BRAND SELECTIVITY]")
    brands = service.resolve_brands_for_category("AI Marketing")
    names = sorted([b["name"] for b in brands])
    print(f"Expected: ['Focus Marketing', 'MentorMap', 'Raphael OS']")
    print(f"Actual:   {names}")
    assert names == ["Focus Marketing", "MentorMap", "Raphael OS"]
    
    # 2. Selectivity Test
    print("\n[TEST 2: SELECTIVITY (Single Match)]")
    brands = service.resolve_brands_for_category("Career Advice")
    names = sorted([b["name"] for b in brands])
    print(f"Expected: ['MentorMap']")
    print(f"Actual:   {names}")
    assert names == ["MentorMap"]
    
    # 3. Negative Test
    print("\n[TEST 3: NEGATIVE TEST (No Match)]")
    brands = service.resolve_brands_for_category("Quantum Gardening")
    names = sorted([b["name"] for b in brands])
    print(f"Expected: []")
    print(f"Actual:   {names}")
    assert names == []
    
    # 4. Ambiguity Test
    print("\n[TEST 4: AMBIGUITY TEST (AI vs AI Marketing)]")
    brands = service.resolve_brands_for_category("AI")
    names = sorted([b["name"] for b in brands])
    print(f"Expected: ['Raphael OS']")
    print(f"Actual:   {names}")
    assert names == ["Raphael OS"]
    
    print("\nALL PHASE 2A TESTS PASSED.")

if __name__ == "__main__":
    run_tests()
