#!/usr/bin/env bash
# exit on error
set -o errexit

echo "🚀 Starting Production Build Pipeline..."

# 1. Install required dependencies
echo "📦 Installing requirements from requirements.txt..."
pip install -r requirements.txt

# 2. Collect all static assets for WhiteNoise
echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

# 3. Create and apply database migrations for Zambia structures
echo "🗄️ Creating and running database migrations..."
python manage.py makemigrations
python manage.py migrate

echo "✅ Build pipeline finished successfully!"
