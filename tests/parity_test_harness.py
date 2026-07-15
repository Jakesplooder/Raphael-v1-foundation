import json
from deepdiff import DeepDiff

class ParityHarness:
    """
    Automated Parity Harness for Epic D Migration.
    Validates Level 1 (Schema) and Level 2 (Value) Parity.
    """
    
    @staticmethod
    def compare_payloads(legacy_payload: dict, rrk_translated_payload: dict) -> dict:
        """
        Deep compares the legacy payload against the RRK-translated payload.
        Returns a diff dictionary.
        """
        diff = DeepDiff(legacy_payload, rrk_translated_payload, ignore_order=True)
        
        result = {
            "level_1_schema_parity": True,
            "level_2_value_parity": True,
            "differences": []
        }
        
        if diff:
            # If there's any dictionary_item_added or dictionary_item_removed, schema parity fails.
            if "dictionary_item_added" in diff or "dictionary_item_removed" in diff:
                result["level_1_schema_parity"] = False
            
            # If there are value changes or type changes, value parity fails.
            if "values_changed" in diff or "type_changes" in diff:
                result["level_2_value_parity"] = False
                
            result["differences"] = json.loads(diff.to_json())
            
        return result

    @staticmethod
    def assert_strict_parity(legacy_payload: dict, rrk_translated_payload: dict, endpoint_name: str):
        """
        Raises an exception if strict Level 1 and Level 2 parity is not achieved.
        """
        result = ParityHarness.compare_payloads(legacy_payload, rrk_translated_payload)
        
        if not result["level_1_schema_parity"]:
            raise AssertionError(f"Parity Test Failed (Level 1: Schema) for {endpoint_name}. Diff: {result['differences']}")
            
        if not result["level_2_value_parity"]:
            raise AssertionError(f"Parity Test Failed (Level 2: Value) for {endpoint_name}. Diff: {result['differences']}")
            
        return True
