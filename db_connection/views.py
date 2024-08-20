from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import SQLAlchemyError
from urllib.parse import quote_plus
from .serializers import DatabaseConnectionSerializer


class DatabaseMetadataAPIView(APIView):
    def post(self, request):
        serializer = DatabaseConnectionSerializer(data=request.data)
        if serializer.is_valid():
            db_type = serializer.validated_data['db_type']
            user = serializer.validated_data['username']
            password = serializer.validated_data['password']
            host = serializer.validated_data['host']
            port = serializer.validated_data['port']
            database = serializer.validated_data['database_name']

            try:
                encoded_password = quote_plus(password)
                engine_url = ""

                if db_type == 'PostgreSQL':
                    engine_url = f'postgresql://{user}:{encoded_password}@{host}:{port}/{database}'
                elif db_type == 'MySQL':
                    engine_url = f'mysql+pymysql://{user}:{encoded_password}@{host}:{port}/{database}'
                elif db_type == 'SQLite':
                    engine_url = f'sqlite:///{database}'
                elif db_type == 'Oracle':
                    engine_url = f'oracle://{user}:{encoded_password}@{host}:{port}/{database}'
                elif db_type == 'MSSQL':
                    engine_url = f'mssql+pyodbc://{user}:{encoded_password}@{host}:{port}/{database}?driver=ODBC+Driver+17+for+SQL+Server'

                engine = create_engine(engine_url)
                metadata = MetaData()
                metadata.reflect(bind=engine)

                metadata_info = {}
                for schema in metadata.tables.values():
                    schema_name = schema.schema or "default"
                    if schema_name not in metadata_info:
                        metadata_info[schema_name] = {}
                    table_name = schema.name
                    columns = [col.name for col in schema.columns]
                    metadata_info[schema_name][table_name] = columns

                return Response({'metadata': metadata_info}, status=status.HTTP_200_OK)

            except SQLAlchemyError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
