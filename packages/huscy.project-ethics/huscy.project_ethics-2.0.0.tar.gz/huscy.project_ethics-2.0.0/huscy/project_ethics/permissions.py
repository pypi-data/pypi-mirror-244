from rest_framework.permissions import BasePermission, SAFE_METHODS

from huscy.projects.models import Membership


class IsProjectCoordinator(BasePermission):
    '''
    this class is temporarily required due to override the `has_object_permission`. In drf versions
    lower than 3.14 the `has_permission` method is not called when checking for object permissions.
    That means, this class can be removed when drf 3.13 is not supported anymore and the
    `IsProjectCoordinator` permission from huscy.projects can be used.
    '''

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        return Membership.objects.filter(project=view.project, user=request.user,
                                         is_coordinator=True).exists()

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class ChangeProjectPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if not any([request.user.has_perm('projects.change_project'),
                    request.user.has_perm('projects.change_project', view.project)]):
            return False

        return True

    def has_object_permission(self, request, view, obj):
        '''
        with drf version 3.14 this method can be simplified to
        `return self.has_permission(request, view)`
        '''
        if not any([request.user.has_perm('projects.change_project'),
                    request.user.has_perm('projects.change_project', view.project)]):
            return False

        return True


class DeleteEthicsFilePermission(BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if not any([request.user.has_perm('projects.change_project'),
                    request.user.has_perm('projects.change_project', view.project)]):
            return False

        if request.method == 'DELETE':
            return request.user.has_perm('project_ethics.delete_ethicsfile')

        return True
