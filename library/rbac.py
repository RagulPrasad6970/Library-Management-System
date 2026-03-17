from functools import wraps

from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect

from .models import StaffProfile


ROLE_CAPABILITIES = {
    StaffProfile.Role.ADMIN: {
        "manage_catalog",
        "manage_members",
        "manage_circulation",
        "manage_roles",
    },
    StaffProfile.Role.LIBRARIAN: {
        "manage_catalog",
        "manage_members",
        "manage_circulation",
    },
    StaffProfile.Role.ASSISTANT: {
        "manage_circulation",
    },
    StaffProfile.Role.VIEWER: set(),
}


ROLE_LABELS = {
    StaffProfile.Role.ADMIN: "Administrator",
    StaffProfile.Role.LIBRARIAN: "Librarian",
    StaffProfile.Role.ASSISTANT: "Assistant",
    StaffProfile.Role.VIEWER: "Viewer",
}


def get_user_role(user):
    if not user or not user.is_authenticated:
        return None
    if user.is_superuser:
        return StaffProfile.Role.ADMIN
    try:
        return user.staff_profile.role
    except StaffProfile.DoesNotExist:
        return StaffProfile.Role.VIEWER


def has_capability(user, capability):
    role = get_user_role(user)
    if not role:
        return False
    if user.is_superuser:
        return True
    return capability in ROLE_CAPABILITIES.get(role, set())


def build_access_context(user):
    role = get_user_role(user)
    return {
        "role": role,
        "role_label": ROLE_LABELS.get(role, "Guest"),
        "can_manage_catalog": has_capability(user, "manage_catalog"),
        "can_manage_members": has_capability(user, "manage_members"),
        "can_manage_circulation": has_capability(user, "manage_circulation"),
        "can_manage_roles": has_capability(user, "manage_roles"),
    }


def capability_required(capability):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())
            if not has_capability(request.user, capability):
                messages.error(request, "You do not have permission to perform that action.")
                return redirect("dashboard")
            return view_func(request, *args, **kwargs)

        return wrapped

    return decorator
