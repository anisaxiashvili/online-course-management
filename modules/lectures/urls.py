from rest_framework.routers import DefaultRouter
from .views import LectureViewSet, HomeworkAssignmentViewSet, SubmissionViewSet, GradeViewSet, GradeCommentViewSet

router = DefaultRouter()
router.register(r'lectures', LectureViewSet, basename='lecture')
router.register(r'assignments', HomeworkAssignmentViewSet, basename='assignment')
router.register(r'submissions', SubmissionViewSet, basename='submission')
router.register(r'grades', GradeViewSet, basename='grade')
router.register(r'grade-comments', GradeCommentViewSet, basename='grade-comment')

urlpatterns = router.urls
