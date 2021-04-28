from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from news_board.models import Post, Comment


@api_view(['GET', 'POST', 'DELETE'])
def post_view(request: Request):
    if request.method == 'GET':
        try:
            limit = int(request.data.get('limit', 10))
            offset = int(request.data.get('offset', 0))
        except ValueError:
            return Response(
                {'message': 'Arguments type is not supported'},
                status=status.HTTP_400_BAD_REQUEST
            )

        posts = Post.objects.all()[offset:offset + limit]

        return Response([post.to_dict() for post in posts])

    elif request.method == 'POST':
        title = request.data.get('title', None)
        link = request.data.get('link', None)

        if not title or not link:
            return Response(
                {'message': 'Arguments not found'},
                status=status.HTTP_400_BAD_REQUEST
            )

        Post.objects.create(title=title, link=link, author=request.user).save()
        return Response('Post created successfully')

    elif request.method == 'DELETE':
        try:
            pk = int(request.data.get('id', None))
        except ValueError:
            return Response(
                {'message': 'Arguments type is not supported'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except TypeError:
            return Response(
                {'message': 'Id is not provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            Post.objects.get(pk=pk).delete()
        except Post.DoesNotExist:
            return Response(
                {'message': 'No such post'}, status=status.HTTP_404_NOT_FOUND
            )
        return Response('Post deleted successfully')


@api_view(['GET', 'POST', 'DELETE'])
def comment_view(request: Request):
    if request.method == 'GET':
        try:
            post = int(request.data.get('id', None))
        except ValueError:
            return Response(
                {'message': 'Arguments type is not supported'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except TypeError:
            return Response(
                {'message': 'Id is not provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            limit = int(request.data.get('limit', 10))
            offset = int(request.data.get('offset', 0))
        except ValueError:
            return Response(
                {'message': 'Arguments type is not supported'},
                status=status.HTTP_400_BAD_REQUEST
            )

        comments = Comment.objects.filter(post_id=post)[offset:offset + limit]

        return Response([comment.to_dict() for comment in comments])

    elif request.method == 'POST':
        try:
            post = int(request.data.get('id', None))
        except ValueError:
            return Response(
                {'message': 'Arguments type is not supported'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except TypeError:
            return Response(
                {'message': 'Id is not provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            post = Post.objects.get(pk=post)
        except Post.DoesNotExist:
            return Response(
                {'message': 'No such post'}, status=status.HTTP_404_NOT_FOUND
            )
        content = request.data.get('text', None)

        if not content:
            return Response(
                {'message': 'Arguments not found'},
                status=status.HTTP_400_BAD_REQUEST
            )

        Comment.objects.create(content=content,
                               post=post,
                               author=request.user).save()
        return Response('Comment created successfully')

    elif request.method == 'DELETE':
        try:
            pk = int(request.data.get('id', None))
        except ValueError:
            return Response(
                {'message': 'Arguments type is not supported'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except TypeError:
            return Response(
                {'message': 'Id is not provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            Comment.objects.get(pk=pk).delete()
        except Comment.DoesNotExist:
            return Response(
                {'message': 'No such comment'}, status=status.HTTP_404_NOT_FOUND
            )
        return Response('Comment deleted successfully')


@api_view(['POST'])
def upvote_view(request: Request):
    try:
        post = int(request.data.get('id', None))
    except ValueError:
        return Response(
            {'message': 'Arguments type is not supported'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except TypeError:
        return Response(
            {'message': 'Id is not provided'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = request.user
    try:
        post = Post.objects.get(pk=post)
    except Post.DoesNotExist:
        return Response({'message': 'No such post'},
                        status=status.HTTP_404_NOT_FOUND)
    if user.is_authenticated:
        if user in post.upvotes.all():
            post.upvotes.remove(user)
            return Response('Devoted the post')
        else:
            post.upvotes.add(user)
            return Response('Upvoted the post')
