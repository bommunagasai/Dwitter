from django.conf.urls import url, include

from rest_framework import routers
from views import AccountViewSet, DweetViewSet
router = routers.DefaultRouter()


router.register('users', AccountViewSet)

router.register('dweets', DweetViewSet)

urlpatterns = [
    url(r'', include(router.urls))
]