# userprog

> Generated from a read-only source. The original files were not copied, modified, moved, renamed, deleted, overwritten, indexed, or uploaded.
> raphael-knowledge-summary: true

## Title

userprog

## Source Path Reference

`K:\userprog`

## Category

Programming

## Course

CSC4103 — Operating Systems

## Technologies

- C/C++

## Skills Demonstrated

- Implementation with C
- operating systems concepts
- systems programming

## Summary

#ifndef USERPROG_SYSCALL_H #define USERPROG_SYSCALL_H void syscall_init(void); #endif /* userprog/syscall.h */ #ifndef USERPROG_TSS_H #define USERPROG_TSS_H #include <stdint.h> struct tss; void tss_init(void); struct tss* tss_get(void); void tss_update(void); #endif /* userprog/tss.h */ #ifndef USERPROG_EXCEPTION_H #define USERPROG_EXCEPTION_H /* Page fault error code bits that describe the cause of the exception. */ #define PF_P 0x1 /* 0: not-present page. 1: access rights violation. */ #define PF_W 0x2 /* 0: read, 1: write. */ #define PF_U 0x4 /* 0: kernel, 1: user process. */ void exception_init(void); void exception_print_stats(void); #endif /* userprog/exception.h */ #ifndef USERPROG_GDT_H #define USERPROG_GDT_H #include "threads/loader.h" /* Segment selectors. More selectors are defined by the loader in loader.h. */ #define SEL_UCSEG 0x1B /* User code selector. */ #define...

## Files Found

- `userprog\exception.c` (.c, 6328 bytes)
- `userprog\exception.h` (.h, 397 bytes)
- `userprog\gdt.c` (.c, 4945 bytes)
- `userprog\gdt.h` (.h, 405 bytes)
- `userprog\pagedir.c` (.c, 6755 bytes)
- `userprog\pagedir.h` (.h, 702 bytes)
- `userprog\process.c` (.c, 20113 bytes)
- `userprog\process.h` (.h, 2016 bytes)
- `userprog\syscall.c` (.c, 8623 bytes)
- `userprog\syscall.h` (.h, 113 bytes)
- `userprog\tss.c` (.c, 3503 bytes)
- `userprog\tss.h` (.h, 180 bytes)


## Portfolio Value

Medium — Curated score 52/100.

## Resume Bullet Potential

- Built or completed **userprog** using C/C++, demonstrating technical implementation.
- Add measurable outcomes, scope, grade, users, or performance results after human review.

## Lessons Learned

- Preserve requirements, decisions, tests, and final outcomes together so the project remains explainable later.
- Review this generated summary against the original source before using it in a resume or portfolio.

## Suggested Tags

- #c-c++
- #programming

## Related Raphael Projects/Goals

- Project: Shell Project
- Project: CSC4330 Project Group J

## Safety Record

- Source access: read-only
- Source files copied: no
- Raw source indexed: no
- Credential-bearing files/content: skipped
- External uploads: none

## Knowledge ID

KNOW-50BEB716DF

## Course Code

CSC4103

## Course Name

Operating Systems

## Suggested Title

PintOS User Programs

## Project Type

Operating Systems Lab

## Technology Stack

- C

## Assignment/Project Status

Likely Completed

## Portfolio Score

52/100

## Resume Value

6/10

## Outcome

Unclear — human curation needed.

## Likely Duplicates

- None detected.

## Curation Flags

- None.

## Cleanup Suggestions

- Document implemented system calls, process behavior, and test results.

## Classification Scores

- Technical depth: 5/10
- Completeness: 8/10
- Uniqueness: 5/10
- Career relevance: 8/10
- Demo potential: 5/10
- Resume value: 6/10
- Business relevance: 3/10
- Cleanup effort: 3/10

## Knowledge Relationships

- `KNOW-4F5C580EBD` csc4103-fall2024-assignment2-Jakesplooder — same_course (0.94): CSC4103
- `KNOW-4F5C580EBD` csc4103-fall2024-assignment2-Jakesplooder — same_cluster (0.88): Operating Systems Cluster
- `KNOW-668F0A4293` Homework3 answer — same_cluster (0.88): Operating Systems Cluster
- `KNOW-38EBC2F305` opam64 — shared_technology (0.86): C
- `KNOW-4F5C580EBD` csc4103-fall2024-assignment2-Jakesplooder — shared_technology (0.86): C
- `KNOW-A397A2E244` lab_2 — shared_technology (0.86): C
- `KNOW-BDFE213910` K Drive Knowledge Root — shared_technology (0.86): C
- `KNOW-A397A2E244` lab_2 — shared_skill (0.80): Implementation with C
- `KNOW-19023766AB` ajanua3_proj2 — shared_career_track (0.78): Software Engineering
- `KNOW-21573891BF` Substitution Cipher Cryptanalysis — shared_career_track (0.78): Software Engineering
- `KNOW-3F7C86815B` n8n Workflow Automation Collection — shared_career_track (0.78): Software Engineering
- `KNOW-6057D9E8B2` Substitution Cipher Cryptanalysis — shared_career_track (0.78): Software Engineering
- `KNOW-668F0A4293` Homework3 answer — shared_career_track (0.78): Software Engineering
- `KNOW-70F2729989` Substitution Cipher Cryptanalysis — shared_career_track (0.78): Software Engineering
- `KNOW-7F1BB3F008` Untitled Folder — shared_career_track (0.78): Software Engineering
- `KNOW-8D7E89B99E` OCaml Homework 3 — shared_career_track (0.78): Software Engineering
- `KNOW-8EE4596287` LCIntel — shared_career_track (0.78): Software Engineering
- `KNOW-A8E8979849` proj0f23StarterCodeJava — shared_career_track (0.78): Software Engineering
- `KNOW-A9A046D623` OCaml Homework 3 — shared_career_track (0.78): Software Engineering
- `KNOW-B2AF17275B` Programming Project # 3 Starter Code-20231107 — shared_career_track (0.78): Software Engineering

## Relationship Concepts

- Course Relationship: CSC4103 (0.98)
- Technology Relationship: C (0.92)
- Project Family Relationship: Operating Systems Lab (0.90)
- Project Family Relationship: Operating Systems Cluster (0.88)
- Skill Relationship: Implementation with C (0.84)
- Skill Relationship: operating systems concepts (0.84)
- Skill Relationship: systems programming (0.84)
- Career Relationship: Software Engineering (0.82)
- Portfolio Relationship: Tier 2 (0.72)
- Employee Skill Relationship: Developer Agent (0.72)
- Council Relationship: Engineering Council (0.68)

## Relationship Metadata

- Generated: 2026-06-18T00:20:50
- Direct relationships: 20
- Concept relationships: 11
