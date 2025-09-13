# CI/CD Setup Guide

## GitHub Actions Automatic Deployment

This repository includes a GitHub Actions workflow that automatically tests and deploys the Django-React application when changes are pushed to the main branch.

### Workflow Overview

The CI/CD pipeline (`.github/workflows/ci-cd.yml`) includes:

1. **Testing Phase:**
   - Sets up Python 3.8 and Node.js 14
   - Installs dependencies for both backend and frontend
   - Runs Django tests with PostgreSQL
   - Builds the React frontend

2. **Build & Deploy Phase (only on main branch):**
   - Builds Docker containers using `docker-compose.prod.yml`
   - Performs basic health checks on the containers
   - Ready for deployment to production environment

### Setup Instructions

1. **Create Production Environment Files:**
   ```bash
   # Copy templates and edit with your secure values
   cp backend/.env.prod.template backend/.env.prod
   cp postgres/.env.prod.template postgres/.env.prod
   ```

2. **Configure Production Environment:**
   - Edit `backend/.env.prod` with secure SECRET_KEY, admin credentials, and database password
   - Edit `postgres/.env.prod` with matching database credentials
   - Update DJANGO_ALLOWED_HOSTS with your actual domain

3. **GitHub Secrets (if deploying to cloud):**
   Add these secrets to your GitHub repository settings:
   - `DOCKER_REGISTRY_URL` (if pushing to container registry)
   - `DOCKER_USERNAME` and `DOCKER_PASSWORD`
   - Cloud provider credentials as needed

### Local Testing

To test the production build locally:

```bash
# Create production env files from templates first
cp backend/.env.prod.template backend/.env.prod
cp postgres/.env.prod.template postgres/.env.prod

# Edit the files with secure values, then:
docker compose -f docker-compose.prod.yml up --build
```

### Adding Deployment Steps

To complete the deployment, add your specific deployment commands in the "Deploy notification" step of `.github/workflows/ci-cd.yml`. Examples:

- Push to Docker registry
- Deploy to AWS, GCP, Azure
- Update Kubernetes deployments
- Notify deployment status

The workflow ensures that deployment only happens when all tests pass successfully.