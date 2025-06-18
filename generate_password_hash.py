import bcrypt


def generate_password_hash(password):
    """Generate bcrypt hash for a password"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def check_password(password, hashed):
    """Check if password matches the hashed version"""
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


# Generate hash for "password"
password = "password"
hashed = generate_password_hash(password)

print(f"Password: {password}")
print(f"Hash: {hashed}")
print(f"Verification: {check_password(password, hashed)}")

# Test the hash that was in the SQL
old_hash = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj2LN1B9tXvG"
print(f"Old hash works: {check_password(password, old_hash)}")
