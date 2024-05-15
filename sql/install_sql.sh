#!/bin/bash

# Load environment variables
source .env

# Check if environment variables are set
if [ -z "$SUPABASE_URL" ] || [ -z "$SUPABASE_DB" ] || [ -z "$SUPABASE_USER" ] || [ -z "$SUPABASE_PASSWORD" ]; then
  echo "Please set the SUPABASE_URL, SUPABASE_DB, SUPABASE_USER, and SUPABASE_PASSWORD environment variables in the .env file."
  exit 1
fi

# Function to execute a SQL file
execute_sql() {
  local file=$1
  echo "Executing $file..."
  PGPASSWORD=$SUPABASE_PASSWORD psql -h $SUPABASE_URL -d $SUPABASE_DB -U $SUPABASE_USER -f $file
  if [ $? -eq 0 ]; then
    echo "$file executed successfully."
  else
    echo "Error executing $file."
    exit 1
  fi
}

# List of SQL files to be executed
sql_files=(
  "agent_data.sql"
  "agent_interaction.sql"
  "analytics_reporting.sql"
  "chat_history_agent_details.sql"
  "command_control.sql"
  "documentation.sql"
  "governance.sql"
  "system_settings.sql"
  "users_agents.sql"
)

# Execute each SQL file
for sql_file in "${sql_files[@]}"; do
  if [ -f "$sql_file" ]; then
    execute_sql "$sql_file"
  else
    echo "File $sql_file does not exist."
    exit 1
  fi
done

echo "All SQL files executed successfully."
