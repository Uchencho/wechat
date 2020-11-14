from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from accounts.models import User
from chat.models import Thread, ChatMessage
from .serializers import UserSerializer, ChatMessageSerializer

class UserView(generics.ListAPIView):
    serializer_class        = UserSerializer
    permission_classes      = [IsAuthenticated]
    authentication_classes  = [SessionAuthentication]

    def get_queryset(self):
        return User.objects.filter(email__iexact=self.request.user.email)


def string_to_bool(the_string):
    if the_string == "true":
        return True
    elif the_string == "false":
        return False
    else:
        return ""


class ChatHistory(APIView):

    """
    Retrieve the list of users a specific user has had a conversation with
    """

    def get(self, request):
        qs = Thread.objects.by_user(request.user)
        if not qs.exists():
            return Response({"message" : "success", "data" : {}})

        chat_det = [{"id" : chatter.id, "username" : chatter.first.username if not request.user.username else chatter.second.username} for chatter in qs]
        return Response({"message" : "success", "data" : chat_det})


class AllUsers(APIView):

    """
    Retrieve a list of users with the option of filtering only online users
    """

    def get(self, request):
        online  = request.GET.get('online', None)

        if not online:
            qs = User.objects.filter(is_staff=False)
        else:
            online = string_to_bool(online)
            if type(online) != bool:
                return Response({"error" : "Online query parameter must be either 'true' or 'false'"}, status=status.HTTP_400_BAD_REQUEST)
            qs = User.objects.filter(is_staff=False, online=online)

        if not qs.exists():
            return Response({"message" : "success", "data" : {}})

        user_l = [{"id" : the_user.id, "username" : the_user.username, "online" : the_user.online} for the_user in qs if the_user != request.user]
        return Response({"message" : "success", "data" : user_l})


class MessageHistory(APIView):

    def post(self, request):
        page_param              = request.GET.get('page', '1')
        paginator               = PageNumberPagination()
        paginator.page_size     = 30

        logged_in_user = request.user
        other_user_username = request.data.get('username', "Not Sent")

        if other_user_username == logged_in_user.username:
            return Response({"error": "username cannot be the same as logged in user"}, status=status.HTTP_400_BAD_REQUEST)

        if other_user_username == "Not Sent":
            return Response({"error": "username is required"}, status=status.HTTP_400_BAD_REQUEST)

        thread_obj, new = Thread.objects.get_or_new(logged_in_user, other_user_username)

        if not thread_obj:
            return Response({"error": "Username is invalid"}, status=status.HTTP_400_BAD_REQUEST)
        if new:
            return Response({"error": "User has no message history"}, status=status.HTTP_400_BAD_REQUEST)

        qs = ChatMessage.objects.filter(thread=thread_obj)
        if not qs.exists():
            return Response({"message": {}})

        paginated_qs    = paginator.paginate_queryset(qs, request)
        msg_history     = ChatMessageSerializer(paginated_qs, many=True).data
        data            = {
                            "count" : qs.count(),
                            "count_per_page" : 30,
                            "current_page" : page_param,
                            "payload" : msg_history
                            }
        return Response({"message" : "successful", "data": data}, status=status.HTTP_200_OK)

