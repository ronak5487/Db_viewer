from django import forms


class DatabaseConnectionForm(forms.Form):
    DB_TYPE_CHOICES = [
        ('postgresql', 'PostgreSQL'),
        ('mysql', 'MySQL'),
        ('sql_server', 'SQL Server'),
    ]
    db_type = forms.ChoiceField(choices=DB_TYPE_CHOICES, label="Database Type")
    host = forms.CharField(max_length=100, label="Host")
    port = forms.IntegerField(label="Port")
    username = forms.CharField(max_length=100, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    database_name = forms.CharField(max_length=100, label="Database Name")
