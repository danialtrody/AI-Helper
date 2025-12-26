# import os
# from pydantic import BaseModel
# from datetime import datetime, timedelta, timezone
# from jose import jwt, JWTError
# from dotenv import load_dotenv
#
#
# load_dotenv()
#
#
# SECRET_KEY = os.getenv('SECRET_KEY')
# ALGORITHM = os.getenv('ALGORITHM')
# ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
#
#
#
# class Token(BaseModel):
#     access_token: str
#     token_type: str
#
#
# def create_access_token(username:str ,user_id:str , expire_delta:timedelta):
#
#     payload = {"name": username ,"user_id":user_id}
#
#     expires = datetime.now(timezone.utc) + expire_delta
#     payload.update({"exp": expires})
#
#     return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
#
#
