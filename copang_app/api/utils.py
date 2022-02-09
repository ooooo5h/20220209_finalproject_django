# 사용자 정보를 가지고 토큰을 생성하기 
import jwt
import my_custom_settings

def encode_token(user):
    
    return jwt.encode(
        {'id':user.id, 'email':user.email, 'password': user.password_hashed, },
        my_custom_settings.JWT_SECRET_KEY, # 비밀키를 뭘로 할건지
        my_custom_settings.JWT_ALGORITHM, # 어떤 알고리즘
    )