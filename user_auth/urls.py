from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterStepOneView,
    RegisterStepTwoView,
    SignInView,
    MyNewsTimelineView,
    InterestViewSet,
    get_csrf_token
)

# Router for InterestViewSet
router = DefaultRouter()
router.register(r'interests', InterestViewSet, basename='interests')

urlpatterns = [
    path('register/step-one/', RegisterStepOneView.as_view(), name='register-step-one'),
    path('register/step-two/', RegisterStepTwoView.as_view(), name='register-step-two'),
    path('signin/', SignInView.as_view(), name='sign-in'),
    path('my-news/<uuid:user_id>/', MyNewsTimelineView.as_view(), name='my-news'),
    path('get-csrf-token/', get_csrf_token, name='get-csrf-token'),

    # Router URLs for interests
    path('', include(router.urls)),
]
