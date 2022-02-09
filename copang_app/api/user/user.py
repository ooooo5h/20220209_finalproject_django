from rest_framework.views import APIView
from rest_framework.response import Response

from copang_app.models import Users
from copang_app.serializers import UsersSerializer

class User(APIView):
    
    def post(self, request):
        
        input_email = request.POST['email']
        input_pw = request.POST['password']
        
        print(f'이메일 : {input_email}, 비밀번호 : {input_pw}')
        
        # 이메일만 가지고 사용자를 검색해보자
        email_ok_user = Users.objects.filter(email=input_email).first()
        
        if email_ok_user:
            # 임시 : 비밀번호는 암호화되어있고 장고에서는 아직 기능 구현이 안되어있음!!
            # 그래서 이메일만 맞으면 성공처리하자
            
            user_serialized = UsersSerializer(email_ok_user)
            
            return Response({
                'code' : 200,
                'message' : '임시 - 로그인 성공',
                'data' : {
                    'user' : user_serialized.data,
                }
        })
            
        else :
            return Response({
                'code' : 400,
                'message' : '해당 이메일의 사용자는 존재하지않습니다.'
            }, status=400)
            
