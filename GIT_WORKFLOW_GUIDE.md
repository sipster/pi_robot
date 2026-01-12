# Git Workflow Guide for Cursor Script Development

## Best Practices: Step-by-Step Workflow

### Daily Workflow: Making Changes to Scripts

#### Step 1: Before Making Changes
```bash
# Check current status
git status

# See what you're working on
git log --oneline -5
```

**Why**: Know your starting point before making changes.

---

#### Step 2: Make Your Changes in Cursor
- Edit your script (`space_invaders_tkinter.py`, etc.)
- Test your changes
- Make sure it works before committing

**Best Practice**: Don't commit broken code. Test first!

---

#### Step 3: Review What Changed
```bash
# See what files changed
git status

# See the actual changes (what was added/removed)
git diff

# See changes in a specific file
git diff space_invaders_tkinter.py
```

**Why**: Review changes before committing to catch mistakes.

---

#### Step 4: Stage Your Changes
```bash
# Stage a specific file
git add space_invaders_tkinter.py

# OR stage all changed files
git add .

# See what's staged
git status
```

**Why**: Git requires you to explicitly stage files before committing.

---

#### Step 5: Commit with a Descriptive Message
```bash
# Good commit message format
git commit -m "Brief summary of what changed

Optional: More detailed explanation if needed"

# Examples:
git commit -m "Added realistic spaceship design to player"
git commit -m "Fixed sound effects for barrier hits"
git commit -m "Improved enemy movement patterns"
```

**Best Practices for Commit Messages**:
- ✅ **Good**: "Added sound effects for shooting"
- ✅ **Good**: "Fixed barrier collision detection bug"
- ✅ **Good**: "Improved spaceship graphics with wings and cockpit"
- ❌ **Bad**: "Update"
- ❌ **Bad**: "Changes"
- ❌ **Bad**: "Fixed stuff"

**Why**: Good messages help you understand history later.

---

#### Step 6: Verify Your Commit
```bash
# See your commit
git log --oneline -1

# See full details
git show HEAD
```

---

## Complete Workflow Example

Here's a real example of updating your Space Invaders script:

```bash
# 1. Start: Check status
git status

# 2. Make changes in Cursor (edit space_invaders_tkinter.py)

# 3. Test your changes
python3 space_invaders_tkinter.py

# 4. Review changes
git diff space_invaders_tkinter.py

# 5. Stage the file
git add space_invaders_tkinter.py

# 6. Commit
git commit -m "Added realistic spaceship with wings and cockpit"

# 7. Verify
git log --oneline -1
```

---

## When to Commit: Best Practices

### ✅ Commit Frequently When:
- You complete a feature (e.g., "Added sound effects")
- You fix a bug (e.g., "Fixed barrier collision bug")
- You refactor code (e.g., "Improved enemy movement logic")
- You make a working improvement
- End of a work session (save your progress)

### ❌ Don't Commit:
- Broken/non-working code
- Temporary test code
- Files with syntax errors
- Half-finished features (unless using a branch)

### Commit Frequency Guidelines:
- **Small changes**: Commit after each logical change
- **Large features**: Commit when feature is complete and tested
- **End of day**: Always commit your work before closing

---

## Advanced: Using Branches for Experiments

### When to Use Branches:
- Trying experimental features
- Major refactoring
- Testing different approaches
- Working on multiple features simultaneously

### Branch Workflow:

```bash
# 1. Create a branch for your experiment
git checkout -b experiment-sound-improvements

# 2. Make changes, test, commit
# (work normally, commits go to this branch)

# 3. If experiment works, merge to main
git checkout main
git merge experiment-sound-improvements

# 4. If experiment fails, just switch back
git checkout main
git branch -D experiment-sound-improvements  # Delete branch
```

**Example**:
```bash
# Try adding new enemy types
git checkout -b new-enemy-types
# ... make changes ...
git add .
git commit -m "Added flying saucer enemy type"
# Test it, works great!
git checkout main
git merge new-enemy-types
```

---

## Useful Git Commands for Daily Use

### See What Changed
```bash
# Quick status
git status

# See changes in detail
git diff

# See changes in specific file
git diff space_invaders_tkinter.py

# See what's staged
git diff --staged
```

