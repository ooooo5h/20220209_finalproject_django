# 사용자 정보를 가지고 토큰을 생성하기 
from urllib import request
import jwt
import my_custom_settings

from copang_app.models import Users
from copang_app.global_data import token_user

from functools import wraps
from rest_framework.response import Response

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
    
    
# 데코레이터 - @추가함수 형태로, 본 함수 실행전에 추가기능을 우선 수행하도록 하는 함수
def token_required(func):
    @wraps(func)
    def decorater(*args, **kwargs):
        
        request = args[1]
        token = request.headers['X-Http-Token']
        user = decode_token(token)
        
        if user:
            # 요청의 세션에 사용자 기록
            request.session['user_id'] = user.id
            # 프로젝트의 전역변수로 사용자를 전달하는 작업이 필요
            
            # 추가 행동을 하고 나면, 본 함수를 실행하도록 처리

            return func(*args, **kwargs)
        else:
            return Response({
                'code' : 403,
                'message' : '잘못된 토큰입니다.'
            }, status=403)

    # 위의 decorator에 적힌 내용을 실행하도록
    return decorater