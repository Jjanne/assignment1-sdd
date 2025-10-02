# Report – Assignment 1 (SD&D)

## SDLC Model Choice and Justification

**Chosen Model:** Iterative & Incremental (Agile-lite)

**Justification:**  
This project was developed in small, incremental cycles where a minimal version of the system (CRUD endpoints + database persistence) was built first and then extended with new features (filters, error handling, documentation). This approach is well-suited for a small student project because:  

- The scope is limited, so heavy upfront planning (like Waterfall) is unnecessary.  
- It allows quick feedback and fast fixes when requirements change (e.g., switching from `lat/lng` to `start_location`).  
- Testing and verification happen continuously after each iteration, reducing risk of large-scale failures.  
- It keeps overhead low while still encouraging disciplined progress.  

Overall, the iterative model ensures a working system is always available and improvements can be added step by step.

---

## Reflection: Scaling and Adapting for DevOps

If this project were to be developed further in a professional environment, it could be adapted for **DevOps practices** as follows:  

- **Continuous Integration (CI):** Automate linting, testing, and build processes on every commit (e.g., with GitHub Actions).  
- **Automated Testing:** Add unit and integration tests for routers, database operations, and request flows.  
- **Database Migrations:** Use Alembic for versioned schema changes, ensuring smooth upgrades across environments.  
- **Configuration Management:** Replace hard-coded SQLite URL with environment variables to support multiple environments (dev, staging, production).  
- **Containerization:** Package the app with Docker for consistent deployments.  
- **Monitoring & Observability:** Add structured logging, health checks, and error tracking to improve reliability.  
- **Release Management:** Version the API (e.g., `/v1`) and maintain a changelog so clients can upgrade safely.  

These adaptations would make the system more maintainable, scalable, and ready for deployment in real-world settings.

---
