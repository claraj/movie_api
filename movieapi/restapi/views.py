from django.shortcuts import render
from rest_framework import viewsets 
from movieapi.restapi.serializers import MovieSerializer
from movieapi.restapi.models import Movie
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.utils import IntegrityError
from django.http import HttpResponse


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
            movie = Movie(name=request.data['name'], rating=request.data['rating'], user=request.user).save()
            return Response(movie, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
