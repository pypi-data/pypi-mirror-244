from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from reversion import set_comment
from reversion.views import RevisionMixin

from huscy.projects.models import Project
from huscy.project_ethics import serializer
from huscy.project_ethics.models import Ethics
from huscy.project_ethics.permissions import (
    ChangeProjectPermission,
    DeleteEthicsFilePermission,
    IsProjectCoordinator,
)
from huscy.project_ethics.services import get_ethics_files, get_ethics, get_ethics_committees


class EthicsCommitteeViewSet(RevisionMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                             mixins.ListModelMixin, mixins.UpdateModelMixin,
                             viewsets.GenericViewSet):
    http_method_names = 'delete', 'head', 'get', 'options', 'post', 'put'
    permission_classes = (DjangoModelPermissions, )
    queryset = get_ethics_committees()
    serializer_class = serializer.EthicsCommitteeSerializer

    def perform_create(self, serializer):
        ethics_committee = serializer.save()
        set_comment(f'Created ethics committee "{ethics_committee.name}"')

    def perform_destroy(self, ethics_committee):
        ethics_committee.delete()
        set_comment(f'Deleted ethics committee "{ethics_committee.name}"')

    def perform_update(self, serializer):
        ethics_committee = serializer.save()
        set_comment(f'Updated ethics committee "{ethics_committee.name}"')


class EthicsViewSet(RevisionMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                    mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    http_method_names = 'delete', 'head', 'get', 'options', 'post', 'put'
    permission_classes = IsAuthenticated, ChangeProjectPermission
    serializer_class = serializer.EthicsSerializer

    def initial(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        super().initial(request, *args, **kwargs)

    def get_queryset(self):
        return get_ethics(self.project)

    def perform_create(self, serializer):
        ethics = serializer.save(project=self.project)
        set_comment(f'Created ethics <ID-{ethics.id}>')

    def perform_destroy(self, ethics):
        ethics.delete()
        set_comment(f'Deleted ethics <ID-{ethics.id}>')

    def perform_update(self, serializer):
        ethics = serializer.save()
        set_comment(f'Updated ethics <ID-{ethics.id}>')


class EthicsFileViewSet(RevisionMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                        mixins.UpdateModelMixin, viewsets.GenericViewSet):
    http_method_names = 'delete', 'head', 'options', 'post', 'put'
    permission_classes = (
        IsAuthenticated,
        IsProjectCoordinator | (ChangeProjectPermission & DeleteEthicsFilePermission),
    )

    def initial(self, request, *args, **kwargs):
        self.ethics = get_object_or_404(Ethics.objects.select_related('project'),
                                        pk=self.kwargs['ethics_pk'],
                                        project=self.kwargs['project_pk'])
        self.project = self.ethics.project
        super().initial(request, *args, **kwargs)

    def get_queryset(self):
        return get_ethics_files(self.ethics)

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return serializer.UpdateEthicsFileSerializer
        return serializer.EthicsFileSerializer

    def perform_create(self, serializer):
        ethics_file = serializer.save(ethics=self.ethics, creator=self.request.user)
        set_comment(f'Created ethics file <ID-{ethics_file.id}>')

    def perform_destroy(self, ethics_file):
        ethics_file.delete()
        set_comment(f'Deleted ethics file <ID-{ethics_file.id}>')

    def perform_update(self, serializer):
        ethics_file = serializer.save()
        set_comment(f'Updated ethics file <ID-{ethics_file.id}>')
