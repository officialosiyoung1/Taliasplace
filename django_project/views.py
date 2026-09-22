import logging
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

logger = logging.getLogger(__name__)

@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check and auto-migration endpoint.
    Verifies database connectivity, checks for unapplied migrations,
    and automatically applies any missing migrations if necessary.
    """
    data = {
        "status": "healthy",
        "database": "unknown",
        "unapplied_migrations": [],
    }

    # 1. Test database connection
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        data["database"] = "connected"
    except Exception as exc:
        data["database"] = f"error: {str(exc)}"
        data["status"] = "degraded"

    # 2. Check and auto-apply migrations if pending
    try:
        from django.db.migrations.executor import MigrationExecutor
        from django.db import DEFAULT_DB_ALIAS, connections
        executor = MigrationExecutor(connections[DEFAULT_DB_ALIAS])
        plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
        if plan:
            pending_names = [f"{mig.app_label}.{mig.name}" for mig, _ in plan]
            data["unapplied_migrations"] = pending_names
            data["status"] = "migrating"

            from django.core.management import call_command
            call_command("migrate", interactive=False)
            data["status"] = "healthy"
            data["auto_migrated"] = True
            logger.info(f"Auto-applied pending migrations: {pending_names}")
    except Exception as exc:
        data["migration_error"] = str(exc)
        logger.error(f"Migration check/application failed: {exc}", exc_info=True)

    return Response(data)
