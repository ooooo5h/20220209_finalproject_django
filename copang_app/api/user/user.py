from rest_framework.views import APIView
from rest_framework.response import Response

from copang_app.models import Users
from copang_app.serializers import UsersSerializer

from copang_app.api.utils import encode_token, decode_token, token_required

class User(APIView):
    
    @token_required
    def get(self, request):
        
        return Response({
            'code' : 200,
            'message' : '내 정보 조회',
            
        })
       
   
    
    def post(self, request):
        
        input_email = request.POST['email']
        input_pw = request.POST['password']
        
        print(f'이메일 : {input_email}, 비밀번호 : {input_pw}')
        
        # 이메일만 가지고 사용자를 검색해보자
        email_ok_user = Users.objects.filter(email=input_email).first()
        
        if email_ok_user:
            # 비밀번호도 맞는지 확인
            
            if email_ok_user.is_same_password(input_pw):
                
                user_serialized = UsersSerializer(email_ok_user)
                
                return Response({
                    'code' : 200,
                    'message' : '로그인 성공',
                    'data' : {
                        'user' : user_serialized.data,
                        'token' : encode_token(email_ok_user),
                    }
                }) 
            else :
                return Response({
                    'code' : 400,
                    'message' : '비밀번호가 틀렸습니다.'
                }, status=400)
            
        else:
            return Response({
                'code': 400,
                'message': '해당 이메일의 사용자는 존재하지 않습니다.'
            }, status=400)

