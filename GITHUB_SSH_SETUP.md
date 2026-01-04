# GitHub SSH Key Setup for udhaydurai Account

## Step 1: Check Existing SSH Keys

```bash
# List all SSH keys
ls -la ~/.ssh/

# Check if you have keys for GitHub
ls -la ~/.ssh/id_*.pub
```

## Step 2: Generate New SSH Key (if needed)

If you don't have an SSH key or want to create a new one:

```bash
# Generate new SSH key
ssh-keygen -t ed25519 -C "udhayakumar.d@gmail.com" -f ~/.ssh/id_ed25519_github_udhaydurai

# Or use RSA if ed25519 is not supported
ssh-keygen -t rsa -b 4096 -C "udhayakumar.d@gmail.com" -f ~/.ssh/id_rsa_github_udhaydurai
```

**When prompted:**
- Press Enter to accept default location
- Enter a passphrase (optional but recommended)

## Step 3: Add SSH Key to SSH Agent

```bash
# Start ssh-agent
eval "$(ssh-agent -s)"

# Add your SSH key to the agent
ssh-add ~/.ssh/id_ed25519_github_udhaydurai
# OR if using RSA:
# ssh-add ~/.ssh/id_rsa_github_udhaydurai
```

**To make it persistent (add to ~/.ssh/config):**

```bash
# Create or edit SSH config
nano ~/.ssh/config
```

Add this:

```
Host github.com-udhaydurai
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_github_udhaydurai
    IdentitiesOnly yes
```

## Step 4: Copy Public Key

```bash
# Display your public key
cat ~/.ssh/id_ed25519_github_udhaydurai.pub
# OR if using RSA:
# cat ~/.ssh/id_rsa_github_udhaydurai.pub
```

**Copy the entire output** (starts with `ssh-ed25519` or `ssh-rsa`)

## Step 5: Add SSH Key to GitHub

1. Go to https://github.com/settings/keys
2. Click **"New SSH key"**
3. **Title**: `FlightAgent Mac` (or any descriptive name)
4. **Key type**: Authentication Key
5. **Key**: Paste your public key
6. Click **"Add SSH key"**

## Step 6: Test Connection

```bash
# Test GitHub connection
ssh -T git@github.com
```

**Expected output:**
```
Hi udhaydurai! You've successfully authenticated, but GitHub does not provide shell access.
```

## Step 7: Update Git Remote to Use SSH

After SSH is set up:

```bash
cd /Users/udhaydurai/Documents/GitHub/FlightAgent

# If remote already exists with HTTPS, remove it
git remote remove origin

# Add remote with SSH
git remote add origin git@github.com:udhaydurai/FlightAgent.git

# Verify
git remote -v
```

## Troubleshooting

### "Permission denied (publickey)" error
- Make sure SSH key is added to GitHub
- Check key is loaded: `ssh-add -l`
- Verify key file permissions: `chmod 600 ~/.ssh/id_*`

### Multiple GitHub Accounts
If you have multiple GitHub accounts, use SSH config:

```
# ~/.ssh/config
Host github.com-udhaydurai
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_github_udhaydurai
    IdentitiesOnly yes

Host github.com-sdtsweb
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_github_sdtsweb
    IdentitiesOnly yes
```

Then use: `git@github.com-udhaydurai:udhaydurai/FlightAgent.git`

### Check Which Account You're Connected To
```bash
ssh -T git@github.com
```

The response will show your username.
