-- Create the table for storing agent parameters
CREATE TABLE agent_parameters (
    id SERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL,
    default_learning_rate FLOAT NOT NULL,
    default_exploration_rate FLOAT NOT NULL,
    agent_types TEXT[] NOT NULL,
    agent_specializations TEXT[] NOT NULL,
    reward_structure VARCHAR(50) NOT NULL,
    max_tokens INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial agent parameters data
INSERT INTO agent_parameters (tenant_id, default_learning_rate, default_exploration_rate, agent_types, agent_specializations, reward_structure, max_tokens) VALUES
('00000000-0000-0000-0000-000000000001', 0.1, 0.1, ARRAY['Conversational', 'Retrieval-based'], ARRAY['Sales', 'Support'], 'Fixed', 512);

-- Create the table for storing resource management settings
CREATE TABLE resource_management (
    id SERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL,
    max_compute_usage INT NOT NULL,
    max_storage_usage INT NOT NULL,
    cost_per_compute_hour FLOAT NOT NULL,
    cost_per_gb_storage FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial resource management data
INSERT INTO resource_management (tenant_id, max_compute_usage, max_storage_usage, cost_per_compute_hour, cost_per_gb_storage) VALUES
('00000000-0000-0000-0000-000000000001', 10000, 1000, 0.05, 0.02);

-- Create the table for storing access and permissions settings
CREATE TABLE access_permissions (
    id SERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL,
    user_roles TEXT[] NOT NULL,
    enable_api_access BOOLEAN NOT NULL,
    api_rate_limit INT NOT NULL,
    enable_logging BOOLEAN NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial access and permissions data
INSERT INTO access_permissions (tenant_id, user_roles, enable_api_access, api_rate_limit, enable_logging) VALUES
('00000000-0000-0000-0000-000000000001', ARRAY['Administrator', 'Developer'], TRUE, 1000, TRUE);

-- Enable Row-Level Security (RLS) for all system settings tables
ALTER TABLE agent_parameters ENABLE ROW LEVEL SECURITY;
ALTER TABLE resource_management ENABLE ROW LEVEL SECURITY;
ALTER TABLE access_permissions ENABLE ROW LEVEL SECURITY;

-- Create RLS policies for agent_parameters
CREATE POLICY "tenant_isolation" ON agent_parameters
FOR ALL
USING (tenant_id = current_setting('app.current_tenant')::uuid);

CREATE POLICY "Enable real-time" ON agent_parameters
FOR SELECT USING (true);

CREATE POLICY "parameters_access" ON agent_parameters
FOR SELECT
USING (tenant_id = current_setting('app.current_tenant')::uuid);

-- Create RLS policies for resource_management
CREATE POLICY "tenant_isolation" ON resource_management
FOR ALL
USING (tenant_id = current_setting('app.current_tenant')::uuid);

CREATE POLICY "Enable real-time" ON resource_management
FOR SELECT USING (true);

CREATE POLICY "resource_access" ON resource_management
FOR SELECT
USING (tenant_id = current_setting('app.current_tenant')::uuid);

-- Create RLS policies for access_permissions
CREATE POLICY "tenant_isolation" ON access_permissions
FOR ALL
USING (tenant_id = current_setting('app.current_tenant')::uuid);

CREATE POLICY "Enable real-time" ON access_permissions
FOR SELECT USING (true);

CREATE POLICY "permissions_access" ON access_permissions
FOR SELECT
USING (tenant_id = current_setting('app.current_tenant')::uuid);

-- Create indexes for optimization
CREATE INDEX idx_agent_parameters_tenant_id ON agent_parameters(tenant_id);
CREATE INDEX idx_resource_management_tenant_id ON resource_management(tenant_id);
CREATE INDEX idx_access_permissions_tenant_id ON access_permissions(tenant_id);