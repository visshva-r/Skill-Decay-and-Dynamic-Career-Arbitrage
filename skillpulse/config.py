"""Paths, constants, and lookup maps for SkillPulse."""
from __future__ import annotations

from pathlib import Path

MAX_UPLOAD_SIZE_MB = 10

DATA_PATH = Path("data/job_postings.csv")
SAMPLE_RESUME_PATH = Path("data/sample_resume.txt")
SAMPLE_RESUME_ALT_PATH = Path("data/sample_resume_alt.txt")
RESUME_VISSHVA_AIML_PATH = Path("data/resume_visshva_aiml_redacted.txt")
RESUME_VISSHVA_SDE_PATH = Path("data/resume_visshva_sde_redacted.txt")
SAMPLE_BATCH_STUDENT_3_PATH = Path("data/sample_batch_student_3.txt")
LIVE_CACHE_PATH = Path("data/live_cache.csv")
SNAPSHOT_HISTORY_PATH = Path("data/profile_snapshots.json")

SKILL_CATALOG = [
    "Excel", "SQL", "Python", "Power BI", "Tableau", "DAX",
    "Data Cleaning", "Data Visualization", "Dashboard Storytelling",
    "Dashboard Design", "Data Modeling", "Statistics", "EDA",
    "Business Communication", "Communication", "Presentation Skills",
    "Business Analysis", "Documentation", "Reporting",
    "Stakeholder Reporting", "KPI Tracking", "Data Validation",
    "A/B Testing", "Experiment Analysis", "ETL Basics",
    "MIS Reporting", "Problem Solving", "Storytelling",
    "Attention to Detail", "LLM-assisted Analytics", "Prompt Engineering",
    "TypeScript", "Next.js", "Tailwind CSS", "Node.js", "Express.js",
    "REST APIs", "Docker", "Postman", "PostgreSQL", "MongoDB", "MySQL",
    "Prisma", "Supabase", "NextAuth.js", "HuggingFace Transformers",
    "DistilGPT-2", "Scikit-learn", "XGBoost", "NumPy", "Pandas", "Flask",
    "Java", "C++", "JavaScript", "HTML", "CSS", "React.js", "Git",
    "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch",
    "NLP", "Computer Vision", "AWS", "Azure", "GCP", "Kubernetes",
    "CI/CD", "Agile", "Scrum", "JIRA", "Figma", "R",
    "Financial Modeling", "Risk Analysis", "Regulatory Basics",
    "Healthcare KPIs", "Clinical Data",
]

SKILL_ALIAS = {
    "powerbi": "Power BI", "prompting": "Prompt Engineering",
    "llm analytics": "LLM-assisted Analytics", "story telling": "Storytelling",
    "nextjs": "Next.js", "tailwind": "Tailwind CSS",
    "typescript": "TypeScript", "node": "Node.js", "express": "Express.js",
    "postgres": "PostgreSQL", "postgresql": "PostgreSQL", "mongodb": "MongoDB",
    "scikit learn": "Scikit-learn", "sklearn": "Scikit-learn",
    "huggingface": "HuggingFace Transformers", "reactjs": "React.js",
    "react": "React.js", "ml": "Machine Learning", "dl": "Deep Learning",
    "nlp": "NLP", "cv": "Computer Vision", "amazon web services": "AWS",
    "google cloud": "GCP",
}

