from django.shortcuts import render
from rest_framework import viewsets 
from movieapi.restapi.serializers import MovieSerializer
from movieapi.restapi.models import Movie
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.core.exceptions import ValidationError


def homepage(request):
    return HttpResponse('Hello Android Students.')


class MovieViewSet(viewsets.ModelViewSet):

    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Movie.objects.filter(user=self.request.user).order_by('name')

    def create(self, request):
        try:
            print("creating", request.data)
            movie = Movie(name=request.data['name'], rating=request.data['rating'], user=request.user)
            movie.full_clean()
            movie.save()
            return Response(MovieSerializer(movie).data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            print('Invalid request, validation error ' + str(e))
            return Response({'error': 'Invalid data. Movie name must be unique. Rating must be between 0 and 5.'}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            print('Ivnavlid request, ntegrity error ' + str(e))
            return Response({'error': 'Invalid data. Movie name must be unique. Rating must be between 0 and 5.'}, status=status.HTTP_400_BAD_REQUEST)
