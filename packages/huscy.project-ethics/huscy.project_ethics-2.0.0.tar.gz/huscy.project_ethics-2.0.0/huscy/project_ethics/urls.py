from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from huscy.project_ethics import views
from huscy.projects.urls import project_router


router = DefaultRouter()
router.register('ethicscommittees', views.EthicsCommitteeViewSet)

project_router.register('ethics', views.EthicsViewSet, basename='ethics')

ethics_router = NestedDefaultRouter(project_router, 'ethics', lookup='ethics')
ethics_router.register('ethicsfiles', views.EthicsFileViewSet, basename='ethicsfile')


urlpatterns = [
    path('api/', include(router.urls + project_router.urls + ethics_router.urls)),
]
