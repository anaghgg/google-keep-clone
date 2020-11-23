from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from .serializers import NoteSerializer
from .models import Note
from rest_framework import status
from rest_framework import serializers
from accounts.serializers import UserSerializer

@login_required
@api_view(['GET'])
def get_user(request):
    user=request.user
    serializer=UserSerializer(user)
    return Response(serializer.data)

@login_required
@api_view(['GET'])
def notes_list(request):
    notes=Note.objects.filter(author=request.user).order_by('-date')
    serializer=NoteSerializer(notes,many=True)
    return Response(serializer.data)

@login_required
@api_view(['POST'])
def add_note(request):
    serializer=NoteSerializer(data=request.data,context = {"request":request})
    if serializer.is_valid():
        serializer.save()
    return Response(status=status.HTTP_201_CREATED)    

@login_required
@api_view(['PUT','DELETE'])
def edit_note(request,pk):
    note=Note.objects.get(id=pk)
    if note.author==request.user:
        if request.method=="PUT":
            serializer=NoteSerializer(instance=note,data=request.data,context = {"request":request})
            if serializer.is_valid():
                serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            note.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_403_FORBIDDEN)



