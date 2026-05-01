-- 1. Create the Main CVs Table
CREATE TABLE cvs (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    title TEXT,
    template TEXT DEFAULT 'Classic',
    full_name TEXT,
    email TEXT,
    phone TEXT,
    address TEXT,
    linkedin TEXT,
    summary TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Create the Experience Table
CREATE TABLE experience (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    cv_id BIGINT REFERENCES cvs(id) ON DELETE CASCADE,
    job_title TEXT,
    company TEXT,
    start_date TEXT,
    end_date TEXT,
    description TEXT
);

-- 3. Create the Education Table
CREATE TABLE education (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    cv_id BIGINT REFERENCES cvs(id) ON DELETE CASCADE,
    degree TEXT,
    institution TEXT,
    year TEXT
);

-- 4. Create the Skills Table
CREATE TABLE skills (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    cv_id BIGINT REFERENCES cvs(id) ON DELETE CASCADE,
    skill_name TEXT
);

-- 5. Enable Row Level Security (Optional, but recommended for production)
-- For now, we will allow all access so the app works immediately.
ALTER TABLE cvs ENABLE ROW LEVEL SECURITY;
ALTER TABLE experience ENABLE ROW LEVEL SECURITY;
ALTER TABLE education ENABLE ROW LEVEL SECURITY;
ALTER TABLE skills ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public Access" ON cvs FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Public Access" ON experience FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Public Access" ON education FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Public Access" ON skills FOR ALL USING (true) WITH CHECK (true);

-- 6. Create the Projects Table (Newly Added)
CREATE TABLE projects (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    cv_id BIGINT REFERENCES cvs(id) ON DELETE CASCADE,
    name TEXT,
    link TEXT,
    description TEXT
);
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public Access" ON projects FOR ALL USING (true) WITH CHECK (true);
