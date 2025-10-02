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

# Datasbase Setup

``` sql
CREATE TABLE records (
    id VARCHAR(64) PRIMARY KEY,
    project_name TEXT NOT NULL,
    registry TEXT NOT NULL,
    vintage INT NOT NULL,
    quantity INT NOT NULL,
    serial_number TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE events (
    event_id SERIAL PRIMARY KEY,
    record_id VARCHAR(64) REFERENCES records(id),
    event_type TEXT NOT NULL,
    details JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);


CREATE USER carbon_user WITH PASSWORD 'carbon123';
GRANT CONNECT ON DATABASE carbon_db TO carbon_user;
\c carbon_db
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE records TO carbon_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE events TO carbon_user;
GRANT USAGE, SELECT, UPDATE ON SEQUENCE events_event_id_seq TO carbon_user;
ALTER TABLE records OWNER TO carbon_user;
ALTER TABLE events OWNER TO carbon_user;
ALTER SEQUENCE events_event_id_seq OWNER TO carbon_user;
```

# Setup Instructions:-

1. 

```bash
export DATABASE_URL="postgresql://carbon_user:carbon123@localhost/carbon_db"
```
2. Run the API

``` bash
uvicorn app.main:app --reload
```

3. Go To FastAPI Docs:
    http://127.0.0.1:8000/docs

OR

3. Go To Terminal 
``` python

python seed_records.py

```

To insert all sample records from sample-registry.json


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


