# coding:utf-8
from rest_framework.routers import SimpleRouter
from record.views import UserView, VoteRecordView, SubscribeMessageView, StudentView

router = SimpleRouter()
router.register(r'user', UserView)
router.register(r'user/vote', VoteRecordView)
router.register(r'student', StudentView)
router.register(r'subscribe_message', SubscribeMessageView)
urlpatterns = router.urls
