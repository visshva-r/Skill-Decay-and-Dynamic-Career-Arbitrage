# SkillPulse Expo Pitch

## One-line pitch

`SkillPulse` is a job-signal intelligence tool for students that detects skill decay from recent local job postings and generates a proof-oriented roadmap to stay employable.

## Problem

Students learn from static syllabi, but hiring demand changes much faster than the curriculum. By the time a student applies, some of their skills are no longer enough and new micro-skills have already become important.

## Gap in current solutions

Most existing platforms recommend generic courses. They do not show:

- which skills are rising right now
- which skills are losing value
- how a student should prove a missing skill through a portfolio artifact

## Solution

SkillPulse compares a student's profile against a curated dataset of recent job postings for a chosen role and city. It then:

- extracts the student's current skills
- finds matched and missing skills
- detects fast-rising skills in the market
- computes a skill decay risk score
- generates a 7-day proof-oriented roadmap
- produces a downloadable judge report (proof of output)

Reliability note (judge-friendly):

- the system is offline-safe using curated data, but also supports optional live refresh and caching to capture real-time drift when available.

## Novelty

- `Skill Decay Meter`: shows which previously common skills are being replaced by newer expectations
- `Proof Pack`: suggests what to build, how to describe it on a resume, and how to package it on GitHub
- `Local market view`: grounds the analysis in one city and one role instead of generic global advice

## Utility

Students can immediately decide:

- what skill to learn next
- what project to build next
- how to present that skill as evidence

## Demo flow

1. Open SkillPulse.
2. Choose `Junior Data Analyst` in `Chennai`.
3. Load the sample student profile (or the weak-match profile to show contrast).
4. Show extracted skills and market matches.
5. Show missing skills and trending skills.
6. Show the skill decay score.
7. Generate the roadmap and proof pack.
8. Download the report.

## SDG alignment (optional, if asked)

- SDG 4 (Quality Education): targeted upskilling roadmap
- SDG 8 (Decent Work & Economic Growth): improved student employability

## Demo closing line

`We are not just telling students what to learn. We are showing what the market changed, what they are missing, and how to prove those skills quickly.`
