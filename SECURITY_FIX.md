# Security Fix: Exposed API Key

## Issue
An Amadeus API key was exposed in `api/check_env.py` and committed to git history.

## Actions Taken
1. ✅ Removed the key from current file (replaced with placeholder)
2. ✅ Committed the fix
3. ⚠️  Key still exists in git history (needs cleanup)

## IMPORTANT: Rotate Your API Key

**The exposed key is compromised. You must:**

1. **Go to Amadeus Developer Portal**: https://developers.amadeus.com/
2. **Revoke the old API key**: `GJGyBTf1laUXRgFlye2cN0oBsPEtP8wG`
3. **Generate a new API key**
4. **Update your `.env` file** with the new key
5. **Update GitHub Secrets** if using GitHub Actions

## Remove from Git History (Optional but Recommended)

The key is still visible in git history. To completely remove it:

### Option 1: Using git filter-repo (Recommended)

```bash
# Install git-filter-repo if needed
pip install git-filter-repo

# Remove the key from all history
git filter-repo --invert-paths --path api/check_env.py
# Then re-add the file with the fixed version
git add api/check_env.py
git commit -m "Security: Remove exposed API key"
git push origin master --force
```

### Option 2: Using BFG Repo-Cleaner

```bash
# Download BFG from https://rtyley.github.io/bfg-repo-cleaner/
# Replace the key in the file
echo 'GJGyBTf1laUXRgFlye2cN0oBsPEtP8wG' > secrets.txt
java -jar bfg.jar --replace-text secrets.txt
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push origin master --force
```

### Option 3: Manual History Rewrite (Advanced)

```bash
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch api/check_env.py" \
  --prune-empty --tag-name-filter cat -- --all
git push origin master --force
```

**⚠️ Warning**: Force pushing rewrites history. Coordinate with any collaborators.

## Prevention

- ✅ `.env` is already in `.gitignore`
- ✅ All example files use placeholders
- ✅ Never commit real credentials
- ✅ Use GitHub Secrets for CI/CD

## Status

- ✅ Current file fixed
- ⚠️  Git history still contains key (optional cleanup)
- ⚠️  **MUST ROTATE THE API KEY** (critical)
