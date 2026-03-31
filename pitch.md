# SkillPulse Expo Pitch

## One-line pitch

`SkillPulse` is a continuous skill-intelligence tool for students that compares resumes and GitHub signals against live or curated job-market demand, then generates proof-oriented learning actions.

## Problem

Students learn from static syllabi, but hiring demand changes much faster than the curriculum. By the time a student applies, some of their skills are no longer enough and new micro-skills have already become important.

## Gap in current solutions

Most existing platforms recommend generic courses. They do not show:

- which skills are rising right now
- which skills are losing value
- how a student should prove a missing skill through a portfolio artifact

## Solution

SkillPulse compares a student's profile against recent job postings for a chosen role and city. It then:

- extracts the student's current skills
- enriches the profile using optional GitHub repository signals
- finds matched and missing skills
- detects fast-rising skills in the market
- computes a skill decay risk score
- computes a resume compatibility score
- tracks profile snapshots over time
- generates a 7-day and Gemini-enhanced proof-oriented roadmap
- produces a downloadable analysis report

Reliability note (judge-friendly):

- the system is offline-safe using curated data, but also supports optional Adzuna-powered live refresh and caching to capture real-time drift when available.

## Novelty

- `Continuous Skill Alert`: highlights a rising skill that the current profile does not show strongly
- `Skill Decay Meter`: shows which previously common skills are being replaced by newer expectations
- `Proof Pack`: suggests what to build, how to describe it on a resume, and how to package it on GitHub
- `GitHub Signal Overlay`: folds public repository metadata into profile analysis
- `Local market view`: grounds the analysis in one city and one role instead of generic global advice

## Utility

Students can immediately decide:

- what skill to learn next
- what project to build next
- how to present that skill as evidence

## Demo flow

1. Open SkillPulse.
2. Start with `Fresh profile`.
3. Choose a target role and city, or upload the richer live jobs CSV.
4. Paste a short profile or upload a resume.
5. Optionally paste a GitHub profile URL to activate GitHub-aware analysis.
6. Show extracted skills, missing skills, and trend evidence.
7. Show the resume compatibility score and skill decay risk.
8. Open `Continuous Skill Alert`, `Profile Snapshot History`, and `Gemini Vision Layer`.
9. Show the roadmap, proof pack, and downloadable report.

## SDG alignment (optional, if asked)

- SDG 4 (Quality Education): targeted upskilling roadmap
- SDG 8 (Decent Work & Economic Growth): improved student employability

## Demo closing line

`We are not just telling students what to learn. We show what the market changed, what the student's profile misses, and what they should build next to stay employable.`
