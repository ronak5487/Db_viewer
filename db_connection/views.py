from django.conf import settings
from django.db import connections, OperationalError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


def connection(request):
    # Add dynamic database configuration with required settings
    settings.DATABASES['dynamic'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test_project',
        'USER': 'postgres',
        'PASSWORD': 'Ronak@123',
        'HOST': 'localhost',
        'PORT': request.port,
        'TIME_ZONE': 'UTC',
        'ATOMIC_REQUESTS': False,
        'CONN_MAX_AGE': 0,  # Add this line
        'CONN_HEALTH_CHECKS': False,
        'OPTIONS': {},
        'AUTOCOMMIT': True  # Add this line
    }

    try:
        with connections['dynamic'].cursor() as cursor:
            # Fetch tables
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            tables = cursor.fetchall()

            metadata = {}
            for table in tables:
                table_name = table[0]
                cursor.execute(
                    f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}'")
                columns = cursor.fetchall()
                metadata[table_name] = columns

            return JsonResponse(metadata)
    except OperationalError as e:
        return HttpResponse(f"Error: {e}", status=500)
