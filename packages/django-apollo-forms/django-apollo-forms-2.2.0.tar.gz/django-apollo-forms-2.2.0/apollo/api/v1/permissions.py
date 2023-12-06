from rest_framework import permissions


class FormSubmissionsPermission(permissions.DjangoModelPermissions):
    """ form submissions may be viewed by staff only, but are open for creation by anyone """
    message = 'Only users with perms may view/modify form submissions'

    def has_permission(self, request, view):
        # anyone can create a form submission
        if request.method == 'POST':
            return True

        has_modify_perms = super(FormSubmissionsPermission, self).has_permission(request, view)
        has_read_perms = request.user.has_perm('apollo.can_view_submissions')

        return has_modify_perms if request.method != 'GET' else has_read_perms

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # view-level has_permission already takes care of read perms
            return True

        # for updating objects, we only want to allow the creator of the form submission to update it
        return hasattr(request, 'user') and request.user is not None and not request.user.is_anonymous and obj.created_by == request.user
