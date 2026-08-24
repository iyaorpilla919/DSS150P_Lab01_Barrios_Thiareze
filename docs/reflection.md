# Reflection

**1. Which source would be easiest to integrate into a future pipeline, and why?**

customers.csv is the easiest to integrate. It's a flat file with a fixed, predictable schema, and pandas read it in a single line with no special handling. This contrasts with orders.json, which has a nested structure requiring extra parsing before it can be flattened, and the REST API, which depends on an internet connection and can fail if the endpoint is slow or down. Since customers.csv has none of these complications, and its columns mapped directly into PostgreSQL types with almost no adjustment when I built the lab.customers table in Task 3.2, it's the source I'd trust to integrate first.

**2. Which source presents the greatest schema or data-quality risk, and what evidence supports your answer?**

The REST API carries the highest risk. It's a live, external system I don't control. When I inspected it in Task 2.3, it returned 100 JSON records, but nothing guarantees the field names, types, or record count will stay the same on the next call. A file's structure only changes if someone edits it, but an API provider could update their service without warning. There's also the added risk of the request failing outright due to network issues, rate limiting, or downtime — none of which apply to a local file.

**3. What could go wrong if a pipeline is built before the source schema and contract are understood?**

Skipping the schema and contract step invites silent, hard-to-trace errors. If a column's type is auto-inferred without checking, something like a customer ID with leading zeros could quietly become a plain integer and lose information. If a field is assumed to always be filled in when it isn't — which I confirmed happens with email and city in customers.csv, both had missing values during profiling — any downstream step depending on that field could break or produce incomplete results. Without a contract to compare against, there's no early warning system if the source's structure changes later.

**4. How do Git, virtual environments, containers, and documentation improve reproducibility for a data-engineering team?**

Each tool solves a different piece of the "works on my machine" problem. Git keeps a shared history of every change, so the team works from the same version and can trace what changed and when. Virtual environments isolate each project's Python packages, avoiding version conflicts with anything else installed locally. Containers go further — the PostgreSQL setup I ran through Docker behaves identically regardless of operating system, removing an entire category of environment-related bugs. Documentation like the README and data contract captures reasoning that isn't visible in the code itself — why a field is nullable, or what the schema evolution policy is — so a new team member could pick up the project without asking me directly.