PROJECT_MAP = {
    "Power BI": "Build a Chennai retail KPI dashboard with filters, drill-down views, and one executive summary page.",
    "Dashboard Storytelling": "Create a business dashboard that ends with three written insights and one recommendation slide.",
    "DAX": "Build a Power BI report using calculated measures for revenue, growth, and customer retention.",
    "LLM-assisted Analytics": "Create an analytics copilot that turns natural language questions into chart suggestions from a CSV file.",
    "Prompt Engineering": "Design prompts for summarizing dataset insights and compare output quality using a fixed rubric.",
    "Data Modeling": "Create a star-schema style mini warehouse for sales data and show how joins improve reporting speed.",
    "A/B Testing": "Analyze a mock marketing campaign and recommend the winning variant using a simple significance check.",
    "TypeScript": "Convert an existing React UI to TypeScript with strict types and clear API error handling.",
    "Next.js": "Build a small Next.js app with SSR/SSG and an authenticated dashboard flow.",
    "Tailwind CSS": "Rebuild a UI with Tailwind and document a small design system (tokens + components).",
    "Docker": "Containerize a small API + UI, document local run steps, and add health checks.",
    "REST APIs": "Build and document a REST API with pagination, validation, and consistent error responses.",
    "HuggingFace Transformers": "Fine-tune or prompt a small transformer model and evaluate outputs with a measurable rubric.",
    "SQL": "Write advanced SQL queries with window functions, CTEs, and performance optimizations for a sample dataset.",
    "Python": "Build a CLI data pipeline that ingests, cleans, and summarizes CSV data with logging and error handling.",
    "Machine Learning": "Train and evaluate a classification model on a real-world dataset with proper cross-validation.",
    "React.js": "Build a responsive single-page app with state management, routing, and API integration.",
    "Node.js": "Create a RESTful backend with authentication, middleware, and database integration.",
    "Excel": "Build an advanced Excel workbook with pivot tables, lookup chains, and automated summary dashboards.",
    "Tableau": "Design an interactive Tableau dashboard with calculated fields, parameters, and storytelling.",
    "Financial Modeling": "Build a three-statement financial model for a startup scenario with assumptions, scenarios, and sensitivity tables.",
    "Risk Analysis": "Create a portfolio risk dashboard with exposure metrics, trend alerts, and documented mitigation recommendations.",
    "Regulatory Basics": "Map a fintech workflow to key compliance checkpoints and produce a one-page regulatory readiness summary.",
    "Healthcare KPIs": "Design a hospital operations KPI dashboard covering occupancy, wait times, and readmission indicators.",
    "Clinical Data": "Clean and validate a de-identified clinical dataset with documented quality checks and summary statistics.",
}

SKILL_CATEGORIES = {
    "Technical": ["Python", "SQL", "Java", "C++", "JavaScript", "TypeScript", "R", "HTML", "CSS"],
    "Data & Analytics": ["Excel", "Power BI", "Tableau", "Data Cleaning", "Data Visualization",
                         "Dashboard Storytelling", "Dashboard Design", "Data Modeling", "Statistics",
                         "EDA", "Data Validation", "A/B Testing", "Experiment Analysis"],
    "AI / ML": ["Machine Learning", "Deep Learning", "Scikit-learn", "XGBoost", "NumPy", "Pandas",
                "HuggingFace Transformers", "DistilGPT-2", "TensorFlow", "PyTorch", "NLP",
                "Computer Vision", "LLM-assisted Analytics", "Prompt Engineering"],
    "Web & Cloud": ["Next.js", "Tailwind CSS", "Node.js", "Express.js", "REST APIs", "Docker",
                    "React.js", "Flask", "Prisma", "Supabase", "NextAuth.js", "AWS", "Azure",
                    "GCP", "Kubernetes", "CI/CD"],
    "Soft Skills": ["Business Communication", "Communication", "Presentation Skills",
                    "Business Analysis", "Documentation", "Reporting", "Stakeholder Reporting",
                    "KPI Tracking", "Problem Solving", "Storytelling", "Attention to Detail",
                    "Agile", "Scrum"],
    "Tools": ["Git", "Postman", "JIRA", "Figma", "MongoDB", "MySQL", "PostgreSQL", "ETL Basics",
              "MIS Reporting", "DAX"],
}

