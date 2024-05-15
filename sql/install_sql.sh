#!/bin/bash

# Check if psql is installed
if ! command -v psql &> /dev/null; then
  echo "psql could not be found. Installing it now..."

  # Check OS and install psql accordingly
  if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sudo apt update
    sudo apt install postgresql-client -y
  elif [[ "$OSTYPE" == "darwin"* ]]; then
    brew install postgresql
  elif [[ "$OSTYPE" == "msys" ]]; then
    echo "Please install psql manually from: https://www.postgresql.org/download/windows/"
    exit 1
  else
    echo "Unsupported OS. Please install psql manually."
    exit 1
  fi
fi

# Load environment variables
if [ -f ".env" ]; then
  source .env
else
  echo ".env file not found. Please create one with your Supabase configuration."
  exit 1
fi

# Prompt for environment variables if not set
if [ -z "$SUPABASE_URL" ]; then
  read -p "Enter your Supabase URL: " SUPABASE_URL
fi

if [ -z "$SUPABASE_DB" ]; then
  read -p "Enter your Supabase database name: " SUPABASE_DB
fi

if [ -z "$SUPABASE_USER" ]; then
  read -p "Enter your Supabase username: " SUPABASE_USER
fi

if [ -z "$SUPABASE_PASSWORD" ]; then
  read -s -p "Enter your Supabase password: " SUPABASE_PASSWORD
  echo
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
