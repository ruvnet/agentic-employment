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
('00000000-0000-0000-0000-000000000001', 'Sales AI', 'Conversational', 'Active', 4.5),
('00000000-0000-0000-0000-000000000001', 'Support Bot', 'Retrieval-based', 'Active', 4.2),
('00000000-0000-0000-0000-000000000002', 'Marketing Assistant', 'Generative', 'Inactive', 3.8),
('00000000-0000-0000-0000-000000000002', 'Data Analyst', 'Analytical', 'Active', 4.7),
('00000000-0000-0000-0000-000000000001', 'HR Coordinator', 'Conversational', 'Active', 4.1);

-- Enable Row-Level Security (RLS) for chat_history and agent_details tables
ALTER TABLE agent_details ENABLE ROW LEVEL SECURITY;

-- Create RLS policies for agent_details
CREATE POLICY "tenant_isolation" ON agent_details
FOR ALL
USING (tenant_id = current_setting('app.current_tenant')::uuid);

CREATE POLICY "Enable real-time" ON agent_details
FOR SELECT USING (true);

CREATE POLICY "agent_access" ON agent_details
FOR SELECT
USING (tenant_id = current_setting('app.current_tenant')::uuid);

-- Create indexes for optimization
CREATE INDEX idx_agent_details_tenant_id ON agent_details(tenant_id);