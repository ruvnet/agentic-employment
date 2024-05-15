-- Create the table for storing agent interactions
CREATE TABLE agent_interactions (
    id SERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL,
    agent1 VARCHAR(255) NOT NULL,
    agent2 VARCHAR(255) NOT NULL,
    interaction_type VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial agent interaction data
INSERT INTO agent_interactions (tenant_id, agent1, agent2, interaction_type, description, status) VALUES
('tenant-1-uuid', 'Sales AI', 'Support Bot', 'Collaboration Request', 'Help with customer issue', 'In Progress'),
('tenant-1-uuid', 'Marketing Assistant', 'Data Analyst', 'Knowledge Share', 'Campaign insights', 'Completed'),
('tenant-2-uuid', 'HR Coordinator', 'IT Helpdesk', 'Task Handoff', 'New employee onboarding', 'Pending'),
('tenant-2-uuid', 'Data Analyst', 'Sales AI', 'Feedback', 'Improve data collection process', 'In Progress'),
('tenant-1-uuid', 'All Agents', 'Hive Mind', 'Hive Structure Update', 'Reorganize into specialized clusters', 'Completed'),
('tenant-2-uuid', 'Support Bot', 'Support Bot', 'Evolutionary Adaptation', 'Optimize response time by 10%', 'In Progress'),
('tenant-1-uuid', 'Project Manager', 'Task Allocation Engine', 'Self-Orchestration', 'Dynamically assign tasks based on agent availability and skills', 'Ongoing');

-- Enable Row-Level Security (RLS) for agent_interactions table
ALTER TABLE agent_interactions ENABLE ROW LEVEL SECURITY;

-- Create RLS policies for agent_interactions
CREATE POLICY "tenant_isolation" ON agent_interactions
FOR ALL
USING (tenant_id = current_setting('app.current_tenant')::uuid);

CREATE POLICY "Enable real-time" ON agent_interactions
FOR SELECT USING (true);

CREATE POLICY "interaction_access" ON agent_interactions
FOR SELECT
USING (auth.uid() = user_id);

-- Create indexes for optimization
CREATE INDEX idx_agent_interactions_tenant_id ON agent_interactions(tenant_id);