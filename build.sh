#!/usr/bin/env border-bash
# Exit immediately if a command exits with a non-zero status
set -o errexit

echo "🚀 Starting Production Build Pipeline..."

# 1. Install project dependencies
echo "📦 Installing requirements..."
pip install -r requirements.txt

# 2. Compile static assets using WhiteNoise settings
echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

# 3. Process structural database migrations
echo "🗄️ Running database migrations..."
python manage.py makemigrations
python manage.py migrate

echo "✅ Build Process Completed Successfully!"