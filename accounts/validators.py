from .models import User

def validate_user_data(user_data):
    username = user_data.get("username")
    password = user_data.get("password")
    email = user_data.get("email")
    nickusername = user_data.get("nickusername")
    birthday = user_data.get("birthday")
    image = user_data.get("image")
    gender = user_data.get("gender")
    introduction = user_data.get("introduction")

    if len(username) < 4 :
        return "message : username is require max 15 digit"
    
    if len(password) < 8 :
        return "message : password is require max 20 digit"
    
    if User.objects.filter(username=username).exists():
        return "already existed username"
    
    if User.objects.filter(email=email).exists():
        return "already existed email"
    