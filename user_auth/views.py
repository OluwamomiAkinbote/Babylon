from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from user_auth.models import NewsUser, Interest, ComposeNews
from user_auth.serializers import ComposeNewsSerializer, NewsUserSerializer
import uuid
from user_auth.serializers import InterestSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.http import JsonResponse


# Register Step 1 (with CSRF protection)
@method_decorator(csrf_protect, name='dispatch')
class RegisterStepOneView(APIView):
    def post(self, request):
        data = request.data
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        agreement = data.get('agreement')

        if not agreement:
            return Response({"error": "You must agree to the terms and policy."}, status=status.HTTP_400_BAD_REQUEST)

        if password != confirm_password:
            return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        if NewsUser.objects.filter(email=email).exists():
            return Response({"error": "Email already registered."}, status=status.HTTP_400_BAD_REQUEST)

        # Temporary save in session or return data for frontend to move to next step
        request.session['register_step_one'] = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password
        }

        return Response({"message": "Step 1 complete. Proceed to Step 2."}, status=status.HTTP_200_OK)


# Register Step 2 (with interests serialization)
@method_decorator(csrf_protect, name='dispatch')
class RegisterStepTwoView(APIView):
    def post(self, request):
        step_one_data = request.session.get('register_step_one')

        if not step_one_data:
            return Response({"error": "Step 1 data missing. Please start again."}, status=status.HTTP_400_BAD_REQUEST)

        bio = request.data.get('bio')
        profile_image = request.data.get('profile_image')
        interest_ids = request.data.get('interests', [])

        user = NewsUser.objects.create(
            id=uuid.uuid4(),
            username=step_one_data['email'].split('@')[0],
            email=step_one_data['email'],
            first_name=step_one_data['first_name'],
            last_name=step_one_data['last_name'],
            password=make_password(step_one_data['password']),
            bio=bio,
            profile_image=profile_image
        )

        if interest_ids:
            interests = Interest.objects.filter(id__in=interest_ids)
            user.interests.set(interests)

        user.save()

        # Clear session
        request.session.pop('register_step_one', None)

        # Return the user data along with interests
        user_serializer = NewsUserSerializer(user)
        return Response({"message": "Registration completed. You can now sign in.", "user": user_serializer.data}, status=status.HTTP_201_CREATED)


# Sign In (remains unchanged)
@method_decorator(csrf_protect, name='dispatch')
class SignInView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = NewsUser.objects.get(email=email)
            if user.check_password(password):
                # Fake token / session set up for frontend (you can improve later)
                return Response({
                    "message": "Login successful",
                    "redirect_url": "/my-news",
                    "user_id": str(user.id),
                    "username": user.username,
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        except NewsUser.DoesNotExist:
            return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)


# My News Timeline (based on interests)
@method_decorator(csrf_protect, name='dispatch')
class MyNewsTimelineView(APIView):
    def get(self, request, user_id):
        try:
            user = NewsUser.objects.get(id=user_id)
            interests = user.interests.all()

            # Fetch ComposeNews based on matching interests
            news_posts = ComposeNews.objects.filter(
                author__interests__in=interests
            ).distinct()

            # Serialize news posts including author details
            serializer = ComposeNewsSerializer(news_posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except NewsUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)


# Interest ViewSet for listing, retrieving, creating, and updating interests
@method_decorator(csrf_protect, name='dispatch')
class InterestViewSet(viewsets.ModelViewSet):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer

    def list(self, request):
        interests = self.get_queryset()
        serializer = self.get_serializer(interests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({"message": "CSRF cookie set."})