### View History
```bash
# Compact view
git log --oneline

# Last 5 commits
git log --oneline -5

# See changes in a commit
git show <commit-hash>

# See changes in a file over time
git log --follow space_invaders_tkinter.py
```

### Undo Mistakes
```bash
# Unstage a file (keep changes)
git reset HEAD space_invaders_tkinter.py

# Discard changes in a file (careful!)
git checkout -- space_invaders_tkinter.py

# Undo last commit (keep changes)
git reset --soft HEAD~1

# See what you'd lose
git status
```

### Compare Versions
```bash
# Compare current with last commit
git diff HEAD~1

# Compare two specific commits
git diff <commit1> <commit2>

# Compare with a specific file version
git diff HEAD~3 space_invaders_tkinter.py
```

---

## Recommended Workflow for Cursor

### Quick Workflow (Most Common)
```bash
# 1. Make changes in Cursor
# 2. Test: python3 space_invaders_tkinter.py
# 3. Commit:
git add space_invaders_tkinter.py
git commit -m "Description of what you changed"
```

### Full Workflow (For Important Changes)
```bash
# 1. Check status
git status

# 2. Make changes in Cursor

# 3. Test thoroughly
python3 space_invaders_tkinter.py

# 4. Review changes
git diff space_invaders_tkinter.py

# 5. Stage
git add space_invaders_tkinter.py

# 6. Commit with good message
git commit -m "Clear description of changes"

# 7. Verify
git log --oneline -1
```

---

## Commit Message Templates

### Feature Addition
```
Added [feature name]

- What it does
- Why it's useful
```

### Bug Fix
```
Fixed [bug description]

- What was wrong
- How it's fixed
```

### Improvement
```
Improved [what was improved]

- What changed
- Why it's better
```

### Refactoring
```
Refactored [what was refactored]

- What changed structurally
- Why (performance, readability, etc.)
```

---

## Example Session

Here's a complete example session:

```bash
# Morning: Start working
$ git status
On branch main
nothing to commit, working tree clean

# Make changes in Cursor: Add new enemy type
# ... edit space_invaders_tkinter.py ...

# Test it
$ python3 space_invaders_tkinter.py
# Works! ✓

# Review changes
$ git diff space_invaders_tkinter.py
# Review the diff, looks good

# Commit
$ git add space_invaders_tkinter.py
$ git commit -m "Added flying saucer enemy with different movement pattern"
[main a1b2c3d] Added flying saucer enemy with different movement pattern
 1 file changed, 45 insertions(+), 2 deletions(-)

# Continue working: Fix a bug
# ... edit space_invaders_tkinter.py ...

# Test fix
$ python3 space_invaders_tkinter.py
# Fixed! ✓

# Commit the fix
$ git add space_invaders_tkinter.py
$ git commit -m "Fixed enemy collision detection bug"
[main e4f5g6h] Fixed enemy collision detection bug
 1 file changed, 8 insertions(+), 5 deletions(-)

# End of session: View history
$ git log --oneline -3
e4f5g6h Fixed enemy collision detection bug
a1b2c3d Added flying saucer enemy with different movement pattern
796ed61 Added realistic spaceship
```

---

## Pro Tips

1. **Commit often**: Small, frequent commits are better than large, infrequent ones
2. **Test before commit**: Don't commit broken code
3. **Write good messages**: Future you will thank you
4. **Review before commit**: `git diff` is your friend
5. **Use branches for experiments**: Safe way to try new things
6. **Commit at end of day**: Always save your work

---

## Quick Reference Card

```bash
# Daily workflow
git status                    # Check what changed
git diff                      # See changes
git add <file>               # Stage file
git commit -m "Message"      # Commit
git log --oneline -5         # View history

# When experimenting
git checkout -b branch-name  # Create branch
git checkout main            # Switch back
git merge branch-name         # Merge branch

# If something goes wrong
git diff                      # See what changed
git checkout -- <file>       # Discard changes (careful!)
git log                       # Find previous version
```

---

## Summary

**The Golden Rule**: Commit working, tested code with clear messages.

**The Workflow**:
1. Make changes
2. Test changes
3. Review changes (`git diff`)
4. Stage changes (`git add`)
5. Commit changes (`git commit -m "message"`)
6. Verify commit (`git log`)

Follow this workflow, and you'll have a clean, understandable Git history!
