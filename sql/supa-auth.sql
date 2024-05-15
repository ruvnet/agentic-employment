-- Enable Row-Level Security for all tables
ALTER TABLE auth.audit_log_entries ENABLE ROW LEVEL SECURITY;
ALTER TABLE auth.flow_state ENABLE ROW LEVEL SECURITY;
ALTER TABLE auth.identities ENABLE ROW LEVEL SECURITY;
ALTER TABLE auth.instances ENABLE ROW LEVEL SECURITY;
ALTER TABLE auth.mfa_amr_claims ENABLE ROW LEVEL SECURITY;
ALTER TABLE auth.mfa_challenges ENABLE ROW LEVEL SECURITY;
ALTER TABLE auth.mfa_factors ENABLE ROW LEVEL SECURITY;
ALTER TABLE auth.one_time_tokens ENABLE ROW LEVEL SECURITY;
ALTER TABLE auth.refresh_tokens ENABLE ROW LEVEL SECURITY;
ALTER TABLE auth.saml_providers ENABLE ROW LEVEL SECURITY;
ALTER TABLE auth.saml_relay_states ENABLE ROW LEVEL SECURITY;
ALTER TABLE auth.schema_migrations ENABLE ROW LEVEL SECURITY;
ALTER TABLE auth.sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE auth.sso_domains ENABLE ROW LEVEL SECURITY;
ALTER TABLE auth.sso_providers ENABLE ROW LEVEL SECURITY;
ALTER TABLE auth.users ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if they exist
DROP POLICY IF EXISTS "Allow logged-in users to access their own audit log entries" ON auth.audit_log_entries;
DROP POLICY IF EXISTS "Enable real-time" ON auth.audit_log_entries;
DROP POLICY IF EXISTS "Enable real-time" ON auth.flow_state;
DROP POLICY IF EXISTS "Enable real-time" ON auth.identities;
DROP POLICY IF EXISTS "Enable real-time" ON auth.instances;
DROP POLICY IF EXISTS "Enable real-time" ON auth.mfa_amr_claims;
DROP POLICY IF EXISTS "Enable real-time" ON auth.mfa_challenges;
DROP POLICY IF EXISTS "Enable real-time" ON auth.mfa_factors;
DROP POLICY IF EXISTS "Enable real-time" ON auth.one_time_tokens;
DROP POLICY IF EXISTS "Enable real-time" ON auth.refresh_tokens;
DROP POLICY IF EXISTS "Enable real-time" ON auth.saml_providers;
DROP POLICY IF EXISTS "Enable real-time" ON auth.saml_relay_states;
DROP POLICY IF EXISTS "Enable real-time" ON auth.schema_migrations;
DROP POLICY IF EXISTS "Enable real-time" ON auth.sso_domains;
DROP POLICY IF EXISTS "Enable real-time" ON auth.sso_providers;
DROP POLICY IF EXISTS "Allow logged-in users to access their own sessions" ON auth.sessions;
DROP POLICY IF EXISTS "Enable real-time" ON auth.sessions;
DROP POLICY IF EXISTS "Allow logged-in users to access their own data" ON auth.users;
DROP POLICY IF EXISTS "Enable real-time" ON auth.users;

-- Create policies for auth.audit_log_entries
CREATE POLICY "Allow logged-in users to access their own audit log entries" ON auth.audit_log_entries
FOR SELECT
USING (auth.uid() = id);

CREATE POLICY "Enable real-time" ON auth.audit_log_entries
FOR SELECT USING (true);

-- Create policies for auth.flow_state
CREATE POLICY "Enable real-time" ON auth.flow_state
FOR SELECT USING (true);

-- Create policies for auth.identities
CREATE POLICY "Enable real-time" ON auth.identities
FOR SELECT USING (true);

-- Create policies for auth.instances
CREATE POLICY "Enable real-time" ON auth.instances
FOR SELECT USING (true);

-- Create policies for auth.mfa_amr_claims
CREATE POLICY "Enable real-time" ON auth.mfa_amr_claims
FOR SELECT USING (true);

-- Create policies for auth.mfa_challenges
CREATE POLICY "Enable real-time" ON auth.mfa_challenges
FOR SELECT USING (true);

-- Create policies for auth.mfa_factors
CREATE POLICY "Enable real-time" ON auth.mfa_factors
FOR SELECT USING (true);

-- Create policies for auth.one_time_tokens
CREATE POLICY "Enable real-time" ON auth.one_time_tokens
FOR SELECT USING (true);

-- Create policies for auth.refresh_tokens
CREATE POLICY "Enable real-time" ON auth.refresh_tokens
FOR SELECT USING (true);

-- Create policies for auth.saml_providers
CREATE POLICY "Enable real-time" ON auth.saml_providers
FOR SELECT USING (true);

-- Create policies for auth.saml_relay_states
CREATE POLICY "Enable real-time" ON auth.saml_relay_states
FOR SELECT USING (true);

-- Create policies for auth.schema_migrations
CREATE POLICY "Enable real-time" ON auth.schema_migrations
FOR SELECT USING (true);

-- Create policies for auth.sso_domains
CREATE POLICY "Enable real-time" ON auth.sso_domains
FOR SELECT USING (true);

-- Create policies for auth.sso_providers
CREATE POLICY "Enable real-time" ON auth.sso_providers
FOR SELECT USING (true);

-- Create policies for auth.sessions
CREATE POLICY "Allow logged-in users to access their own sessions" ON auth.sessions
FOR SELECT
USING (auth.uid() = id);

CREATE POLICY "Enable real-time" ON auth.sessions
FOR SELECT USING (true);

-- Create policies for auth.users
CREATE POLICY "Allow logged-in users to access their own data" ON auth.users
FOR SELECT
USING (auth.uid() = id);

CREATE POLICY "Enable real-time" ON auth.users
FOR SELECT USING (true);
