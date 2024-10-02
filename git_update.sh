#!/bin/bash

# Check if there are any changes
if git diff --quiet && git diff --staged --quiet; then
    echo "No changes to commit"
    exit 0
fi

# Stage all changes
git add -A

# Commit with a default message (or you can prompt the user for a message)
commit_message="Auto-update: $(date +"%Y-%m-%d %H:%M:%S")"
git commit -m "$commit_message"

# Push to the current branch
git push

# Print success message
echo "Changes pushed successfully!"
