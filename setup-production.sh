#!/bin/bash

echo "🚀 Setting up production environment for Django-React app..."

# Check if production env files already exist
if [ -f "backend/.env.prod" ] || [ -f "postgres/.env.prod" ]; then
    echo "⚠️  Production environment files already exist."
    read -p "Do you want to overwrite them? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled."
        exit 1
    fi
fi

# Copy template files
echo "📋 Copying environment templates..."
cp backend/.env.prod.template backend/.env.prod
cp postgres/.env.prod.template postgres/.env.prod

# Generate a secure secret key
echo "🔐 Generating secure Django secret key..."
SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')

# Generate secure passwords
echo "🔒 Generating secure passwords..."
DB_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-25)
ADMIN_PASSWORD=$(openssl rand -base64 16 | tr -d "=+/" | cut -c1-12)

# Update backend/.env.prod
sed -i "s/YOUR_SECRET_KEY_HERE_CHANGE_THIS/$SECRET_KEY/" backend/.env.prod
sed -i "s/YOUR_SECURE_DB_PASSWORD/$DB_PASSWORD/" backend/.env.prod
sed -i "s/YOUR_SECURE_ADMIN_PASSWORD/$ADMIN_PASSWORD/" backend/.env.prod

# Update postgres/.env.prod
sed -i "s/YOUR_SECURE_DB_PASSWORD/$DB_PASSWORD/" postgres/.env.prod

echo "✅ Production environment setup complete!"
echo ""
echo "📝 Important next steps:"
echo "1. Edit backend/.env.prod to update:"
echo "   - DJANGO_ALLOWED_HOSTS with your domain"
echo "   - DJANGO_ADMIN_EMAIL with your email"
echo ""
echo "2. Your generated admin credentials:"
echo "   - Username: admin"
echo "   - Password: $ADMIN_PASSWORD"
echo "   - Email: (update in backend/.env.prod)"
echo ""
echo "3. Test production build:"
echo "   docker compose -f docker-compose.prod.yml up --build"
echo ""
echo "🔐 Keep your environment files secure and never commit them to git!"