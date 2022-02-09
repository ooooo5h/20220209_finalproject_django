import imp
from rest_framework.views import APIView
from rest_framework.response import Response

from copang_app.models import Users

class User(APIView):
    
    def post(self, request):
        
        input_email = request.POST['email']
        input_pw = request.POST['password']
        
        print(f'이메일 : {input_email}, 비밀번호 : {input_pw}')
        
        return Response({
            'code' : 200,
            'message' : '임시 - 로그인 기능'
        })