LEARNING_RESOURCES = {
    "Business Analysis": [
        {"title": "Business Analysis Basics - Microsoft Learn", "url": "https://learn.microsoft.com/en-us/training/modules/get-started-with-business-analysis/", "type": "Official Guide", "time": "2 hrs"},
        {"title": "What is Business Analysis? - IIBA", "url": "https://www.iiba.org/business-analysis-blogs/what-is-business-analysis/", "type": "Article", "time": "30 min"},
    ],
    "Excel": [
        {"title": "Excel Video Training - Microsoft Support", "url": "https://support.microsoft.com/en-us/excel", "type": "Official Training", "time": "4 hrs"},
        {"title": "Excel for Beginners - Great Learning", "url": "https://www.mygreatlearning.com/academy/learn-for-free/courses/excel-for-beginners", "type": "Course", "time": "2 hrs"},
    ],
    "Power BI": [
        {"title": "Microsoft Power BI Learning Path", "url": "https://learn.microsoft.com/en-us/training/powerplatform/power-bi", "type": "Official Docs", "time": "10 hrs"},
        {"title": "Power BI Full Course - freeCodeCamp", "url": "https://www.youtube.com/watch?v=3u7MQz1EyPY", "type": "Video", "time": "4 hrs"},
    ],
    "SQL": [
        {"title": "SQLBolt - Interactive SQL Tutorials", "url": "https://sqlbolt.com/", "type": "Interactive", "time": "3 hrs"},
        {"title": "Mode Analytics SQL Tutorial", "url": "https://mode.com/sql-tutorial/", "type": "Tutorial", "time": "6 hrs"},
    ],
    "Python": [
        {"title": "Python Official Tutorial", "url": "https://docs.python.org/3/tutorial/", "type": "Official Docs", "time": "8 hrs"},
        {"title": "Automate the Boring Stuff", "url": "https://automatetheboringstuff.com/", "type": "Book (Free)", "time": "15 hrs"},
    ],
    "Dashboard Storytelling": [
        {"title": "Storytelling with Data", "url": "https://www.storytellingwithdata.com/", "type": "Book", "time": "5 hrs"},
        {"title": "Data Storytelling Guide", "url": "https://www.tableau.com/learn/articles/data-storytelling", "type": "Article", "time": "1 hr"},
    ],
    "Prompt Engineering": [
        {"title": "Prompt Engineering Guide", "url": "https://www.promptingguide.ai/", "type": "Guide", "time": "4 hrs"},
        {"title": "DeepLearning.AI Prompt Course", "url": "https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/", "type": "Course", "time": "2 hrs"},
    ],
    "Docker": [
        {"title": "Docker Getting Started", "url": "https://docs.docker.com/get-started/", "type": "Official Docs", "time": "3 hrs"},
    ],
    "TypeScript": [
        {"title": "TypeScript Handbook", "url": "https://www.typescriptlang.org/docs/handbook/", "type": "Official Docs", "time": "6 hrs"},
        {"title": "TypeScript Exercises", "url": "https://typescript-exercises.github.io/", "type": "Interactive", "time": "4 hrs"},
    ],
    "React.js": [
        {"title": "React Official Tutorial", "url": "https://react.dev/learn", "type": "Official Docs", "time": "6 hrs"},
    ],
    "Machine Learning": [
        {"title": "Google ML Crash Course", "url": "https://developers.google.com/machine-learning/crash-course", "type": "Course", "time": "15 hrs"},
    ],
    "Tableau": [
        {"title": "Tableau Training", "url": "https://www.tableau.com/learn/training", "type": "Official", "time": "8 hrs"},
    ],
    "Next.js": [
        {"title": "Next.js Learn Course", "url": "https://nextjs.org/learn", "type": "Official", "time": "6 hrs"},
    ],
}

MICRO_CURRICULUM_TEMPLATES = {
    "Power BI": [
        "Connect Power BI to a small relational dataset and clean fields for reporting.",
        "Create one KPI page, one drill-down page, and one stakeholder summary page.",
        "Write 3 business insights and 1 recommendation based on the dashboard.",
    ],
    "SQL": [
        "Practice SELECT, JOIN, GROUP BY, and filtering on a realistic analytics dataset.",
        "Write one CTE and one window-function query for trend analysis.",
        "Export your best 3 queries into a portfolio-ready SQL script with comments.",
    ],
    "Prompt Engineering": [
        "Design prompts for summarization, extraction, and reasoning over the same dataset.",
        "Compare outputs using a small evaluation rubric for accuracy and usefulness.",
        "Turn the best prompt set into a repeatable workflow with before/after examples.",
    ],
}

