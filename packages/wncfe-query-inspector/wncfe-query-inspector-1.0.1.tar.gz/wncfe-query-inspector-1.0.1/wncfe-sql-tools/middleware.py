from django.db import connection
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import SqlLexer
from sqlparse import format
from django.conf import settings
from decimal import Decimal


def new_middleware(get_response):

    def middleware(request):
        response = get_response(request)
        
        if settings.DEBUG:
            number_queries = len(connection.queries)
            duplicates = set()
            total_excecution_time = Decimal()
            
            for query in connection.queries:
                total_excecution_time += Decimal(query['time'])
                duplicates.add(query['sql'])
                
                sqlformatted = format(str(query["sql"]), reindent=True)
                print(highlight(sqlformatted, SqlLexer(), TerminalFormatter()))

        print('==========')
        print('[SQL Stats]')
        print(f'{number_queries} Total Queries')
        print(f'{number_queries - len(duplicates)} Total Duplicates')
        print(f'{total_excecution_time} Execution time')
        print('==========')
        
        return response

    return middleware