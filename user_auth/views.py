from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.contrib.auth.hashers import make_password
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Member, Interest
from .serializers import MemberSerializer, InterestSerializer
import re
from django.urls import reverse
import uuid
from django.shortcuts import redirect

# Register Step 1
@method_decorator(csrf_protect, name='dispatch')
class RegisterStepOneView(APIView):
    @require_http_methods(["POST"])
    def post(self, request):
        data = request.data
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        email = data.get('email', '').lower().strip()
        password = data.get('password', '')
        confirm_password = data.get('confirm_password', '')
        agreement = data.get('agreement', False)

        # Validation checks
        errors = {}

        if not first_name:
            errors['first_name'] = "First name is required"
        elif len(first_name) > 50:
            errors['first_name'] = "First name too long (max 50 characters)"

        if not last_name:
            errors['last_name'] = "Last name is required"
        elif len(last_name) > 50:
            errors['last_name'] = "Last name too long (max 50 characters)"

        if not email:
            errors['email'] = "Email is required"
        elif not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            errors['email'] = "Enter a valid email address"
        elif len(email) > 100:
            errors['email'] = "Email too long (max 100 characters)"
        elif Member.objects.filter(email=email).exists():
            errors['email'] = "Email already registered"

        if not password:
            errors['password'] = "Password is required"
        elif len(password) < 8:
            errors['password'] = "Password must be at least 8 characters"

        if password != confirm_password:
            errors['confirm_password'] = "Passwords do not match"

        if not agreement:
            errors['agreement'] = "You must agree to the terms and policy"

        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        # Store minimal data in session
        request.session['register_step_one'] = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": make_password(password)  # Store hashed password instead of plain text
        }
        request.session.modified = True  # Ensure session is saved

        return Response({
            "message": "Step 1 completed successfully",
            "redirect_url": reverse('register-step-two')  # Use Django's reverse to get URL
        }, status=status.HTTP_200_OK)


# Register Step 2
@method_decorator(csrf_protect, name='dispatch')
class RegisterStepTwoView(APIView):
    def post(self, request):
        step_one_data = request.session.get('register_step_one')

        if not step_one_data:
            return Response({"error": "Step 1 data missing. Please start again."}, status=status.HTTP_400_BAD_REQUEST)

        bio = request.data.get('bio')
        profile_image = request.data.get('profile_image')
        interest_ids = request.data.get('interests', [])

        # Create user
        user = Member.objects.create(
            id=uuid.uuid4(),
            username=step_one_data['email'].split('@')[0],
            email=step_one_data['email'],
            first_name=step_one_data['first_name'],
            last_name=step_one_data['last_name'],
            password=make_password(step_one_data['password']),
            bio=bio,
            profile_image=profile_image
        )

        # Set user interests
        if interest_ids:
            interests = Interest.objects.filter(id__in=interest_ids)
            user.interests.set(interests)

        user.save()

        request.session.pop('register_step_one', None)  # Clear session data after completion

        user_serializer = MemberSerializer(user)
        return Response({"message": "Registration completed. You can now sign in.", "user": user_serializer.data}, status=status.HTTP_201_CREATED)


# Sign In - Updated View
@method_decorator([ensure_csrf_cookie, csrf_protect], name='dispatch')
class SignInView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = Member.objects.get(email=email)
            if user.check_password(password):
                request.session['user_id'] = str(user.id)
                return Response({
                    "message": "Login successful",
                    "redirect_url": "/my-news",  # Redirect after login
                    "user_id": str(user.id),
                    "username": user.username,
                }, status=status.HTTP_200_OK)
            else:
                return Response({"password": "Incorrect password."}, status=status.HTTP_401_UNAUTHORIZED)
        except Member.DoesNotExist:
            return Response({"email": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)


# Timeline View
class MyNewsTimelineView(APIView):
    def get(self, request, user_id):
        try:
            user = Member.objects.get(id=user_id)
            interests = user.interests.all()
            serializer = InterestSerializer(interests, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Member.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)


# Interest ViewSet
@method_decorator(csrf_protect, name='dispatch')
class InterestViewSet(viewsets.ModelViewSet):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer


# CSRF Token Set
@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({"message": "CSRF cookie set."})