DEFAULT_GITHUB_SKILL_MAP = {
    "python": "Python", "jupyter notebook": "Python",
    "typescript": "TypeScript", "javascript": "JavaScript",
    "html": "HTML", "css": "CSS",
    "react": "React.js", "next.js": "Next.js", "nextjs": "Next.js",
    "node": "Node.js", "node.js": "Node.js",
    "express": "Express.js", "flask": "Flask",
    "sql": "SQL", "postgresql": "PostgreSQL", "mysql": "MySQL", "mongodb": "MongoDB",
    "docker": "Docker", "kubernetes": "Kubernetes",
    "aws": "AWS", "azure": "Azure", "gcp": "GCP",
    "pandas": "Pandas", "numpy": "NumPy",
    "scikit-learn": "Scikit-learn", "sklearn": "Scikit-learn",
    "tensorflow": "TensorFlow", "pytorch": "PyTorch",
    "nlp": "NLP", "computer-vision": "Computer Vision", "computer vision": "Computer Vision",
    "power bi": "Power BI", "tableau": "Tableau",
    "prompt-engineering": "Prompt Engineering", "prompt engineering": "Prompt Engineering",
    "rest-api": "REST APIs", "rest api": "REST APIs", "api": "REST APIs",
    "tailwindcss": "Tailwind CSS", "tailwind": "Tailwind CSS",
    "postman": "Postman", "git": "Git",
}

ROLE_QUERY_MAP = {
    "Junior Data Analyst": "junior data analyst",
    "Frontend Developer": "frontend developer",
    "AI/ML Intern": "machine learning intern",
    "Business Analyst": "business analyst",
    "Data Science Intern": "data science intern",
    "SDE / Full-stack Developer": "full stack developer",
    "FinTech Analyst": "fintech analyst",
    "Healthcare Data Analyst": "healthcare data analyst",
}

CITY_TO_STATE_MAP = {
    "Chennai": "Tamil Nadu",
    "Bengaluru": "Karnataka",
    "Hyderabad": "Telangana",
    "Pune": "Maharashtra",
    "Gurugram": "Haryana",
    "Mumbai": "Maharashtra",
    "Delhi": "Delhi",
}

CITY_ALIAS_MAP = {
    "bangalore": "Bengaluru", "bengaluru": "Bengaluru",
    "madras": "Chennai", "chennai": "Chennai",
    "hyderabad": "Hyderabad",
    "gurgaon": "Gurugram", "gurugram": "Gurugram",
    "mumbai": "Mumbai", "bombay": "Mumbai",
    "delhi": "Delhi", "new delhi": "Delhi",
}

