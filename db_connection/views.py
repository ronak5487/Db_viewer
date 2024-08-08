from django.shortcuts import render
from .forms import DatabaseConnectionForm
import psycopg2  # For PostgreSQL, or another DB-API module for your DB


def home(request):
    form = DatabaseConnectionForm()
    metadata = None
    error = None
    show_modal = False

    if request.method == 'POST':
        form = DatabaseConnectionForm(request.POST)
        show_modal = True  # Show modal when the form is submitted
        if form.is_valid():
            show_modal = False  # Hide modal if the form is valid
            try:
                # (Assuming PostgreSQL)
                conn = psycopg2.connect(
                    host=form.cleaned_data['host'],
                    port=form.cleaned_data['port'],
                    user=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],
                    dbname=form.cleaned_data['database_name']
                )
                cur = conn.cursor()
                cur.execute("SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema NOT IN ('information_schema', 'pg_catalog')")
                tables = cur.fetchall()
                metadata = {}
                for table_schema, table_name in tables:
                    cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_schema = %s AND table_name = %s", (table_schema, table_name))
                    columns = cur.fetchall()
                    if table_schema not in metadata:
                        metadata[table_schema] = {}
                    metadata[table_schema][table_name] = [col[0] for col in columns]
                cur.close()
                conn.close()
            except Exception as e:
                error = str(e)

    return render(request, 'home.html', {
        'form': form,
        'metadata': metadata,
        'error': error,
        'show_modal': show_modal,
    })
