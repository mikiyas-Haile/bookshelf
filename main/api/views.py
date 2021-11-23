from rest_framework.serializers import Serializer
from django.conf import settings
from django.db.models.aggregates import Count
from rest_framework.authentication import TokenAuthentication

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db.models import Max
from rest_framework import (generics, filters)
from .serializers import BookSerializer,BookActionSerializer

from main.models import Book
ALLOWED_HOSTS = settings.ALLOWED_HOSTS

class BookListView(generics.ListCreateAPIView):
    search_fields = ['author__username', 'author__first_name', 'author__last_name']
    filter_backends = (filters.SearchFilter,)
    queryset = Book.objects.annotate(num_likess=Count('likes')).order_by('-num_likess')
    serializer_class = BookSerializer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def BookDetailView(request, book_id, *args, **kwargs):
    qs = Book.objects.filter(id= book_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = BookSerializer(obj, context={"request":request})
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def BookActionView(request, *args, **kwargs):
    serializer = BookActionSerializer(data=request.data, context={"request":request})
    if serializer.is_valid(raise_exception=True):
        data = serializer.data
        action = data['action']
        try :
            status_id = data['id']
            qs = Book.objects.filter(id=status_id)
            if not qs.exists():
                return Response({}, status=404)
            obj = qs.first()
            if action == "like":
                obj.likes.add(request.user)
                # notification = Notification.objects.create(type='like',notification_type=1, from_user=request.user, to_user=obj.author, status=obj)
                serializer = BookSerializer(obj, context={"request":request})
                return Response(serializer.data, status=200)
            elif action == "unlike":
                obj.likes.remove(request.user)
                serializer = BookSerializer(obj, context={"request":request})
                return Response(serializer.data, status=200)
        except KeyError:
            pass
        if action == "create":
            try :
                body = data['body']
                title = data['title']
                discription = data['discription']
            except KeyError:
                return Response({"keyerror": 'missing file'})
            new_status = Book.objects.create(author=request.user,title=title,discription=discription, body=body)
            # notification = Notification.objects.create(type='share',notification_type=5, from_user=request.user, to_user=obj.author, status=obj)
            serializer = BookSerializer(new_status, context={"request":request})
            return Response(serializer.data, status=200)
    return Response({}, status=200)

