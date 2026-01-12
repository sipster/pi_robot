# Common Python Update Errors Explained

## 1. Syntax Errors (Python 2 → Python 3)

### Error: `print` without parentheses
```python
# Python 2 (old)
print "Hello"

# Python 3 (new)
print("Hello")
```

### Error: Integer division
```python
# Python 2
result = 5 / 2  # Returns 2

# Python 3
result = 5 / 2   # Returns 2.5
result = 5 // 2   # Returns 2 (integer division)
```

## 2. Import Errors

### Error: `ModuleNotFoundError: No module named 'X'`
**Meaning**: The module isn't installed or the name changed.

**Fix**:
```bash
pip3 install module_name
```

### Error: `ImportError: cannot import name 'X' from 'Y'`
**Meaning**: The import path or name changed between versions.

**Fix**: Check the library's documentation for the new import path.

## 3. Deprecated Features

### Error: `DeprecationWarning` or feature removed
**Meaning**: Old code uses features that are no longer supported.

**Common examples**:
- `raw_input()` → `input()` (Python 2 → 3)
- `xrange()` → `range()` (Python 2 → 3)
- `dict.has_key()` → `in` operator (Python 2 → 3)

## 4. Type/Attribute Errors

### Error: `AttributeError: 'X' object has no attribute 'Y'`
**Meaning**: The object structure changed in a newer version.

**Fix**: Check the library's changelog or documentation.

### Error: `TypeError: X() takes Y positional arguments but Z were given`
**Meaning**: Function signature changed.

**Fix**: Update function calls to match new signature.

## 5. String/Byte Errors

### Error: `TypeError: a bytes-like object is required, not 'str'`
**Meaning**: Python 3 distinguishes between strings (text) and bytes (binary data).

**Fix**:
```python
# Old (Python 2)
data = "text"

# New (Python 3)
data = b"text"  # For bytes
data = "text"   # For strings (Unicode)
```

## 6. Library Version Compatibility

### Error: `VersionConflict` or `Requirement already satisfied`
**Meaning**: Package version conflicts.

**Fix**:
```bash
# Check current version
pip3 show package_name

# Upgrade package
pip3 install --upgrade package_name

# Install specific version
pip3 install package_name==2.5.0
```

## 7. Python Version Mismatch

### Error: `SyntaxError: invalid syntax` on valid code
**Meaning**: Code written for newer Python version, running on older version.

**Fix**: Check Python version:
```bash
python3 --version
```

### Error: `f-string expressions` or other Python 3.6+ features
**Meaning**: Using features from newer Python versions.

**Fix**: Either upgrade Python or rewrite code for older version.

## 8. Path/File Errors

### Error: `FileNotFoundError` or `IOError`
**Meaning**: File path handling changed.

**Fix**: Use `pathlib` or ensure correct path format:
```python
# Modern approach
from pathlib import Path
file_path = Path("file.txt")
```

## Common Update Scenarios

### Updating from Python 2 to Python 3
- Use `2to3` tool: `2to3 -w script.py`
- Fix print statements
- Update imports
- Fix string/bytes handling

### Updating Python 3.x to 3.y
- Usually backward compatible
- Check for deprecated warnings
- Update libraries if needed

### Updating Libraries
- Check changelog: `pip3 show package_name`
- Read migration guide
- Test thoroughly after update

## How to Diagnose Your Error

1. **Read the full error message** - It usually tells you what's wrong
2. **Check the line number** - Points to the problematic code
3. **Google the error** - Someone else has likely seen it
4. **Check library docs** - Look for migration guides
5. **Use `python3 -m py_compile script.py`** - Check for syntax errors

## Getting Help

When asking for help, provide:
- Full error message (copy/paste)
- Python version: `python3 --version`
- What you're trying to do
- Relevant code snippet
