-- Create the table for storing agent metrics over time
CREATE TABLE agent_metrics (
    id SERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL,
    date DATE NOT NULL,
    total_agents INT NOT NULL,
    active_agents INT NOT NULL,
    tasks_completed INT NOT NULL,
    avg_rating FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data into agent_metrics table
INSERT INTO agent_metrics (tenant_id, date, total_agents, active_agents, tasks_completed, avg_rating) VALUES
('00000000-0000-0000-0000-000000000001', '2023-01-01', 500, 375, 8000, 4.5),
('00000000-0000-0000-0000-000000000001', '2023-01-08', 525, 395, 8500, 4.52),
('00000000-0000-0000-0000-000000000001', '2023-01-15', 540, 410, 9200, 4.54),
('00000000-0000-0000-0000-000000000001', '2023-01-22', 560, 430, 9800, 4.56),
('00000000-0000-0000-0000-000000000001', '2023-01-29', 575, 445, 10400, 4.58),
('00000000-0000-0000-0000-000000000002', '2023-02-05', 590, 460, 11000, 4.6),
('00000000-0000-0000-0000-000000000002', '2023-02-12', 600, 475, 11600, 4.62),
('00000000-0000-0000-0000-000000000002', '2023-02-19', 615, 490, 12200, 4.64),
('00000000-0000-0000-0000-000000000002', '2023-02-26', 630, 505, 12800, 4.66),
('00000000-0000-0000-0000-000000000002', '2023-03-05', 645, 520, 13400, 4.68),
('00000000-0000-0000-0000-000000000001', '2023-03-12', 660, 535, 14000, 4.7),
('00000000-0000-0000-0000-000000000001', '2023-03-19', 675, 550, 14600, 4.72),
('00000000-0000-0000-0000-000000000001', '2023-03-26', 690, 565, 15200, 4.74),
('00000000-0000-0000-0000-000000000001', '2023-04-02', 700, 580, 15800, 4.76),
('00000000-0000-0000-0000-000000000001', '2023-04-09', 710, 595, 16400, 4.78);

-- Create the table for storing agent team performance
CREATE TABLE agent_teams (
    id SERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL,
    team VARCHAR(255) NOT NULL,
    agents INT NOT NULL,
    tasks INT NOT NULL,
    avg_rating FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data into agent_teams table
INSERT INTO agent_teams (tenant_id, team, agents, tasks, avg_rating) VALUES
('00000000-0000-0000-0000-000000000001', 'Sales', 120, 3200, 4.7),
('00000000-0000-0000-0000-000000000001', 'Support', 180, 4800, 4.75),
('00000000-0000-0000-0000-000000000001', 'Marketing', 95, 2400, 4.65),
('00000000-0000-0000-0000-000000000002', 'Analytics', 65, 1600, 4.8),
('00000000-0000-0000-0000-000000000002', 'HR', 40, 800, 4.72);

-- Create the table for storing custom reports
CREATE TABLE custom_reports (
    id SERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL,
    report_type VARCHAR(255) NOT NULL,
    report_period VARCHAR(255) NOT NULL,
    start_date DATE,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the table for storing forecast data
CREATE TABLE forecast_data (
    id SERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL,
    metric VARCHAR(255) NOT NULL,
    period VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    value INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Enable Row-Level Security (RLS) for all analytics reporting tables
ALTER TABLE agent_metrics ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_teams ENABLE ROW LEVEL SECURITY;
ALTER TABLE custom_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE forecast_data ENABLE ROW LEVEL SECURITY;

-- Create RLS policies for agent_metrics
CREATE POLICY "tenant_isolation" ON agent_metrics
FOR ALL
USING (tenant_id = current_setting('app.current_tenant')::uuid);

CREATE POLICY "Enable real-time" ON agent_metrics
FOR SELECT USING (true);

CREATE POLICY "metrics_access" ON agent_metrics
FOR SELECT
USING (tenant_id = current_setting('app.current_tenant')::uuid);

-- Create RLS policies for agent_teams
CREATE POLICY "tenant_isolation" ON agent_teams
FOR ALL
USING (tenant_id = current_setting('app.current_tenant')::uuid);

CREATE POLICY "Enable real-time" ON agent_teams
FOR SELECT USING (true);

CREATE POLICY "teams_access" ON agent_teams
FOR SELECT
USING (tenant_id = current_setting('app.current_tenant')::uuid);

-- Create RLS policies for custom_reports
CREATE POLICY "tenant_isolation" ON custom_reports
FOR ALL
USING (tenant_id = current_setting('app.current_tenant')::uuid);

CREATE POLICY "Enable real-time" ON custom_reports
FOR SELECT USING (true);

CREATE POLICY "reports_access" ON custom_reports
FOR SELECT
USING (tenant_id = current_setting('app.current_tenant')::uuid);

-- Create RLS policies for forecast_data
CREATE POLICY "tenant_isolation" ON forecast_data
FOR ALL
USING (tenant_id = current_setting('app.current_tenant')::uuid);

CREATE POLICY "Enable real-time" ON forecast_data
FOR SELECT USING (true);

CREATE POLICY "forecast_access" ON forecast_data
FOR SELECT
USING (tenant_id = current_setting('app.current_tenant')::uuid);

-- Create indexes for optimization
CREATE INDEX idx_agent_metrics_tenant_id ON agent_metrics(tenant_id);
CREATE INDEX idx_agent_teams_tenant_id ON agent_teams(tenant_id);
CREATE INDEX idx_custom_reports_tenant_id ON custom_reports(tenant_id);
CREATE INDEX idx_forecast_data_tenant_id ON forecast_data(tenant_id);