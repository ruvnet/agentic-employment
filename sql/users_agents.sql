-- Create the table for storing user information
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(50) NOT NULL,
    tenant_id UUID NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the table for storing agent information
CREATE TABLE agents (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    tenant_id UUID NOT NULL,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    description TEXT,
    avatar_url TEXT,
    llm_base VARCHAR(50),
    prompt TEXT,
    knowledge_base_url TEXT,
    learning_rate FLOAT,
    exploration_rate FLOAT,
    training_iterations INT,
    batch_size INT,
    max_tokens INT,
    temperature FLOAT,
    top_p FLOAT,
    frequency_penalty FLOAT,
    presence_penalty FLOAT,
    stop_sequences TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial users for tenant UUID 1 and UUID 2
INSERT INTO users (id, email, password_hash, role, tenant_id) VALUES
('00000000-0000-0000-0000-000000000001', 'user1@example.com', 'hashed_password_1', 'admin', '00000000-0000-0000-0000-000000000001'),
('00000000-0000-0000-0000-000000000002', 'user2@example.com', 'hashed_password_2', 'user', '00000000-0000-0000-0000-000000000002');

-- Insert initial agents for tenant UUID 1 and UUID 2
INSERT INTO agents (user_id, tenant_id, name, type, status, description) VALUES
('00000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000001', 'Agent1', 'Conversational', 'Active', 'Description for Agent1'),
('00000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-000000000002', 'Agent2', 'Analytical', 'Idle', 'Description for Agent2');

-- Enable Row-Level Security (RLS) for users and agents tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE agents ENABLE ROW LEVEL SECURITY;

-- Create RLS policies for users
CREATE POLICY "tenant_isolation" ON users
FOR ALL
USING (tenant_id = current_setting('app.current_tenant')::uuid);

CREATE POLICY "Enable real-time" ON users
FOR SELECT USING (true);

CREATE POLICY "user_access" ON users
FOR SELECT
USING (auth.uid() = id);

-- Create RLS policies for agents
CREATE POLICY "tenant_isolation" ON agents
FOR ALL
USING (tenant_id = current_setting('app.current_tenant')::uuid);

CREATE POLICY "Enable real-time" ON agents
FOR SELECT USING (true);

CREATE POLICY "agent_access" ON agents
FOR SELECT
USING (auth.uid() = user_id);

-- Create indexes for optimization
CREATE INDEX idx_users_tenant_id ON users(tenant_id);
CREATE INDEX idx_agents_tenant_id ON agents(tenant_id);