CAREER_PATHS = {
    "Junior Data Analyst": {
        "current": "Junior Data Analyst",
        "paths": [
            {"role": "Senior Data Analyst", "years": "2-3 yrs", "key_skills": ["SQL", "Power BI", "Dashboard Storytelling", "Statistics"]},
            {"role": "Business Intelligence Analyst", "years": "2-4 yrs", "key_skills": ["Power BI", "DAX", "Data Modeling", "ETL Basics"]},
            {"role": "Data Scientist", "years": "3-5 yrs", "key_skills": ["Python", "Machine Learning", "Statistics", "NLP"]},
            {"role": "Analytics Manager", "years": "5-7 yrs", "key_skills": ["Business Analysis", "Stakeholder Reporting", "KPI Tracking", "Communication"]},
        ],
    },
    "Frontend Developer": {
        "current": "Frontend Developer",
        "paths": [
            {"role": "Senior Frontend Engineer", "years": "2-3 yrs", "key_skills": ["TypeScript", "Next.js", "React.js", "Tailwind CSS"]},
            {"role": "Full-Stack Developer", "years": "2-4 yrs", "key_skills": ["Node.js", "REST APIs", "PostgreSQL", "Docker"]},
            {"role": "Frontend Architect", "years": "4-6 yrs", "key_skills": ["TypeScript", "CI/CD", "Kubernetes", "Agile"]},
            {"role": "Engineering Manager", "years": "5-8 yrs", "key_skills": ["Agile", "Communication", "Scrum", "JIRA"]},
        ],
    },
    "SDE / Full-stack Developer": {
        "current": "SDE / Full-stack Developer",
        "paths": [
            {"role": "Senior SDE", "years": "2-3 yrs", "key_skills": ["Node.js", "TypeScript", "Docker", "REST APIs"]},
            {"role": "Backend Specialist", "years": "2-4 yrs", "key_skills": ["Node.js", "PostgreSQL", "Docker", "Kubernetes"]},
            {"role": "DevOps Engineer", "years": "3-5 yrs", "key_skills": ["Docker", "Kubernetes", "CI/CD", "AWS"]},
            {"role": "Tech Lead", "years": "4-6 yrs", "key_skills": ["Agile", "Communication", "Docker", "CI/CD"]},
        ],
    },
    "AI/ML Intern": {
        "current": "AI/ML Intern",
        "paths": [
            {"role": "ML Engineer", "years": "1-2 yrs", "key_skills": ["Python", "PyTorch", "Machine Learning", "Docker"]},
            {"role": "Data Scientist", "years": "2-3 yrs", "key_skills": ["Python", "Statistics", "Scikit-learn", "SQL"]},
            {"role": "NLP Engineer", "years": "2-4 yrs", "key_skills": ["NLP", "HuggingFace Transformers", "Python", "Deep Learning"]},
            {"role": "AI Research Engineer", "years": "3-5 yrs", "key_skills": ["Deep Learning", "PyTorch", "Computer Vision", "NLP"]},
        ],
    },
    "Business Analyst": {
        "current": "Business Analyst",
        "paths": [
            {"role": "Senior BA", "years": "2-3 yrs", "key_skills": ["Business Analysis", "SQL", "Power BI", "Stakeholder Reporting"]},
            {"role": "Product Manager", "years": "3-5 yrs", "key_skills": ["Business Analysis", "Agile", "Communication", "JIRA"]},
            {"role": "Data Analyst Lead", "years": "3-4 yrs", "key_skills": ["SQL", "Power BI", "Dashboard Storytelling", "KPI Tracking"]},
            {"role": "Strategy Consultant", "years": "5-7 yrs", "key_skills": ["Business Analysis", "Presentation Skills", "Communication", "Documentation"]},
        ],
    },
    "Data Science Intern": {
        "current": "Data Science Intern",
        "paths": [
            {"role": "Data Scientist", "years": "1-2 yrs", "key_skills": ["Python", "Machine Learning", "Statistics", "SQL"]},
            {"role": "ML Engineer", "years": "2-3 yrs", "key_skills": ["Python", "PyTorch", "Docker", "REST APIs"]},
            {"role": "Analytics Engineer", "years": "2-4 yrs", "key_skills": ["SQL", "Python", "ETL Basics", "Power BI"]},
            {"role": "AI Product Specialist", "years": "3-5 yrs", "key_skills": ["Machine Learning", "Prompt Engineering", "Communication", "Agile"]},
        ],
    },
    "FinTech Analyst": {
        "current": "FinTech Analyst",
        "paths": [
            {"role": "Senior FinTech Analyst", "years": "2-3 yrs", "key_skills": ["Financial Modeling", "SQL", "Power BI", "Risk Analysis"]},
            {"role": "Risk Analyst", "years": "2-4 yrs", "key_skills": ["Risk Analysis", "Python", "Regulatory Basics", "Excel"]},
            {"role": "Product Analyst (FinTech)", "years": "3-5 yrs", "key_skills": ["Business Analysis", "SQL", "Dashboard Storytelling", "Stakeholder Reporting"]},
            {"role": "Compliance Analytics Lead", "years": "4-6 yrs", "key_skills": ["Regulatory Basics", "Documentation", "KPI Tracking", "Communication"]},
        ],
    },
    "Healthcare Data Analyst": {
        "current": "Healthcare Data Analyst",
        "paths": [
            {"role": "Senior Healthcare Analyst", "years": "2-3 yrs", "key_skills": ["Healthcare KPIs", "SQL", "Power BI", "Clinical Data"]},
            {"role": "Health Informatics Specialist", "years": "2-4 yrs", "key_skills": ["Clinical Data", "Data Validation", "Python", "Dashboard Storytelling"]},
            {"role": "Healthcare BI Lead", "years": "3-5 yrs", "key_skills": ["Power BI", "SQL", "Stakeholder Reporting", "KPI Tracking"]},
            {"role": "Population Health Analyst", "years": "4-6 yrs", "key_skills": ["Statistics", "Python", "Healthcare KPIs", "Data Visualization"]},
        ],
    },
}

