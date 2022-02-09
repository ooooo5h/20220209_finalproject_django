# 사용자 정보를 가지고 토큰을 생성하기 
import jwt
import my_custom_settings

from copang_app.models import Users

def encode_token(user):
    
    return jwt.encode(
        {'id':user.id, 'email':user.email, 'password': user.password_hashed, },
        my_custom_settings.JWT_SECRET_KEY, # 비밀키를 뭘로 할건지
        my_custom_settings.JWT_ALGORITHM, # 어떤 알고리즘
    )
    
def decode_token(token):
    # 암호화된 토큰을 가지고, 복호화를 하면 그 결과물이 dict로 나온다(id, email, password를 가지고 있는. 위)
    # 복호화에 실패했다면 잘못된 토큰이란 이야기 -> 토큰에 맞는 사용자는 없다
    # 복호화 성공 -> id/email/pw이 틀렸다면 이미 완료된 토큰처리 -> 토큰에 맞는 사용자는 없다
    
    try :
        decoded_dict = jwt.decode(
            token,
            my_custom_settings.JWT_SECRET_KEY,
            algorithms = my_custom_settings.JWT_ALGORITHM,
        )
        
        user = Users.objects\
            .filter(id=decoded_dict['id'])\
            .filter(email=decoded_dict['email'])\
            .filter(password_hashed=decoded_dict['password'])\
            .first()
            
        # 성공했다면 실제 사용자가 있고 없다면 None
        # 받는 입장에서 있냐없냐를 판단해서 쓰자
        return user                
    
    except jwt.exceptions.DecodeError:
         
        # 복호화중에 문제가 발생했다는 이야기
        # 토큰이 잘못됐다 => 사용자 없다고 None 리턴
        return None