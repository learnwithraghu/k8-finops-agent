# AWS Credentials Setup for Section 09

**IMPORTANT: Never store AWS credentials in `.env` or any file committed to git.**

This guide shows you how to configure AWS credentials **locally on your machine** for the Bedrock agent.

## Why Not in `.env`?

The `.env` file is tracked by git (see `.gitignore`). If you put credentials there, you risk:
- Accidentally committing secrets to the repo
- Exposing them in git history
- Security breaches if the repo is public

## How Boto3 Finds Credentials

Boto3 automatically searches for credentials in this order:

1. **Environment variables** in your current shell session
2. **`~/.aws/credentials`** file (created by `aws configure`)
3. **`~/.aws/config`** file
4. **IAM role** (if running on AWS)

## Setup Methods

### Method 1: `aws configure` (Recommended)

```bash
# Install AWS CLI if you haven't already
pip install awscli

# Configure your credentials
aws configure
```

You'll be prompted:
```
AWS Access Key ID [None]: AKIA... (from AWS Console)
AWS Secret Access Key [None]: ... (from AWS Console)
Default region name [None]: us-east-1
Default output format [None]: json
```

This creates two files:
- `~/.aws/credentials` - Your access keys (keep secret!)
- `~/.aws/config` - Region and output format

Then run the agent normally:
```bash
cd /Users/raghunandanask/Desktop/github-repo/k8-finops-agent
source venv/bin/activate
PYTHONPATH=sections/09-simple-agent-example python -m main
```

### Method 2: Environment Variables (Temporary)

Set credentials in your current shell session:

```bash
export AWS_ACCESS_KEY_ID="AKIA..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_REGION="us-east-1"

cd /Users/raghunandanask/Desktop/github-repo/k8-finops-agent
source venv/bin/activate
PYTHONPATH=sections/09-simple-agent-example python -m main
```

These are gone when you close the terminal.

### Method 3: Persistent Shell Profile

Add to your `~/.bashrc`, `~/.zshrc`, or `~/.profile`:

```bash
export AWS_ACCESS_KEY_ID="AKIA..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_REGION="us-east-1"
```

Then reload:
```bash
source ~/.bashrc  # or ~/.zshrc, ~/.profile, etc.
```

### Method 4: One-Line Command

Run the agent with credentials in a single command:

```bash
AWS_ACCESS_KEY_ID="AKIA..." \
AWS_SECRET_ACCESS_KEY="..." \
AWS_REGION="us-east-1" \
PYTHONPATH=sections/09-simple-agent-example python -m main
```

## Get Your AWS Credentials

1. Go to [AWS Console](https://console.aws.amazon.com/)
2. Click your account name → **Security Credentials**
3. Click **Access keys and secret access keys**
4. Click **Create New Access Key**
5. Copy:
   - **Access Key ID** (starts with `AKIA...`)
   - **Secret Access Key** (long string)

**Save these somewhere safe** - AWS only shows the secret key once!

## Verify Setup

Check that boto3 can find your credentials:

```bash
python3 << 'EOF'
import boto3
session = boto3.Session()
credentials = session.get_credentials()
if credentials:
    print(f"✓ Found credentials")
    print(f"  Access Key: {credentials.access_key[:10]}...")
else:
    print("✗ No credentials found")
EOF
```

## Permissions

Your AWS user needs these permissions for Bedrock:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:Converse"
            ],
            "Resource": "*"
        }
    ]
}
```

Ask your AWS admin to attach this policy to your user.

## Troubleshooting

### Error: "UnrecognizedClientException: The security token included in the request is invalid"

This means boto3 found credentials but they're invalid. Check:
1. Access Key ID is correct
2. Secret Access Key is correct
3. They haven't been rotated/deleted in AWS
4. Your user has permission to use Bedrock

### Error: "Unable to locate credentials"

Boto3 can't find credentials. Check:
1. Did you run `aws configure`?
2. Are environment variables set? `echo $AWS_ACCESS_KEY_ID`
3. Does `~/.aws/credentials` exist? `cat ~/.aws/credentials`

### Credentials Exposed in Git

If you accidentally committed credentials:

```bash
# Remove from git history
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch .env' \
  --prune-empty -- --all

# Force push (be careful!)
git push --force-with-lease
```

Then rotate your AWS access keys immediately!

## Next Steps

Once credentials are configured:

```bash
# Run from repo root
cd /Users/raghunandanask/Desktop/github-repo/k8-finops-agent
source venv/bin/activate
PYTHONPATH=sections/09-simple-agent-example python -m main
```

The agent will:
1. ✓ Find your credentials from your terminal/shell
2. ✓ Connect to AWS Bedrock
3. ✓ Fetch Kubernetes pod data
4. ✓ Send analysis to Bedrock
5. ✓ Report findings
