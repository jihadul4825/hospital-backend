from rest_framework import generics, permissions
from rest_framework.response import Response
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .models import Account
from .serializers import AccountSerializer
from django.contrib.auth.tokens import default_token_generator


class UserRegistrationView(generics.GenericAPIView):
    serializer_class = AccountSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, rquest):
        serializer = self.serializer_class(data=rquest.data)
        if serializer.is_valid():
            user = serializer.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            activation_link = f"http://{get_current_site(rquest).domain}/activate/{uid}/{token}"
            email_subject = "Activate your account"
            email_body = render_to_string('user/activation_email.html', {'activation_link': activation_link})
            
            email = EmailMultiAlternatives(email_subject, '', from_email=settings.EMAIL_HOST_USER, to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            
            return Response("Check your email to activate your account", status=201)
        return Response(serializer.errors, status=400)