# --- Hackathon Recommendations ---
HACKATHON_MAP = {
    "Machine Learning": [
        {"name": "Kaggle Competitions", "url": "https://www.kaggle.com/competitions", "platform": "Kaggle", "type": "Ongoing"},
        {"name": "Google ML Challenge", "url": "https://developers.google.com/machine-learning", "platform": "Google", "type": "Annual"},
    ],
    "Deep Learning": [
        {"name": "Kaggle Competitions", "url": "https://www.kaggle.com/competitions", "platform": "Kaggle", "type": "Ongoing"},
    ],
    "NLP": [
        {"name": "SemEval Shared Tasks", "url": "https://semeval.github.io/", "platform": "ACL", "type": "Annual"},
        {"name": "Kaggle NLP Competitions", "url": "https://www.kaggle.com/competitions?tagIds=11208", "platform": "Kaggle", "type": "Ongoing"},
    ],
    "Computer Vision": [
        {"name": "Kaggle Vision Competitions", "url": "https://www.kaggle.com/competitions", "platform": "Kaggle", "type": "Ongoing"},
    ],
    "Python": [
        {"name": "Unstop Hackathons", "url": "https://unstop.com/hackathons", "platform": "Unstop", "type": "Rolling"},
        {"name": "HackerRank Challenges", "url": "https://www.hackerrank.com/domains/python", "platform": "HackerRank", "type": "Ongoing"},
    ],
    "React.js": [
        {"name": "MLH Hackathons", "url": "https://mlh.io/seasons/2026/events", "platform": "MLH", "type": "Seasonal"},
        {"name": "Devpost Hackathons", "url": "https://devpost.com/hackathons", "platform": "Devpost", "type": "Rolling"},
    ],
    "TypeScript": [
        {"name": "MLH Hackathons", "url": "https://mlh.io/seasons/2026/events", "platform": "MLH", "type": "Seasonal"},
        {"name": "Devpost Hackathons", "url": "https://devpost.com/hackathons", "platform": "Devpost", "type": "Rolling"},
    ],
    "Next.js": [
        {"name": "Vercel Hackathons", "url": "https://devpost.com/hackathons", "platform": "Devpost", "type": "Rolling"},
    ],
    "Docker": [
        {"name": "Docker Community Challenges", "url": "https://www.docker.com/community", "platform": "Docker", "type": "Periodic"},
    ],
    "SQL": [
        {"name": "HackerRank SQL Challenges", "url": "https://www.hackerrank.com/domains/sql", "platform": "HackerRank", "type": "Ongoing"},
        {"name": "StrataScratch Practice", "url": "https://www.stratascratch.com/", "platform": "StrataScratch", "type": "Ongoing"},
    ],
    "Power BI": [
        {"name": "Maven Analytics Challenges", "url": "https://mavenanalytics.io/challenges", "platform": "Maven Analytics", "type": "Monthly"},
    ],
    "Tableau": [
        {"name": "Makeover Monday", "url": "https://www.makeovermonday.co.uk/", "platform": "Community", "type": "Weekly"},
    ],
    "Prompt Engineering": [
        {"name": "Unstop AI Hackathons", "url": "https://unstop.com/hackathons", "platform": "Unstop", "type": "Rolling"},
    ],
    "Data Visualization": [
        {"name": "Makeover Monday", "url": "https://www.makeovermonday.co.uk/", "platform": "Community", "type": "Weekly"},
    ],
    "Excel": [
        {"name": "Excel World Championship", "url": "https://fmworldcup.com/", "platform": "FMWC", "type": "Annual"},
    ],
    "Node.js": [
        {"name": "Devpost Hackathons", "url": "https://devpost.com/hackathons", "platform": "Devpost", "type": "Rolling"},
    ],
    "REST APIs": [
        {"name": "Postman API Hackathons", "url": "https://www.postman.com/", "platform": "Postman", "type": "Periodic"},
    ],
}

