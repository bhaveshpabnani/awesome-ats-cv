# Skills Packaging

## Goal

Create a skills section that is comprehensive enough for ATS keyword matching but grouped enough for humans to scan quickly.

## Grouping pattern for technical CVs

- Languages: Python, C++, C, Java, Go, TypeScript, JavaScript, SQL, HTML, CSS, TeX
- Backend: FastAPI, Django, Node.js, Express, REST APIs, GraphQL, Pydantic, SQLAlchemy
- Frontend: React, Next.js, Vite, Tailwind CSS, shadcn/ui, Ant Design, Recharts, WebSocket, Server-Sent Events (SSE)
- AI/ML: Large Language Models (LLM), Retrieval-Augmented Generation (RAG), LangGraph, LangChain, PyTorch, H2O.ai, NetworkX, prompt engineering, reranking, vector search
- Data: Pandas, NumPy, PostgreSQL, MongoDB, DynamoDB, Redis, Supabase, Qdrant, Neo4j, Kafka
- Cloud/DevOps: AWS, Docker, GitHub Actions, Nginx, Infisical, Modal, Firebase, CI/CD, Linux
- Observability/Quality: Langfuse, logging, tracing, unit tests, integration tests, release checks

## Rules

- Use exact official capitalization for proper nouns.
- Prefer `JavaScript`, `TypeScript`, `PostgreSQL`, `MongoDB`, `DynamoDB`, `GitHub Actions`, `Supabase`, `LangGraph`, `LangChain`.
- Expand critical acronyms once if useful for ATS: `Retrieval-Augmented Generation (RAG)`, `Large Language Models (LLM)`, `Server-Sent Events (SSE)`.
- Do not list skills that do not appear in experience/projects unless the user explicitly wants a broader keyword section.
- Remove duplicate tools across categories unless duplication improves parser matching.
- Keep skills relevant to the target profile. For tech roles, prioritize languages, systems, AI, backend, frontend, data, cloud, and testing over societies or generic soft skills.
- Revisit the skills section after rewriting bullets. Add important technologies introduced in experience/project bullets, such as `FastAPI`, `Redis`, `Aurora`, `AWS EC2`, `Kafka`, `Playwright`, `WinUI 3`, or `SwiftUI`, when they are actually supported by the CV.
- Keep skill rows scannable rather than congested. Group related technologies, use pipe separators with one space around each pipe, and avoid more than one visually overloaded row per category.
- Use skills to support keyword matching, but make bullets prove the skill through impact, scale, and implementation detail.
- When tailoring for SDE/backend/distributed systems roles, emphasize programming languages, backend frameworks, cloud, databases, caching, distributed systems, CI/CD, testing, and performance metrics before extracurricular items.
