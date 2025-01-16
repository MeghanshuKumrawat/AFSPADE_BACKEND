#!/bin/bash

echo "Starting build process..."

# Step 1: Install Python dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo "Dependencies installed successfully."
else
    echo "Failed to install dependencies." >&2
    exit 1
fi

# Step 2: Run migrations
echo "Running database migrations..."
python3 manage.py migrate
if [ $? -eq 0 ]; then
    echo "Database migrations completed successfully."
else
    echo "Failed to run database migrations." >&2
    exit 1
fi

# Step 3: Collect static files
echo "Collecting static files..."
python3 manage.py collectstatic --noinput
if [ $? -eq 0 ]; then
    echo "Static files collected successfully."
else
    echo "Failed to collect static files." >&2
    exit 1
fi

# Step 4: (Optional) Create admin user
echo "Creating admin user..."
python3 manage.py create_admin
if [ $? -eq 0 ]; then
    echo "Admin user created successfully."
else
    echo "Failed to create admin user. This step is optional; continuing..." >&2
fi

echo "Build process completed."
