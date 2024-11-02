from passlib.hash import pbkdf2_sha256

hash = pbkdf2_sha256.hash("321")
print(hash)
print(pbkdf2_sha256.verify("321", hash))
