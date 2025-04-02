from werkzeug.security import generate_password_hash

password = "password@123"
# salt + password
hashed_password = generate_password_hash(password)  # 16 -> salt length (default)

print(hashed_password)
