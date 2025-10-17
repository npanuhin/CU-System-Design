```sql
CREATE TYPE project_role AS ENUM ('admin', 'member');

CREATE TABLE users (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name  TEXT NOT NULL CHECK (full_name <> ''),
    email      TEXT NOT NULL UNIQUE CHECK (email ~* '^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$'),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE projects (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        TEXT NOT NULL CHECK (name <> ''),
    owner_id    UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT, -- A project must have an owner.
    start_date  DATE,
    due_date    DATE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT due_date_after_start_date CHECK (due_date >= start_date)
);

CREATE TABLE project_members (
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    user_id    UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role       project_role NOT NULL DEFAULT 'member',

    PRIMARY KEY (project_id, user_id) -- Ensures a user is only on a project once.
);

CREATE TABLE tasks (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title       TEXT NOT NULL CHECK (title <> ''),
    status      TEXT NOT NULL DEFAULT 'todo' CHECK (status IN ('todo', 'in_progress', 'done')),
    project_id  UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE, -- Tasks are deleted with their project.
    assignee_id UUID REFERENCES users(id) ON DELETE SET NULL, -- Task becomes unassigned if user is deleted.
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

---

`tasks.status` can also be solved by using another table or an ENUM type, but for the sake of demonstration, I used a CHECK constraint there
