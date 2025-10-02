# Project Structure

```bash
offset/
│
├─ app/
│  ├─ main.py           # FastAPI routes
│  ├─ models.py         # SQLAlchemy ORM models
│  ├─ schemas.py        # Pydantic request/response schemas
│  ├─ crud.py           # Database logic (create, get, retire)
│  ├─ utils.py          # Deterministic ID generator
│  └─ database.py       # Database connection config
│
├─ sample-registry.json # Sample data for for the database
├─ seed_records.py      # Script to POST sample-registry to API
└─ README.md
```

# Database Structure:

1. Master Credit Table (credit once created, never updated/deleted)
2. Events Table (to track all the updates to all credits (sold/retired), along with details like timestamps, etc)


# Reflection Questions

1. How did you design the ID so it’s always the same for the same input?

-> Built a deterministic ID function that combines key fields like project_name,registry, vintage, quantity to a single normalized string hashed with SHA-256.

2. Why did you use an event log instead of updating the record directly?

-> Since the records table is not supposed to be updated, to record the events going on with a credit record, I created an events table for registering the sale, retirement of the record. By checking with the events table, we can add checks to avoid selling a retired credit, or double selling.

3. If two people tried to retire the same credit at the same time, what would break?

-> Without any safeguards, the same credit maybe retired twice in the events table, breaking the system of retirement

4. How would I fix it?

-> By establishing concurrency control, I created a unique index on (record_id) where the event_type="retired"/"sold", checking if it exists or not, If yes, pass a 409 Conflict detailed "already retired"/"already sold"


