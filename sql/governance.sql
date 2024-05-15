-- Create the table for storing boundaries and constraints
CREATE TABLE boundaries (
    id SERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL,
    boundary_type VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial boundary data
INSERT INTO boundaries (tenant_id, boundary_type, description, status) VALUES
('tenant-1-uuid', 'Ethical', 'Ensure agents adhere to company values and principles', 'Active'),
('tenant-1-uuid', 'Legal', 'Comply with all relevant laws and regulations', 'Active'),
('tenant-2-uuid', 'Operational', 'Maintain service level agreements and uptime targets', 'Active'),
('tenant-2-uuid', 'Financial', 'Stay within allocated budgets and resource limits', 'Warning'),
('tenant-1-uuid', 'Reputational', 'Protect company brand and public image', 'Active');

-- Create the table for storing human feedback
CREATE TABLE human_feedback (
    id SERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL,
    agent VARCHAR(255) NOT NULL,
    task TEXT NOT NULL,
    feedback_type VARCHAR(255) NOT NULL,
    feedback_details TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial human feedback data
INSERT INTO human_feedback (tenant_id, agent, task, feedback_type, feedback_details) VALUES
('tenant-1-uuid', 'Sales AI', 'Generated product description', 'Approval', 'Great job, the description is accurate and compelling'),
('tenant-1-uuid', 'Support Bot', 'Handled customer complaint', 'Modification', 'The response was a bit too formal, try to be more empathetic'),
('tenant-2-uuid', 'Marketing Assistant', 'Created ad campaign', 'Clarification', 'What is the target audience for this campaign?'),
('tenant-2-uuid', 'Data Analyst', 'Provided sales forecast', 'Approval', 'The forecast looks solid, well done'),
('tenant-1-uuid', 'HR Coordinator', 'Sent onboarding email', 'Rejection', 'The email contains outdated information, please update');

-- Create the table for storing output reviews
CREATE TABLE output_reviews (
    id SERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL,
    output_type VARCHAR(255) NOT NULL,
    output_name TEXT NOT NULL,
    agent VARCHAR(255) NOT NULL,
    review_status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial output review data
INSERT INTO output_reviews (tenant_id, output_type, output_name, agent, review_status) VALUES
('tenant-1-uuid', 'Blog post', 'Top 10 AI Trends for 2025', 'Marketing Assistant', 'Pending'),
('tenant-1-uuid', 'Financial report', 'Q3 2024 Earnings Analysis', 'Data Analyst', 'Approved'),
('tenant-2-uuid', 'Product design', 'Smartwatch UI Mockups', 'Design AI', 'Rejected'),
('tenant-2-uuid', 'Customer email', 'Response to Billing Inquiry', 'Support Bot', 'Approved'),
('tenant-1-uuid', 'News article', 'Company Announces New AI Partnership', 'Content Creator', 'Pending');

-- Create the table for storing alerts and notifications
CREATE TABLE alerts (
    id SERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL,
    alert_type VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    urgency VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial alert data
INSERT INTO alerts (tenant_id, alert_type, description, urgency, status) VALUES
('tenant-1-uuid', 'Boundary Violation', 'Sales AI attempted to access restricted data', 'High', 'Unresolved'),
('tenant-1-uuid', 'Anomalous Behavior', 'Support Bot response time increased by 150%', 'Medium', 'Under Investigation'),
('tenant-2-uuid', 'System Error', 'Marketing Assistant encountered a memory leak', 'Critical', 'Resolved'),
('tenant-2-uuid', 'Human Feedback Required', 'Data Analyst report requires manager approval', 'Low', 'Pending'),
('tenant-1-uuid', 'Boundary Violation', 'HR Coordinator tried to modify employee records without authorization', 'High', 'Unresolved');

-- Enable Row-Level Security (RLS) for all governance tables
ALTER TABLE boundaries ENABLE ROW LEVEL SECURITY;
ALTER TABLE human_feedback ENABLE ROW LEVEL SECURITY;
ALTER TABLE output_reviews ENABLE ROW LEVEL SECURITY;
ALTER TABLE alerts ENABLE ROW LEVEL SECURITY;

-- Create RLS policies for boundaries
CREATE POLICY "tenant_isolation" ON boundaries
FOR ALL
USING (tenant_id = current_setting('app.current_tenant')::uuid);

CREATE POLICY "Enable real-time" ON boundaries
FOR SELECT USING (true);

CREATE POLICY "boundary_access" ON boundaries
FOR SELECT
USING (auth.uid() = user_id);

-- Create RLS policies for human_feedback
CREATE POLICY "tenant_isolation" ON human_feedback
FOR ALL
USING (tenant_id = current_setting('app.current_tenant')::uuid);

CREATE POLICY "Enable real-time" ON human_feedback
FOR SELECT USING (true);

CREATE POLICY "feedback_access" ON human_feedback
FOR SELECT
USING (auth.uid() = user_id);

-- Create RLS policies for output_reviews
CREATE POLICY "tenant_isolation" ON output_reviews
FOR ALL
USING (tenant_id = current_setting('app.current_tenant')::uuid);

CREATE POLICY "Enable real-time" ON output_reviews
FOR SELECT USING (true);

CREATE POLICY "review_access" ON output_reviews
FOR SELECT
USING (auth.uid() = user_id);

-- Create RLS policies for alerts
CREATE POLICY "tenant_isolation" ON alerts
FOR ALL
USING (tenant_id = current_setting('app.current_tenant')::uuid);

CREATE POLICY "Enable real-time" ON alerts
FOR SELECT USING (true);

CREATE POLICY "alert_access" ON alerts
FOR SELECT
USING (auth.uid() = user_id);

-- Create indexes for optimization
CREATE INDEX idx_boundaries_tenant_id ON boundaries(tenant_id);
CREATE INDEX idx_human_feedback_tenant_id ON human_feedback(tenant_id);
CREATE INDEX idx_output_reviews_tenant_id ON output_reviews(tenant_id);
CREATE INDEX idx_alerts_tenant_id ON alerts(tenant_id);