import time
import os
from typing import Dict, Any, List

class BuilderDashboard:
    """
    Real-time CLI dashboard for tracking Builder execution.
    """
    
    def __init__(self, workflow_name: str, workspace: str, model: str):
        self.workflow_name = workflow_name
        self.workspace = workspace
        self.model = model
        self.start_time = time.time()
        
        self.current_phase = "Initializing"
        self.retries = 0
        self.compile_errors = 0
        self.review_findings = 0
        self.git_checkpoints = 0
        self.lessons_learned = 0
        
    def update_phase(self, phase: str):
        self.current_phase = phase
        
    def add_retry(self):
        self.retries += 1
        
    def add_compile_error(self):
        self.compile_errors += 1
        
    def add_review_finding(self):
        self.review_findings += 1
        
    def add_git_checkpoint(self):
        self.git_checkpoints += 1
        
    def add_lesson_learned(self):
        self.lessons_learned += 1
        
    def render(self):
        elapsed = int(time.time() - self.start_time)
        mins, secs = divmod(elapsed, 60)
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=========================================")
        print("           BUILDER STATUS                ")
        print("=========================================")
        print(f"Current Workflow : {self.workflow_name}")
        print(f"Current Phase    : {self.current_phase}")
        print(f"Workspace        : {self.workspace}")
        print(f"Current Model    : {self.model}")
        print("-----------------------------------------")
        print(f"Retries          : {self.retries}")
        print(f"Compile Errors   : {self.compile_errors}")
        print(f"Review Findings  : {self.review_findings}")
        print(f"Git Checkpoints  : {self.git_checkpoints}")
        print(f"Lessons Learned  : {self.lessons_learned}")
        print("-----------------------------------------")
        print(f"Elapsed Time     : {mins:02d}:{secs:02d}")
        print("=========================================")
