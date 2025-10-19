from django.shortcuts import render
from .models import Account
from .serializers import AccountSerializer
from rest_framework import generics, permissions


class UserRegistrationView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save()
    
    
    
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # If the URL does not include a pk and the path is intended for the current user,
        # assume client will call with 'me' route; otherwise fallback to lookup by pk.
        # allow /accounts/me/ endpoint
        
        lookup = self.kwargs.get('pk')
        if lookup == 'me' or lookup is None:
            return self.request.user
        return super().get_object()
    # No need to override perform_update because serializer.update handles password hashing
        
        

    

