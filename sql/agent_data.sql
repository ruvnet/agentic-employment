-- Create the table for storing agent data
CREATE TABLE agent_data (
    agent_id SERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL,
    agent_name VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,
    current_task VARCHAR(255) NOT NULL,
    performance_metrics VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial agent data
INSERT INTO agent_data (tenant_id, agent_name, status, current_task, performance_metrics) VALUES
('tenant-1-uuid', 'NLP Agent', 'Active', 'Text Processing', 'High'),
('tenant-1-uuid', 'Vision Agent', 'Idle', 'Image Classification', 'Medium'),
('tenant-2-uuid', 'Data Agent', 'Failed', 'Data Cleaning', 'Low'),
('tenant-2-uuid', 'Chatbot', 'Active', 'Customer Service', 'High'),
('tenant-1-uuid', 'Analysis Agent', 'Idle', 'Data Analysis', 'Medium');

-- Create the table for storing chat history
CREATE TABLE chat_history (
    id SERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL,
    user_message TEXT NOT NULL,
    bot_response TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the table for storing error logs
CREATE TABLE error_log (
    id SERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL,
    time TIMESTAMP NOT NULL,
    agent_id INT REFERENCES agent_data(agent_id),
    error_type VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial error log data
INSERT INTO error_log (tenant_id, time, agent_id, error_type, message) VALUES
('tenant-1-uuid', '2024-05-15 12:01:00', 3, 'Connection Timeout', 'Failed to connect to the database'),
('tenant-2-uuid', '2024-05-15 12:05:00', 5, 'Memory Overflow', 'Exceeded memory limits during data processing');

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

-- Enable Row-Level Security (RLS) for all new tables
ALTER TABLE agent_data ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE error_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_interactions ENABLE ROW LEVEL SECURITY;

-- Create RLS policies for agent_data
CREATE POLICY "tenant_isolation" ON agent_data
FOR ALL
USING (tenant_id = current_setting('app.current_tenant')::uuid);

CREATE POLICY "Enable real-time" ON agent_data
FOR SELECT USING (true);

CREATE POLICY "agent_access" ON agent_data
FOR SELECT
USING (auth.uid() = user_id);

-- Create RLS policies for chat_history
CREATE POLICY "tenant_isolation" ON chat_history
FOR ALL
USING (tenant_id = current_setting('app.current_tenant')::uuid);

CREATE POLICY "Enable real-time" ON chat_history
FOR SELECT USING (true);

CREATE POLICY "chat_access" ON chat_history
FOR SELECT
USING (auth.uid() = user_id);

-- Create RLS policies for error_log
CREATE POLICY "tenant_isolation" ON error_log
FOR ALL
USING (tenant_id = current_setting('app.current_tenant')::uuid);

CREATE POLICY "Enable real-time" ON error_log
FOR SELECT USING (true);

CREATE POLICY "error_access" ON error_log
FOR SELECT
USING (auth.uid() = user_id);

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
CREATE INDEX idx_agent_data_tenant_id ON agent_data(tenant_id);
CREATE INDEX idx_chat_history_tenant_id ON chat_history(tenant_id);
CREATE INDEX idx_error_log_tenant_id ON error_log(tenant_id);
CREATE INDEX idx_agent_interactions_tenant_id ON agent_interactions(tenant_id);