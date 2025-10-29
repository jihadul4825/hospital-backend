from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
# from django.urls import reverse, reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.exceptions import TokenError
# from rest_framework_simplejwt.authentication import JWTAuthentication


from .models import Account
from .serializers import AccountSerializer, UserLoginSerializer



class UserRegistrationView(generics.GenericAPIView):
    serializer_class = AccountSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            activation_link =  f"http://{get_current_site(request).domain}/users/activate/{uid}/{token}/"
            email_subject = "Activate your account"
            email_body = render_to_string('user/activation_email.html', {'user': user, 'activation_link': activation_link})
            
            email = EmailMultiAlternatives(email_subject, '', from_email=settings.EMAIL_HOST_USER, to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            
            return Response("Check your email to activate your account", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
         


class ActivationView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, uidb64, token):
        try:
            # uid = force_str(urlsafe_base64_decode(uidb64))
            uid = urlsafe_base64_decode(uidb64).decode()
            user = Account.objects.get(pk=uid)
        except(Account.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Account activated successfully! You can now login."})
            # return redirect('register')
        else:
            return Response({"error": "Invalid activation link"}, status=status.HTTP_400_BAD_REQUEST)
        

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            

            if user:
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)
                return Response({
                    'token': token.key, 
                    'user_id': user.id,
                    'email': user.email,
                    'username': user.username
                }, status=status.HTTP_200_OK)
                
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserLoginView(generics.GenericAPIView):  # for JWT 
#     serializer_class = UserLoginSerializer
#     permission_classes = [permissions.AllowAny]
    
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data, context={'request': request})
#         if serializer.is_valid():
#             user = serializer.validated_data['user']

#             if user:
#                 # Use JWT tokens instead
#                 refresh = RefreshToken.for_user(user)
#                 return Response({
#                     'refresh': str(refresh),
#                     'access': str(refresh.access_token),
#                     'user_id': user.id,
#                     'email': user.email,
#                     'username': user.username,
#                     'first_name': user.first_name,
#                     'last_name': user.last_name
#                 }, status=status.HTTP_200_OK)
                
#             else:
#                 return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserLogoutView(APIView):  # for JWT
    # permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [JWTAuthentication]
    
    # def post(self, request):
    #     try:
    #         seralizer = LogoutSerializer(data=request.data)
    #         if seralizer.is_valid():
    #             refresh_token = seralizer.validated_data['refresh']
    #             token = RefreshToken(refresh_token)
    #             token.blacklist()  # This will blacklist the refresh token
    #             return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    #         else:
    #             return Response(seralizer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     except TokenError as e:
    #         return Response({
    #             "error": "Invalid token"
    #         }, status=status.HTTP_400_BAD_REQUEST)
    #     except Exception as e:
    #         return Response({
    #             "error": "Something went wrong"
    #         }, status=status.HTTP_400_BAD_REQUEST)
    
    

class UserLogoutView(APIView):
    
    def get(self, request):
        try:
            Token.objects.get(user=request.user).delete()
        except:
            pass 
        
        logout(request)
        return redirect('login')
