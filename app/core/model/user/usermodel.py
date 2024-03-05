from pydantic import BaseModel, EmailStr, constr, validator
from typing_extensions import Optional
import re

class UserDetail(BaseModel):
    """
        - Response model for user detail
    """
    login_id_user: str
    email_user: EmailStr
    point_user: int = None
    point2_user: Optional[int]


class RegisterUser(BaseModel):
    username: str
    password: constr(min_length=8, max_length=20)
    email: EmailStr  # Using EmailStr for built-in email validation
    security_code: int

    @validator('password')
    def validate_password(cls, value):
        # Define a regex pattern to ensure password doesn't contain special characters
        pattern = re.compile(r'^[^\W_]+$')  # Allows letters, numbers, and underscores
        if not pattern.match(value):
            raise ValueError("Password contains invalid characters")
        return value

    @validator('email')
    def validate_email(cls, value):
        # Define a regular expression pattern to validate the email address
        pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        
        # Check if the email matches the pattern
        if not pattern.match(value):
            raise ValueError("Invalid email address")
        return value

class RegisterResponse(BaseModel):
    login_id: str
    email: str 
    default_point: int


##### CHANGEPASSWORD
from pydantic import BaseModel, constr, validator, EmailStr

class UserChangePassword(BaseModel):
    login_id: str
    current_password: constr(min_length=8, max_length=20)
    new_password: constr(min_length=8, max_length=20)
    confirm_new_password: constr(min_length=8, max_length=20)
    current_email: EmailStr

    @validator('current_password')
    def validate_current_password(cls, value):
        # Implement validation logic for current password if needed
        # For example, you might want to check if the current password matches the one stored in the database
        return value

    @validator('new_password')
    def validate_new_password(cls, value):
        # Define a regex pattern to ensure password doesn't contain special characters
        pattern = re.compile(r'^[^\W_]+$')  # Allows letters, numbers, and underscores
        if not pattern.match(value):
            raise ValueError("Password contains invalid characters")
        return value

    @validator('confirm_new_password')
    def validate_confirm_new_password(cls, value, values):
        # Check if the new password matches the confirmed new password
        if 'new_password' in values and value != values['new_password']:
            raise ValueError("Passwords do not match")
        return value

    @validator('current_email')
    def validate_email(cls, value):
        # Define a regular expression pattern to validate the email address
        pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        
        # Check if the email matches the pattern
        if not pattern.match(value):
            raise ValueError("Invalid email address")
        return value