# --- Benchmark Profiles (Placed Professionals) ---
BENCHMARK_PROFILES = {
    "Junior Data Analyst": {
        "label": "Placed Junior Data Analyst (1 yr exp)",
        "skills": ["Excel", "SQL", "Python", "Power BI", "Tableau", "Data Cleaning",
                   "Dashboard Storytelling", "Data Visualization", "Statistics", "EDA",
                   "Stakeholder Reporting", "Presentation Skills"],
        "summary": "Placed at a mid-size analytics firm in Bengaluru after completing a data analytics bootcamp. Built 3 dashboards during internship. Strong SQL and Excel foundation with Power BI proficiency.",
    },
    "Frontend Developer": {
        "label": "Placed Frontend Developer (1 yr exp)",
        "skills": ["React.js", "TypeScript", "JavaScript", "HTML", "CSS", "Next.js",
                   "Tailwind CSS", "REST APIs", "Git", "Figma", "Postman", "Agile"],
        "summary": "Placed at a product startup in Chennai. Built 2 production React apps during internship. Strong TypeScript and Next.js skills with CI/CD experience.",
    },
    "AI/ML Intern": {
        "label": "Placed AI/ML Engineer (1 yr exp)",
        "skills": ["Python", "Machine Learning", "Deep Learning", "PyTorch", "Scikit-learn",
                   "Pandas", "NumPy", "NLP", "HuggingFace Transformers", "Docker",
                   "Prompt Engineering", "Git"],
        "summary": "Placed at an AI research lab in Hyderabad. Published 1 conference paper. Built NLP pipelines and deployed models using Docker and REST APIs.",
    },
    "Business Analyst": {
        "label": "Placed Business Analyst (1 yr exp)",
        "skills": ["Excel", "SQL", "Power BI", "Business Analysis", "Documentation",
                   "Presentation Skills", "Stakeholder Reporting", "KPI Tracking",
                   "Dashboard Storytelling", "Communication", "Agile", "JIRA"],
        "summary": "Placed at a consulting firm in Pune. Led 2 client-facing reporting projects. Strong documentation and stakeholder management skills.",
    },
    "Data Science Intern": {
        "label": "Placed Data Scientist (1 yr exp)",
        "skills": ["Python", "Machine Learning", "Scikit-learn", "Pandas", "NumPy",
                   "SQL", "Statistics", "EDA", "Data Visualization", "Power BI",
                   "Prompt Engineering", "Git"],
        "summary": "Placed at a fintech company in Bengaluru. Built 2 ML models in production. Strong statistical foundation with visualization skills.",
    },
    "SDE / Full-stack Developer": {
        "label": "Placed Full-Stack Developer (1 yr exp)",
        "skills": ["JavaScript", "TypeScript", "React.js", "Node.js", "Express.js",
                   "Next.js", "PostgreSQL", "MongoDB", "Docker", "REST APIs",
                   "Git", "CI/CD", "Agile"],
        "summary": "Placed at a SaaS startup in Bengaluru. Shipped 3 full-stack features end-to-end. Strong backend + DevOps awareness.",
    },
    "FinTech Analyst": {
        "label": "Placed FinTech Analyst (1 yr exp)",
        "skills": ["Excel", "SQL", "Python", "Financial Modeling", "Power BI",
                   "Risk Analysis", "Regulatory Basics", "Dashboard Storytelling",
                   "Data Validation", "Stakeholder Reporting", "Communication"],
        "summary": "Placed at a payments startup in Mumbai. Built risk dashboards and regulatory reporting packs for operations teams.",
    },
    "Healthcare Data Analyst": {
        "label": "Placed Healthcare Data Analyst (1 yr exp)",
        "skills": ["Excel", "SQL", "Python", "Power BI", "Healthcare KPIs",
                   "Clinical Data", "Data Validation", "Dashboard Storytelling",
                   "Statistics", "Documentation", "Communication"],
        "summary": "Placed at a health-tech firm in Bengaluru. Delivered clinical KPI dashboards and validated patient-flow reporting datasets.",
    },
}


