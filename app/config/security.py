from datetime import timedelta

# jwt配置
SECRET_KEY = "fed8a19950e4065ff34e8d12f0657ca36dbb8cdca36b5a14c3b6cc5d65a52103"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = timedelta(minutes=999999999)