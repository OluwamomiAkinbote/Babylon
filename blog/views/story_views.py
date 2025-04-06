from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from blog.models import Story, StoryMedia
from blog.serializers import StorySerializer, StoryMediaSerializer
from datetime import timedelta


class StoryListCreateAPIView(APIView):

    def get(self, request):
        # List all stories
        stories = Story.objects.all()
        serializer = StorySerializer(stories, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Create a new story
        serializer = StorySerializer(data=request.data)
        if serializer.is_valid():
            story = serializer.save(user=request.user)
            # Set expiration date to 3 days after creation (using 'date' field)
            story.expires_at = story.date + timedelta(days=3)
            story.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StoryDetailAPIView(APIView):
   

    def get_object(self, pk):
        try:
            return Story.objects.get(pk=pk)
        except Story.DoesNotExist:
            return None

    def get(self, request, pk):
        story = self.get_object(pk)
        if story is None:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StorySerializer(story)
        return Response(serializer.data)

    def put(self, request, pk):
        story = self.get_object(pk)
        if story is None:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StorySerializer(story, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        story = self.get_object(pk)
        if story is None:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        story.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StoryMediaListCreateAPIView(APIView):
   

    def get(self, request):
        # List all story media
        media = StoryMedia.objects.all()
        serializer = StoryMediaSerializer(media, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Create new media for a story
        serializer = StoryMediaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StoryMediaDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return StoryMedia.objects.get(pk=pk)
        except StoryMedia.DoesNotExist:
            return None

    def get(self, request, pk):
        media = self.get_object(pk)
        if media is None:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StoryMediaSerializer(media)
        return Response(serializer.data)

    def put(self, request, pk):
        media = self.get_object(pk)
        if media is None:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StoryMediaSerializer(media, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        media = self.get_object(pk)
        if media is None:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        media.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
