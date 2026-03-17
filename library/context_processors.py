from .rbac import build_access_context


def rbac(request):
    return {
        "rbac": build_access_context(request.user),
    }
