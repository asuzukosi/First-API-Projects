from django.urls import path
from .views import home, LoginApiView, UserCreateAPIView, PollsAPIView, PollsDetailAPIView, ChoicesAPIView, ChoiceDetailAPIView, VotesAPIView, VoteDetailsAPIView
from rest_framework.documentation import include_docs_urls
urlpatterns = [
    path("", home, name="Home"),
    path('api/polls', PollsAPIView.as_view(), name='Polls'),
    path('api/polls/<int:pk>', PollsDetailAPIView.as_view(), name='Poll'),
    path('api/polls/<int:pk>/choices', ChoicesAPIView.as_view(), name='Choices'),
    path('api/polls/<int:pk>/choices/<c_pk>', ChoiceDetailAPIView.as_view(), name='Choice'),
    path('api/polls/<int:pk>/choices/<c_pk>/votes', VotesAPIView.as_view(), name='Votes'),
    path('api/votes/<int:pk>', VoteDetailsAPIView.as_view(), name='Vote'),
    path('api/users', UserCreateAPIView.as_view(), name='Sign up'),
    path('api/login', LoginApiView.as_view(), name='Login'),
    path(r'docs/', include_docs_urls(title='Polls Api'))

]
