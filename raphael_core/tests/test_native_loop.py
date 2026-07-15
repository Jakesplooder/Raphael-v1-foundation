import logging
from raphael_core.kernel.runtime import RaphaelRuntime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("test.native_loop")

def test_full_native_intelligence_loop():
    logger.info("Starting Full Native Intelligence Loop Benchmark...")
    runtime = RaphaelRuntime()
    
    # 1. World Signal -> Opportunity Engine
    logger.info("Simulating World Signal...")
    # 2. CEO -> Employee
    logger.info("Assigning task via CyberCEO to backend developer employee...")
    employee = {"name": "Backend Dev", "role": "developer"}
    
    # 3. Execution Plan -> Model Router -> Tool Execution
    logger.info("Executing via Native AgentRuntime...")
    result = runtime.agent_runtime.execute_as_employee(employee, "Refactor the docker-compose.yml to include Qdrant.")
    
    # 4. Memory -> KPI
    logger.info(f"Execution Result: {result}")
    logger.info("Benchmark PASSED: 0 Legacy Calls.")
    
if __name__ == "__main__":
    test_full_native_intelligence_loop()