# Visual system: ink + teal (intentionally not purple / "AI dashboard" defaults)
BRAND = {
    "ink": "#0f172a",
    "ink_muted": "#334155",
    "accent": "#0d9488",
    "accent_soft": "#ccfbf1",
    "slate": "#e2e8f0",
    "matched": "#065f46",
    "matched_bg": "#ecfdf5",
    "missing": "#9f1239",
    "missing_bg": "#fff1f2",
    "rising": "#92400e",
    "rising_bg": "#fffbeb",
    "benchmark": "#1e3a5f",
    "benchmark_bg": "#eff6ff",
}

CUSTOM_CSS = """
<style>
    :root {
        --sp-ink: #0f172a;
        --sp-muted: #64748b;
        --sp-accent: #0d9488;
        --sp-accent-soft: #ccfbf1;
        --sp-border: #e2e8f0;
    }
    .main .block-container { padding-top: 1.25rem; max-width: 1180px; }
    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid var(--sp-border);
        border-left: 3px solid var(--sp-accent);
        border-radius: 4px;
        padding: 14px 18px;
    }
    div[data-testid="stMetric"] label {
        font-size: 0.78rem !important;
        font-weight: 600 !important;
        color: var(--sp-muted) !important;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        border-bottom: 1px solid var(--sp-border);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 0;
        padding: 10px 16px;
        font-weight: 600;
        color: var(--sp-muted);
    }
    .skill-tag {
        display: inline-block;
        padding: 3px 10px;
        margin: 2px 3px;
        border-radius: 3px;
        font-size: 0.82rem;
        font-weight: 500;
        letter-spacing: 0.01em;
    }
    .skill-matched { background-color: #ecfdf5; color: #065f46; border: 1px solid #a7f3d0; }
    .skill-missing { background-color: #fff1f2; color: #9f1239; border: 1px solid #fecdd3; }
    .skill-rising { background-color: #fffbeb; color: #92400e; border: 1px solid #fde68a; }
    .skill-benchmark { background-color: #eff6ff; color: #1e3a5f; border: 1px solid #bfdbfe; }
    .section-header {
        font-size: 1.05rem;
        font-weight: 700;
        color: var(--sp-ink);
        margin: 0.85rem 0 0.45rem;
        padding-bottom: 0.25rem;
        border-bottom: 1px solid var(--sp-border);
    }
    .sp-hero {
        border: 1px solid var(--sp-border);
        border-left: 4px solid var(--sp-accent);
        background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
        padding: 1rem 1.15rem;
        margin-bottom: 0.85rem;
    }
    .sp-hero h2 {
        margin: 0 0 0.35rem 0;
        font-size: 1.35rem;
        color: var(--sp-ink);
        font-weight: 700;
    }
    .sp-hero p {
        margin: 0;
        color: var(--sp-muted);
        font-size: 0.95rem;
        line-height: 1.45;
    }
    .sp-evidence {
        border: 1px solid var(--sp-border);
        background: #f8fafc;
        padding: 0.55rem 0.75rem;
        margin: 0.35rem 0;
        font-size: 0.9rem;
        color: var(--sp-ink);
        border-radius: 3px;
    }
    .sp-next {
        border: 1px solid #99f6e4;
        background: var(--sp-accent-soft);
        padding: 0.75rem 0.9rem;
        margin: 0.5rem 0 0.85rem;
        border-radius: 3px;
        color: #115e59;
        font-size: 0.95rem;
    }
    footer { visibility: hidden; }
</style>
"""
