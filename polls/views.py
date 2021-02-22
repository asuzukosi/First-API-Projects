from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Poll, Choice, Vote
from .serializers import PollSerializer, ChoiceSerializer, UserSerializer, VoteSerializer
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
import datetime
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.exceptions import PermissionDenied


# Create your views here.
def home(request):
    return HttpResponse("Hello from polls home")


class PollsAPIView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        This endpoint provides all the polls on the application

        """
        polls = Poll.objects.all()
        serializer = PollSerializer(polls, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = PollSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PollsDetailAPIView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = PollSerializer
    queryset = Poll.objects.all()
    lookup_field = 'pk'

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def put(self, request, pk):
        poll = Poll.objects.get(pk=pk)
        if request.user != poll.created_by:
            raise PermissionDenied("You can not edit this poll")

        return self.update(request, pk)

    def delete(self, request, pk):
        poll = Poll.objects.get(pk=pk)
        if request.user != poll.created_by:
            raise PermissionDenied("You can not delete this poll")
        return self.destroy(request, pk)


class ChoicesAPIView(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = ChoiceSerializer

    def get_queryset(self):
        choices = Choice.objects.filter(poll__id=self.kwargs["pk"])
        return choices

    def get(self, request, pk):
        return self.list(request)

    def post(self, request, pk):
        poll = Poll.objects.get(pk=pk)
        if request.user != poll.created_by:
            raise PermissionDenied("You can not create this choice")

        request.data["poll"] = self.kwargs["pk"]
        return self.create(request)


class ChoiceDetailAPIView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = ChoiceSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        choices = Choice.objects.filter(poll__id=self.kwargs["pk"])
        return choices

    def get(self, request, pk, c_pk):
        return self.retrieve(self, request, c_pk)

    def put(self, request, pk, c_pk):
        poll = Poll.objects.get(pk=pk)
        if request.user != poll.created_by:
            raise PermissionDenied("You can not edit this choice")
        return self.update(self, request, c_pk)

    def delete(self, request, pk, c_pk):
        poll = Poll.objects.get(pk=pk)
        if request.user != poll.created_by:
            raise PermissionDenied("You can not delete this choice")
        return self.destroy(self, request, c_pk)


class VotesAPIView(mixins.ListModelMixin, GenericAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = VoteSerializer

    def get_queryset(self):
        votes = Vote.objects.filter(choice__id=self.kwargs["c_pk"], poll__id=self.kwargs["pk"])
        return votes

    def get(self, request, pk, c_pk):
        return self.list(request)

    def post(self, request, pk, c_pk):
        data = dict()
        data["choice"] = c_pk
        data["poll"] = pk
        data["voted_by"] = 1
        data["time_voted"] = datetime.datetime.now()

        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VoteDetailsAPIView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    lookup_field = 'pk'


class UserCreateAPIView(mixins.CreateModelMixin, GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'pk'

    def post(self, request):
        return self.create(request)


class LoginApiView(APIView):

    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            return Response({
                "token": user.auth_token.key
            })
        else:
            return Response({
               "error": "Wrong credentials"
            }, status=status.HTTP_404_NOT_FOUND)









