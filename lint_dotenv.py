import re
import sys

def validate_env(filename):
    key_regex = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')

    keys_seen = set()
    errors = []
    warnings = []

    with open(filename, 'r', encoding='utf-8') as f:
        for lineno, line in enumerate(f, 1):
            original_line = line
            line = line.strip()

            # Skip empty lines or comments
            if not line or line.startswith('#'):
                continue

            # Check for 'key=value' pattern
            if '=' not in line:
                errors.append(f"Line {lineno}: Missing '=' sign.")
                continue

            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()

            # Check key syntax
            if not key_regex.match(key):
                errors.append(f"Line {lineno}: Invalid key '{key}'. Must start with a letter or underscore and contain only letters, digits, or underscores.")

            # Check for duplicate keys
            if key in keys_seen:
                errors.append(f"Line {lineno}: Duplicate key '{key}'.")
            else:
                keys_seen.add(key)

            # Warn if value is empty
            if value == '':
                warnings.append(f"Line {lineno}: Key '{key}' has no value assigned.")

            # Check for trailing whitespace in value
            stripped_line = line.rstrip('\r\n')
            if original_line.rstrip() != stripped_line:
                warnings.append(f"Line {lineno}: Trailing whitespace detected.")

            # Check for balanced quotes if value is quoted
            if (value.startswith('"') and not value.endswith('"')) or (value.startswith("'") and not value.endswith("'")):
                errors.append(f"Line {lineno}: Unbalanced quotes in value.")

            # Optional: Detect if value contains unescaped spaces without quotes (common mistake)
            if ' ' in value and not (value.startswith('"') and value.endswith('"')) and not (value.startswith("'") and value.endswith("'")):
                warnings.append(f"Line {lineno}: Value contains spaces but is not quoted.")

    # Print errors and warnings
    if errors:
        print("Errors:")
        for e in errors:
            print(f"  {e}")
    if warnings:
        print("Warnings:")
        for w in warnings:
            print(f"  {w}")

    if errors:
        return False
    return True


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_env.py <path_to_env_file>")
        sys.exit(1)

    env_file = sys.argv[1]
    if not validate_env(env_file):
        sys.exit(1)
