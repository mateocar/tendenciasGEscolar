from rest_framework.routers import DefaultRouter
from django.urls import path, include
from ..users.views import UserRegistrationView, UserLoginView, AuthenticatedUserView
from ..roles.views import RolesViewSet
from ..courses.views import CourseViewSet
from ..grades.views import GradeViewSet
from ..students.views import StudentViewSet
from ..teachers.views import TeacherViewSet
from ..schedules.views import ScheduleViewSet

router = DefaultRouter()

router.register(r'roles', RolesViewSet, basename='roles')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'grades', GradeViewSet, basename='grade')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'teachers', TeacherViewSet, basename='teacher')
router.register(r'schedule', ScheduleViewSet, basename='schedule')

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='usuario-register'),
    path('login/', UserLoginView.as_view(), name='usuario-login'),
    path('checkAuth/', AuthenticatedUserView.as_view(), name='checkauth'),
    path('', include((router.urls)))
]