# AIRecruiter – Recruiter-Facing RAG System

### Main description
AIRecruiter (this platform) is a recruiter-facing application I built to help recruiters understand my profile more effectively and evaluate my fit for open roles. It demonstrates applied skills in data science, retrieval-augmented generation (RAG), prompt engineering, and deploying LLM-powered systems into production.

### Overview
I designed AIRecruiter as a decision-support system rather than a traditional résumé screening tool. Instead of relying on keyword matching or heuristic scoring, it uses evidence-based reasoning to evaluate my profile information in context and reflect uncertainty explicitly. It consolidates my professional background, including my transition from energy engineering to data science and machine learning, and it applies evidence-based reasoning to answer questions or assess job fit.
The system prioritizes grounded evaluation, conservative judgment, and human-like recruiter reasoning, while still allowing for informed inference about transferable experience and learning potential.

### Problem Motivation
Nowadays recruiters face +100 applications through each job offer they post. Current algorithms are mostly based on keyword matching and heuristic scoring systems. The hiring process becomes impersonal, often failing to capture transferable experience, learning and adaptation potential and contextual relevance of past roles.
AIRecruiter is built to assist recruiters on getting to know Rafa’s profile better before-hand and ask any question related to his professional life.

### System Architecture
The system follows a Retrieval-Augmented Generation (RAG) architecture:
Structured profile data stored as curated markdown documents
Offline chunking and embedding of profile data
Similarity-based retrieval at query time
Prompt-driven reasoning over verified context
No external knowledge injection about the candidate
Two interaction modes are supported:
QA mode: answers recruiter questions about the profile
Job-fit mode: evaluates alignment with a pasted job description

### Reasoning Design
A key design decision was to separate reasoning from scoring.
Instead of asking the model to compute a score directly, the system:
Forces structured, step-by-step recruiter reasoning
Requires explicit separation between:
demonstrated experience
adjacent or transferable experience
inferred potential
Uses epistemic language to reflect uncertainty
Derives a fit score only after reasoning is complete
This mirrors how human recruiters typically evaluate profiles and reduces brittle or overconfident outputs.

### Tradeoffs and Constraints
Several deliberate constraints were introduced:
The model may only reason over retrieved, verified profile content
Claims must be grounded in evidence
Absolute statements are discouraged unless explicitly supported
Optimism is allowed, but must be framed as potential rather than fact
This creates outputs that are conservative, explainable, and recruiter-realistic, at the cost of sometimes underselling edge-case strengths.

### Technical Stack
Python
FastAPI for the backend API
Streamlit for the recruiter-facing UI
OpenAI embeddings and chat models
Docker for containerization
Google Cloud Run for deployment
Google Secret Manager for secure API key handling

### Key Learnings
Through this project, I deepened my understanding of:
RAG system design
Prompt engineering as a form of system control
“End-to-end development and cloud deployment of ML-powered applications”
The importance of epistemic humility in automated decision-support tools

### Current Status
The system is fully deployed and operational, supporting both recruiter Q&A and job-fit evaluation. The reasoning layer is intentionally frozen to prioritize stability and explainability, with future work focused on UX improvements rather than core logic changes.
