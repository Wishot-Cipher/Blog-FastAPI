from pydantic import BaseModel, EmailStr, Field
from typing import List


class BlogPost(BaseModel):
    title: str = Field(example="Blog Title")
    body: str = Field(example="Blog Body")


class Blog(BlogPost):
    class Config():
        orm_mode = True


class User(BaseModel):
    name: str = Field(example="Username")
    email: EmailStr = Field(example="Example@gmail.com")
    password: str = Field(example="Input password", min_length=8, max_length=50)


# Shows a single user
class SingleUser(BaseModel):
    name: str
    email: EmailStr

    class Config():
        orm_mode = True


# Shows user name with  all the blogs he created
class ShowUser(BaseModel):
    name: str
    email: EmailStr
    blogs: List[Blog]

    class Config():
        orm_mode = True


# Here we are fetching a single user with a single blog created by the user
class ShowBlog(BaseModel):
    title: str = Field(example="Blog Title")
    body: str = Field(example="Blog Body")
    creator: SingleUser

    class Config():
        orm_mode = True


# Creating the login Schema
class Login(BaseModel):
    email: EmailStr
    password: str = Field(example="Input password")


# THIS IS FOR THE JWT TOKEN GENERATOR
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenDate(BaseModel):
    email = EmailStr