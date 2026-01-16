# CI/CD Pipeline

> **What you'll create:** Build a complete CI/CD pipeline with GitHub Actions that tests, builds, and deploys your application automatically.

---

## Quick Start

```bash
# 1. Fork and clone this repo

# 2. Complete the workflow file in .github/workflows/

# 3. Push and watch the magic!
git push origin main
# → Check GitHub Actions tab!
```

---

## What is This Challenge?

Every time you push code, you want:
- ✅ Tests to run automatically
- ✅ Code quality checks
- ✅ Docker image built
- ✅ Application deployed (to staging/production)

**CI/CD** (Continuous Integration / Continuous Deployment) automates all of this!

---

## Do I Need Prior Knowledge?

**You need:**
- ✅ Basic Git commands (commit, push, pull)
- ✅ Understanding of what tests are
- ✅ Basic YAML syntax (you'll learn as you go)

**You'll learn:**
- What CI/CD means and why it matters
- How GitHub Actions works
- Writing workflow files
- Running tests automatically
- Building Docker images in CI
- Deployment strategies

---

## What You'll Build

| File | What You Create | Points |
|------|-----------------|--------|
| `.github/workflows/ci.yml` | Test & lint workflow | 25 |
| `.github/workflows/build.yml` | Docker build workflow | 25 |
| `.github/workflows/deploy.yml` | Deployment workflow | 25 |
| Branch protection | PR-based workflow | 10 |
| Secrets management | Secure credentials | 15 |

---

## Step 0: Understand CI/CD

> ⏱️ **Time:** 15 minutes (reading)

### What is CI/CD?

**CI (Continuous Integration):**
- Automatically run tests when code is pushed
- Catch bugs before they reach production
- Ensure code quality with linting

**CD (Continuous Deployment/Delivery):**
- Automatically deploy code after tests pass
- Delivery = deploy to staging, manual prod deploy
- Deployment = fully automatic to production

### The CI/CD Flow

```
Developer pushes code
        │
        ▼
┌───────────────────┐
│   CI Pipeline     │
│  ┌─────────────┐  │
│  │ Install deps│  │
│  └──────┬──────┘  │
│         ▼         │
│  ┌─────────────┐  │
│  │  Run tests  │  │
│  └──────┬──────┘  │
│         ▼         │
│  ┌─────────────┐  │
│  │  Lint code  │  │
│  └──────┬──────┘  │
└─────────┼─────────┘
          │ All passed?
          ▼
┌───────────────────┐
│   CD Pipeline     │
│  ┌─────────────┐  │
│  │ Build image │  │
│  └──────┬──────┘  │
│         ▼         │
│  ┌─────────────┐  │
│  │ Push to     │  │
│  │ registry    │  │
│  └──────┬──────┘  │
│         ▼         │
│  ┌─────────────┐  │
│  │   Deploy    │  │
│  └─────────────┘  │
└───────────────────┘
```

### Why CI/CD Matters

```
Without CI/CD:
"Did you run the tests?" → "I think so..."
"Is this safe to deploy?" → "Let me check manually..."
"Who broke production?" → "Not me!"

With CI/CD:
Tests run automatically → No guessing
Deployment is automated → Consistent every time
Everything is logged → Clear audit trail
```

---

## Step 1: Create Your First Workflow

> ⏱️ **Time:** 30-40 minutes

### How GitHub Actions Works

GitHub Actions uses **workflow files** (YAML) in `.github/workflows/`:

```yaml
name: My Workflow           # Name shown in GitHub UI

on:                         # When to run
  push:
    branches: [main]

jobs:                       # What to do
  my-job:
    runs-on: ubuntu-latest  # What machine to use
    steps:                  # The actual work
      - name: Step 1
        run: echo "Hello!"
```

### Your Task

Create `.github/workflows/ci.yml`:

**Requirements:**
- [ ] Trigger on push to main and on pull requests
- [ ] Install Python and dependencies
- [ ] Run the test suite
- [ ] Run linting (flake8 or ruff)

### Step-by-Step Guide

<details>
<summary>💡 Hint 1: Basic Structure</summary>

```yaml
name: CI Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest flake8
```

</details>

<details>
<summary>💡 Hint 2: Running Tests</summary>

```yaml
      - name: Run tests
        run: pytest tests/ -v

      - name: Run linter
        run: flake8 src/ --max-line-length=100
```

</details>

<details>
<summary>💡 Hint 3: Caching Dependencies</summary>

Speed up your workflow with caching:

```yaml
      - name: Cache pip packages
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-
```

</details>

<details>
<summary>🎯 Full Solution</summary>

```yaml
name: CI Pipeline

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

jobs:
  test:
    name: Test & Lint
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Cache pip packages
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest flake8 pytest-cov

      - name: Run linter
        run: |
          flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics
          flake8 src/ --count --exit-zero --max-line-length=100 --statistics

      - name: Run tests with coverage
        run: |
          pytest tests/ -v --cov=src --cov-report=term-missing

      - name: Upload coverage report
        uses: actions/upload-artifact@v3
        with:
          name: coverage-report
          path: .coverage
```

</details>

---

## Step 2: Build Docker Images

> ⏱️ **Time:** 25-30 minutes

### Why Build in CI?

- Consistent builds (same environment every time)
- Automatic versioning with git tags/commits
- Push to registry for deployment

### Your Task

Create `.github/workflows/build.yml`:

**Requirements:**
- [ ] Only run after tests pass
- [ ] Build Docker image
- [ ] Tag with commit SHA and 'latest'
- [ ] Push to GitHub Container Registry (ghcr.io)

<details>
<summary>💡 Hint 1: Workflow Dependencies</summary>

You can make one workflow depend on another:

```yaml
name: Build

on:
  workflow_run:
    workflows: ["CI Pipeline"]
    types: [completed]
    branches: [main]
```

Or trigger on the same events but run sequentially:

```yaml
on:
  push:
    branches: [main]

jobs:
  test:
    # ... test steps ...

  build:
    needs: test  # Only runs after test job succeeds
    # ... build steps ...
```

</details>

<details>
<summary>💡 Hint 2: Docker Build Action</summary>

```yaml
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ghcr.io/${{ github.repository }}:latest
            ghcr.io/${{ github.repository }}:${{ github.sha }}
```

</details>

<details>
<summary>🎯 Full Solution</summary>

```yaml
name: Build & Push Docker Image

on:
  push:
    branches: [main, master]
    tags: ['v*']

jobs:
  test:
    name: Run Tests First
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install and test
        run: |
          pip install -r requirements.txt pytest
          pytest tests/ -v

  build:
    name: Build Docker Image
    runs-on: ubuntu-latest
    needs: test  # Only run after tests pass
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ghcr.io/${{ github.repository }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=sha,prefix=
            type=raw,value=latest,enable=${{ github.ref == 'refs/heads/main' }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Image digest
        run: echo "Image pushed with digest ${{ steps.build.outputs.digest }}"
```

</details>

---

## Step 3: Deploy Automatically

> ⏱️ **Time:** 30-40 minutes

### Deployment Strategies

| Strategy | How It Works | Use Case |
|----------|--------------|----------|
| **Rolling** | Replace instances one by one | Zero downtime |
| **Blue-Green** | Switch traffic between two environments | Instant rollback |
| **Canary** | Route small % to new version | Test in production |

### Your Task

Create `.github/workflows/deploy.yml`:

**Requirements:**
- [ ] Deploy to staging on push to main
- [ ] Deploy to production on release/tag
- [ ] Use environment secrets
- [ ] Include deployment verification

<details>
<summary>💡 Hint 1: GitHub Environments</summary>

GitHub Environments let you:
- Require approvals before deploy
- Have different secrets per environment
- See deployment history

```yaml
jobs:
  deploy-staging:
    environment: staging
    # ...

  deploy-production:
    environment: production
    # Requires approval if configured in repo settings
```

</details>

<details>
<summary>💡 Hint 2: Conditional Deployment</summary>

```yaml
jobs:
  deploy-staging:
    if: github.ref == 'refs/heads/main'
    # ...

  deploy-production:
    if: startsWith(github.ref, 'refs/tags/v')
    # ...
```

</details>

<details>
<summary>🎯 Full Solution</summary>

```yaml
name: Deploy

on:
  push:
    branches: [main]
  release:
    types: [published]

jobs:
  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment:
      name: staging
      url: https://staging.example.com

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Deploy to staging
        run: |
          echo "🚀 Deploying to staging..."
          echo "Image: ghcr.io/${{ github.repository }}:${{ github.sha }}"
          # In real scenario, use kubectl, ssh, or cloud CLI
          # kubectl set image deployment/myapp app=ghcr.io/${{ github.repository }}:${{ github.sha }}

      - name: Verify deployment
        run: |
          echo "✓ Verifying deployment health..."
          # curl -f https://staging.example.com/health || exit 1

      - name: Notify on success
        if: success()
        run: echo "✅ Staging deployment successful!"

      - name: Notify on failure
        if: failure()
        run: echo "❌ Staging deployment failed!"

  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    if: github.event_name == 'release'
    environment:
      name: production
      url: https://example.com

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Deploy to production
        run: |
          echo "🚀 Deploying to production..."
          echo "Release: ${{ github.event.release.tag_name }}"
          echo "Image: ghcr.io/${{ github.repository }}:${{ github.event.release.tag_name }}"

      - name: Run smoke tests
        run: |
          echo "🔍 Running smoke tests..."
          # curl -f https://example.com/health
          # curl -f https://example.com/api/status

      - name: Create deployment record
        run: |
          echo "📝 Recording deployment..."
          echo "Version: ${{ github.event.release.tag_name }}"
          echo "Time: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
          echo "Commit: ${{ github.sha }}"
```

</details>

---

## Step 4: Secrets Management

> ⏱️ **Time:** 15-20 minutes

### What Are Secrets?

Secrets are sensitive values like:
- API keys
- Database passwords
- Cloud credentials
- SSH keys

**NEVER** put secrets in code. Use GitHub Secrets!

### Setting Up Secrets

1. Go to your repo on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add your secrets

### Using Secrets in Workflows

```yaml
steps:
  - name: Deploy with credentials
    env:
      API_KEY: ${{ secrets.API_KEY }}
      DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
    run: |
      echo "Deploying with secure credentials..."
      # Secrets are masked in logs
```

### Your Task

Add secrets handling to your workflows:

- [ ] Add a `DEPLOY_TOKEN` secret usage
- [ ] Use environment-specific secrets
- [ ] Verify secrets aren't logged

---

## Step 5: Branch Protection

> ⏱️ **Time:** 10-15 minutes

### Why Branch Protection?

Prevent pushing directly to main:
- Force code review via PRs
- Require CI to pass
- Maintain code quality

### Setup Branch Protection

1. Go to **Settings** → **Branches**
2. Click **Add branch protection rule**
3. Branch name pattern: `main`
4. Enable:
   - ✅ Require a pull request before merging
   - ✅ Require status checks to pass
   - ✅ Require branches to be up to date

### The PR Workflow

```
1. Create feature branch
   git checkout -b feature/my-feature

2. Make changes and push
   git add . && git commit -m "Add feature"
   git push origin feature/my-feature

3. Open Pull Request on GitHub
   → CI runs automatically
   → Request review

4. After approval and CI passes
   → Merge to main
   → CD deploys automatically
```

---

## Step 6: Test Your Pipeline

### Local Testing

```bash
# Run the progress checker
python run.py
```

**Expected output when complete:**
```
============================================================
  🚀 CI/CD Pipeline Challenge
============================================================

  ✅ CI Workflow (25/25 points)
  ✅ Build Workflow (25/25 points)
  ✅ Deploy Workflow (25/25 points)
  ✅ PR Workflow (25/25 points)

============================================================
  🎯 Total Score: 100/100
  🎉 CHALLENGE COMPLETE!
============================================================
```

**If you see less than 100:**
- Read the missing items (marked with ✗)
- Check the corresponding step in this README
- Fix your workflow files and run again

```bash
# Verify YAML syntax
python -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"
```

### Push and Watch

```bash
git add .
git commit -m "Add CI/CD pipeline"
git push origin main

# Go to GitHub → Actions tab → Watch it run!
```

### Trigger Different Workflows

```bash
# Test CI (push to main)
git push origin main

# Test build (push tag)
git tag v1.0.0
git push origin v1.0.0

# Test PR workflow
git checkout -b test-pr
echo "test" >> test.txt
git add . && git commit -m "Test PR"
git push origin test-pr
# → Create PR on GitHub
```

---

## Understanding the Workflow (For DevOps Students)

### Workflow Anatomy

```yaml
name: CI Pipeline                    # ← Display name in GitHub UI

on:                                  # ← TRIGGER: When does this run?
  push:
    branches: [main]                 # Push to main branch
  pull_request:
    branches: [main]                 # PR targeting main
  workflow_dispatch:                 # Manual trigger button

env:                                 # ← GLOBAL VARIABLES
  PYTHON_VERSION: '3.11'

jobs:                                # ← JOBS: Groups of steps
  test:                              # Job ID (unique name)
    name: Run Tests                  # Display name
    runs-on: ubuntu-latest           # VM type

    steps:                           # ← STEPS: Individual commands
      - uses: actions/checkout@v4    # Pre-built action
      - name: Custom step            # Custom command
        run: echo "Hello"

  build:
    needs: test                      # ← DEPENDENCY: Run after 'test'
    runs-on: ubuntu-latest
    # ...
```

### Key Concepts

| Concept | What It Is | Example |
|---------|-----------|---------|
| **Workflow** | YAML file defining automation | `.github/workflows/ci.yml` |
| **Trigger** | Event that starts workflow | `push`, `pull_request`, `schedule` |
| **Job** | Group of steps on same runner | `test`, `build`, `deploy` |
| **Step** | Individual command or action | `run: pytest` |
| **Action** | Reusable workflow component | `actions/checkout@v4` |
| **Runner** | VM that executes the job | `ubuntu-latest` |
| **Artifact** | Files saved between jobs | Test reports, build outputs |
| **Secret** | Encrypted variable | API keys, passwords |

### Useful Actions

```yaml
# Checkout code
- uses: actions/checkout@v4

# Setup languages
- uses: actions/setup-python@v5
- uses: actions/setup-node@v4
- uses: actions/setup-go@v5

# Caching
- uses: actions/cache@v3

# Upload/download artifacts
- uses: actions/upload-artifact@v3
- uses: actions/download-artifact@v3

# Docker
- uses: docker/setup-buildx-action@v3
- uses: docker/build-push-action@v5
- uses: docker/login-action@v3
```

### What You Can Say in Interviews

> "I built a complete CI/CD pipeline using GitHub Actions. The CI workflow runs tests and linting on every push and PR, with dependency caching for speed. The CD pipeline builds Docker images and pushes to GitHub Container Registry, then deploys to staging automatically and production on release. I implemented branch protection rules requiring PR reviews and passing CI checks before merging."

---

## Troubleshooting

<details>
<summary>❌ Workflow not running</summary>

1. Check file location: Must be in `.github/workflows/`
2. Check YAML syntax: No tabs, proper indentation
3. Check trigger: Does the event match?

```bash
# Validate YAML
python -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"
```

</details>

<details>
<summary>❌ Permission denied for packages</summary>

Add permissions to your workflow:

```yaml
jobs:
  build:
    permissions:
      contents: read
      packages: write
```

</details>

<details>
<summary>❌ Secret not found</summary>

1. Check secret name matches exactly (case-sensitive)
2. Check secret is set at right level (repo vs environment)
3. For forks, secrets aren't available by default

</details>

<details>
<summary>❌ Docker build fails</summary>

1. Check Dockerfile exists
2. Check context path is correct
3. Check you're logged in to registry

```yaml
- uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}
```

</details>

---

## What You Learned

- ✅ **CI/CD concepts** - Continuous Integration and Deployment
- ✅ **GitHub Actions** - Workflows, jobs, steps, triggers
- ✅ **Automated testing** - Run tests on every push
- ✅ **Docker in CI** - Build and push images automatically
- ✅ **Deployment pipelines** - Staging and production
- ✅ **Secrets management** - Secure credential handling
- ✅ **Branch protection** - Enforce code quality

---

## Next Steps

- **2.3 Kubernetes Basics** - Where your containers actually run
- **3.1 Monitoring Stack** - Watch your deployments in production

Good luck! 🚀
