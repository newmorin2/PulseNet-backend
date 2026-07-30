from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics

from django.contrib.auth.models import User

from .serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer


@api_view(["GET"])
def current_user(request):

    return Response({
        "username":request.user.username,
        "email":request.user.email

    })