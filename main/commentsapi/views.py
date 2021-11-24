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
from .serializers import BookCommentsSerializer, BookCommentActionSerializer

from main.models import Book, Comment
ALLOWED_HOSTS = settings.ALLOWED_HOSTS


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def BookCommentActionView(request,book_pk, *args, **kwargs):
    serializer = BookCommentActionSerializer(data=request.data, context={"request":request})
    if serializer.is_valid(raise_exception=True):
        data = serializer.data
        action = data['action']
        try:
            id = data['id']
            qs = Comment.objects.filter(id=id)
            if not qs.exists():
                return Response({}, status=404)
            obj = qs.first()
            if action == "like":
                obj.likes.add(request.user)
                # notification = Notification.objects.create(type='like',notification_type=1, from_user=request.user, to_user=obj.author, status=obj)
                serializer = BookCommentsSerializer(obj, context={"request":request})
                return Response(serializer.data, status=200)
            elif action == "unlike":
                obj.likes.remove(request.user)
                serializer = BookCommentsSerializer(obj, context={"request":request})
                return Response(serializer.data, status=200)
            elif action == "reply":
                try :
                    body = data['body']
                except KeyError:
                    body = obj.body
                new_status = Comment.objects.create(book_id=book_pk,author=request.user, body=body, parent=obj)
                serializer = BookCommentsSerializer(new_status, context={"request":request})
                return Response(serializer.data, status=200)
        except KeyError:
            pass
        if action == "create":
            try :
                body = data['body']
            except KeyError:
                return Response({"keyerror": 'missing file'})
            new_status = Comment.objects.create(book_id=book_pk,author=request.user, body=body)
            # notification = Notification.objects.create(type='share',notification_type=5, from_user=request.user, to_user=obj.author, status=obj)
            serializer = BookCommentsSerializer(new_status, context={"request":request})
            return Response(serializer.data, status=200)
    return Response({}, status=200)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def CommentListView(request, book_pk,*args, **kwargs):
    qs = Book.objects.filter(pk=book_pk).first()
    comments = qs.comments.all().order_by('-date_added')
    serializer = BookCommentsSerializer(comments, many=True, context={"request":request})
    return Response(serializer.data)