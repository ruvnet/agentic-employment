-- Create the table for storing chat history
CREATE TABLE chat_history (
    id SERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL,
    user_message TEXT NOT NULL,
    bot_response TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the table for storing agent details
CREATE TABLE agent_details (
    id SERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    performance FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial agent data
INSERT INTO agent_details (tenant_id, name, type, status, performance) VALUES
('tenant-1-uuid', 'Sales AI', 'Conversational', 'Active', 4.5),
('tenant-1-uuid', 'Support Bot', 'Retrieval-based', 'Active', 4.2),
('tenant-2-uuid', 'Marketing Assistant', 'Generative', 'Inactive', 3.8),
('tenant-2-uuid', 'Data Analyst', 'Analytical', 'Active', 4.7),
('tenant-1-uuid', 'HR Coordinator', 'Conversational', 'Active', 4.1);

-- Enable Row-Level Security (RLS) for chat_history and agent_details tables
ALTER TABLE chat_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_details ENABLE ROW LEVEL SECURITY;

-- Create RLS policies for chat_history
CREATE POLICY "tenant_isolation" ON chat_history
FOR ALL
USING (tenant_id = current_setting('app.current_tenant')::uuid);

CREATE POLICY "Enable real-time" ON chat_history
FOR SELECT USING (true);

CREATE POLICY "chat_access" ON chat_history
FOR SELECT
USING (auth.uid() = user_id);

-- Create RLS policies for agent_details
CREATE POLICY "tenant_isolation" ON agent_details
FOR ALL
USING (tenant_id = current_setting('app.current_tenant')::uuid);

CREATE POLICY "Enable real-time" ON agent_details
FOR SELECT USING (true);

CREATE POLICY "agent_access" ON agent_details
FOR SELECT
USING (auth.uid() = user_id);

-- Create indexes for optimization
CREATE INDEX idx_chat_history_tenant_id ON chat_history(tenant_id);
CREATE INDEX idx_agent_details_tenant_id ON agent_details(tenant_id);