from rest_framework import serializers


class DatabaseConnectionSerializer(serializers.Serializer):
    db_type = serializers.ChoiceField(choices=[('PostgreSQL', 'PostgreSQL'), ('MySQL', 'MySQL'), ('MSSQL', 'MSSQL')])
    host = serializers.CharField(max_length=100)
    port = serializers.IntegerField()
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100,
                                     write_only=True)  # write_only to avoid sending it back in responses
    database_name = serializers.CharField(max_length=100)
