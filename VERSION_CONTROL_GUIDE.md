# Version Control Guide for Cursor

## Best Solution: Git Version Control

Git is the industry standard for tracking file versions. Here's how to set it up:

### 1. Initialize Git Repository

Open Terminal in your project directory and run:

```bash
cd /Users/stchung/Downloads/Cursor
git init
```

### 2. Create .gitignore (already created for you)

This prevents tracking temporary files. The `.gitignore` file is already set up.

### 3. Make Your First Commit

```bash
# Stage all files
git add .

# Make your first commit
git commit -m "Initial commit: Space Invaders game with sound effects"
```

### 4. Track Changes Over Time

Every time you make significant changes:

```bash
# See what changed
git status

# Stage specific files
git add space_invaders_tkinter.py

# Commit with a descriptive message
git commit -m "Added realistic sound effects for shooting and barrier hits"
```

### 5. View History

```bash
# See commit history
git log

# See what changed in a file
git log --follow space_invaders_tkinter.py

# See differences between versions
git diff HEAD~1 space_invaders_tkinter.py
```

### 6. Create Branches for Experiments

```bash
# Create a new branch for testing features
git checkout -b sound-improvements

# Make changes, test them
# If you like them, merge back:
git checkout main
git merge sound-improvements

# If you don't like them, just switch back:
git checkout main
git branch -D sound-improvements  # Delete the branch
```

### 7. Restore Previous Versions

```bash
# See all versions of a file
git log --oneline space_invaders_tkinter.py

# Restore a specific version
git checkout <commit-hash> -- space_invaders_tkinter.py

# Or view a file from a specific commit
git show <commit-hash>:space_invaders_tkinter.py > old_version.py
```

## Alternative: Manual Versioning

If you prefer not to use Git, you can manually save versions:

### Option 1: Date-based naming
```bash
space_invaders_tkinter_v1.py
space_invaders_tkinter_v2_2024-01-15.py
space_invaders_tkinter_v3_with_sounds.py
```

### Option 2: Feature-based naming
```bash
space_invaders_tkinter.py          # Current version
space_invaders_tkinter_backup.py    # Backup
space_invaders_tkinter_sounds.py    # Version with sounds
```

### Option 3: Use Cursor's built-in history
- Cursor has a local history feature
- Right-click on a file → "Local History" or "Timeline"
- View previous versions directly in the editor

## Quick Git Commands Cheat Sheet

```bash
# Initialize repository
git init

# Check status
git status

# Add files
git add <filename>
git add .                    # Add all files

# Commit changes
git commit -m "Description of changes"

# View history
git log
git log --oneline           # Compact view
git log --graph --oneline   # Visual graph

# See differences
git diff                    # Unstaged changes
git diff --staged          # Staged changes
git diff HEAD~1            # Compare with previous commit

# Restore file
git restore <filename>      # Discard uncommitted changes
git checkout <commit> -- <filename>  # Restore from commit

# Create branch
git checkout -b <branch-name>

# Switch branch
git checkout <branch-name>

# Merge branch
git merge <branch-name>
```

## Recommended Workflow

1. **Before making changes**: `git status` to see current state
2. **Make your changes** in Cursor
3. **Review changes**: `git diff` to see what changed
4. **Commit regularly**: `git add . && git commit -m "Description"`
5. **Before major changes**: Create a branch with `git checkout -b feature-name`

## Pro Tips

- Commit often with descriptive messages
- Use branches for experimental features
- Tag important milestones: `git tag v1.0`
- Push to GitHub/GitLab for cloud backup (optional)

## Setting Up Remote Backup (Optional)

```bash
# Create a repository on GitHub, then:
git remote add origin https://github.com/yourusername/your-repo.git
git branch -M main
git push -u origin main
```

This gives you:
- Cloud backup
- Version history accessible anywhere
- Easy collaboration
- Free (GitHub free tier)
