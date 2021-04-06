import sqlite3
from social_site import settings
import pyodbc
import re

class EventsGetter:
    #AZURE SETTINGS
    server = 'tcp:betmatcher.database.windows.net' 
    database = 'betmatcher' 
    username = 'azureadmin' 
    password = 'xcazU7qpal3.' 
    driver= '{ODBC Driver 17 for SQL Server}'
    params = f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
    
    #AZURE TABLES
    BET_MATCHES_TWO_OUTCOMES_TABLE = "bet_matches_two_outcomes"
    BET_MATCHES_THREE_OUTCOMES_TABLE = "bet_matches_three_outcomes"

    #AZURE QUERY
    SQL_GET_AVAILABLE_BOOKMAKERS = "SELECT DISTINCT bookmaker FROM scraping_results ORDER BY bookmaker"
    SQL_GET_TWO_OUTCOMES_AVAILABLE_BETS = "SELECT DISTINCT bet1 FROM bet_matches_two_outcomes ORDER BY bet1"
    SQL_GET_THREE_OUTCOMES_AVAILABLE_BETS = "SELECT DISTINCT bet1 FROM bet_matches_three_outcomes ORDER BY bet1"

    #SQLITE
    DB_NAME = "TESTbetmatcher.db"
    TABEL_NAME = "test_multiple_spiders"
    
    AVAILABLE_BOOKS = []

    TWO_OUTCOMES_AVAILABLE_BETS = []
    THREE_OUTCOMES_AVAILABLE_BETS = []

    # @classmethod
    # def get_available_books(cls):
    #     if not cls.AVAILABLE_BOOKS:
    #         azure_connection = pyodbc.connect(cls.params)
    #         azure_cursor = azure_connection.cursor()
    #         azure_cursor.execute(cls.SQL_GET_AVAILABLE_BOOKMAKERS)
    #         cls.AVAILABLE_BOOKS = [f"{s1[0]}" for s1 in azure_cursor.fetchall()]
    #         azure_cursor.close()
    #         azure_connection.close()
    #     return cls.AVAILABLE_BOOKS
    
    @classmethod
    def get_available_bookmakers(cls):
        if not cls.AVAILABLE_BOOKS:
            azure_connection = pyodbc.connect(cls.params)
            azure_cursor = azure_connection.cursor()
            azure_cursor.execute(cls.SQL_GET_AVAILABLE_BOOKMAKERS)
            cls.AVAILABLE_BOOKS = tuple((f"{s1[0]}", f"{s1[0]}") for s1 in azure_cursor.fetchall())
            azure_cursor.close()
            azure_connection.close()
        return cls.AVAILABLE_BOOKS
    
    @classmethod
    def get_available_bets(cls, table_number):
        if not cls.TWO_OUTCOMES_AVAILABLE_BETS or not cls.THREE_OUTCOMES_AVAILABLE_BETS:    #se uno dei due non c'è, popolo entrambi
            azure_connection = pyodbc.connect(cls.params)
            azure_cursor = azure_connection.cursor()
            azure_cursor.execute(cls.SQL_GET_TWO_OUTCOMES_AVAILABLE_BETS)
            cls.TWO_OUTCOMES_AVAILABLE_BETS = tuple((f"{s1[0]}", f"{s1[0]}") for s1 in azure_cursor.fetchall())
            azure_cursor.execute(cls.SQL_GET_THREE_OUTCOMES_AVAILABLE_BETS)
            cls.THREE_OUTCOMES_AVAILABLE_BETS = tuple((f"{s1[0]}", f"{s1[0]}") for s1 in azure_cursor.fetchall())
            azure_cursor.close()
            azure_connection.close()
        if table_number == 2:
            return cls.TWO_OUTCOMES_AVAILABLE_BETS
        else:
            return cls.THREE_OUTCOMES_AVAILABLE_BETS

    # @classmethod
    # def get_available_bets(cls, table_number):
    #     if not cls.TWO_OUTCOMES_AVAILABLE_BETS or not cls.THREE_OUTCOMES_AVAILABLE_BETS:    #se uno dei due non c'è, popolo entrambi
    #         azure_connection = pyodbc.connect(cls.params)
    #         azure_cursor = azure_connection.cursor()
    #         azure_cursor.execute(cls.SQL_GET_TWO_OUTCOMES_AVAILABLE_BETS)
    #         cls.TWO_OUTCOMES_AVAILABLE_BETS = [f"{s1[0]}" for s1 in azure_cursor.fetchall()]
    #         azure_cursor.execute(cls.SQL_GET_THREE_OUTCOMES_AVAILABLE_BETS)
    #         cls.THREE_OUTCOMES_AVAILABLE_BETS = [f"{s1[0]}" for s1 in azure_cursor.fetchall()]
    #         azure_cursor.close()
    #         azure_connection.close()
    #     if table_number == 2:
    #         return cls.TWO_OUTCOMES_AVAILABLE_BETS
    #     else:
    #         return cls.THREE_OUTCOMES_AVAILABLE_BETS
        
        
    @classmethod
    def get_matches(cls, table_number, **filters): #filters are passed as key word argument
        if table_number == 2:
            table_name = cls.BET_MATCHES_TWO_OUTCOMES_TABLE
        else:
            table_name = cls.BET_MATCHES_THREE_OUTCOMES_TABLE

        select_events = f"""SELECT TOP(1000) * 
                            from {table_name}
                            """
        select_events = cls.add_filters_to_condition(select_events, filters)
           
        print(select_events)

        azure_connection = pyodbc.connect(cls.params)
        azure_cursor = azure_connection.cursor()   

        azure_cursor.execute(select_events)
        records = azure_cursor.fetchall()
        azure_cursor.close()
        azure_connection.close()
        return records

    @classmethod
    def add_filters_to_condition(cls, sql_select, filters):
        first_condition = True
        if filters.get("RTPFrom"):   
            sql_select, first_condition = cls.check_first_condition(sql_select, first_condition)
            sql_select += f"RTP >= {filters.get('RTPFrom')} "
        if filters.get("RTPTo"):   
            sql_select, first_condition = cls.check_first_condition(sql_select, first_condition)
            sql_select += f"RTP <= {filters.get('RTPTo')} "
        if filters.get("dateFrom"):   
            sql_select, first_condition = cls.check_first_condition(sql_select, first_condition)
            sql_select += f"date >= '{filters.get('dateFrom')}' "
        if filters.get("dateTo"):   
            sql_select, first_condition = cls.check_first_condition(sql_select, first_condition)
            sql_select += f"date <= '{filters.get('dateTo')}' "
        if filters.get("bookmaker1"):
            #string formatting to create a list for sql server
            bookmaker1_list = re.sub(r'\]{1,1}$', ')', re.sub(r'^\[?', '(', str(filters.get("bookmaker1"))))
            sql_select, first_condition = cls.check_first_condition(sql_select, first_condition)
            sql_select += f"bookmaker1 IN {bookmaker1_list} "
        if filters.get("betOdd1From"):   
            sql_select, first_condition = cls.check_first_condition(sql_select, first_condition)
            sql_select += f"betOdd1 >= {filters.get('betOdd1From')} "
        if filters.get("betOdd1To"):   
            sql_select, first_condition = cls.check_first_condition(sql_select, first_condition)
            sql_select += f"betOdd1 <= {filters.get('betOdd1To')} "
        if filters.get("bet1"):
            #string formatting to create a list for sql server
            bet1_list = re.sub(r'\]{1,1}$', ')', re.sub(r'^\[?', '(', str(filters.get("bet1"))))
            sql_select, first_condition = cls.check_first_condition(sql_select, first_condition)
            sql_select += f" bet1 IN {bet1_list} "
        if filters.get("bookmaker2"):
            #string formatting to create a list for sql server
            bookmaker2_list = re.sub(r'\]{1,1}$', ')', re.sub(r'^\[?', '(', str(filters.get("bookmaker2"))))
            sql_select, first_condition = cls.check_first_condition(sql_select, first_condition)
            sql_select += f" bookmaker2 IN {bookmaker2_list} "
        if filters.get("betOdd2From"):   
            sql_select, first_condition = cls.check_first_condition(sql_select, first_condition)
            sql_select += f"betOdd2 >= {filters.get('betOdd2From')} "
        if filters.get("betOdd2To"):   
            sql_select, first_condition = cls.check_first_condition(sql_select, first_condition)
            sql_select += f"betOdd2 <= {filters.get('betOdd2To')} "
        if filters.get("bet2"):
            #string formatting to create a list for sql server
            bet2_list = re.sub(r'\]{1,1}$', ')', re.sub(r'^\[?', '(', str(filters.get("bet2"))))
            sql_select, first_condition = cls.check_first_condition(sql_select, first_condition)
            sql_select += f" bet2 IN {bet2_list} "
        if filters.get("bookmaker3"):
            bookmaker3_list = re.sub(r'\]{1,1}$', ')', re.sub(r'^\[?', '(', str(filters.get("bookmaker3"))))
            sql_select, first_condition = cls.check_first_condition(sql_select, first_condition)
            sql_select += f" bookmaker3 IN {bookmaker3_list} "
        if filters.get("betOdd3From"):   
            sql_select, first_condition = cls.check_first_condition(sql_select, first_condition)
            sql_select += f"betOdd3 >= {filters.get('betOdd3From')} "
        if filters.get("betOdd3To"):   
            sql_select, first_condition = cls.check_first_condition(sql_select, first_condition)
            sql_select += f"betOdd3 <= {filters.get('betOdd3To')} "
        if filters.get("bet3"):
            #string formatting to create a list for sql server
            bet3_list = re.sub(r'\]{1,1}$', ')', re.sub(r'^\[?', '(', str(filters.get("bet3"))))
            sql_select, first_condition = cls.check_first_condition(sql_select, first_condition)
            sql_select += f" bet3 IN {bet3_list} "
        
        sql_select += "ORDER BY RTP desc;"
        return sql_select

    def check_first_condition(sql_select, first_condition):
        if first_condition:
            first_condition = False
            sql_select += "WHERE "
        else:
            sql_select += "AND "
        return sql_select, first_condition








        # connection = sqlite3.connect(settings.BASE_DIR / cls.DB_NAME)
        # cursor = connection.cursor()
        # select_events = f"""SELECT * 
        #                     from {cls.TABEL_NAME}
        #                     where betRadarID == "{betRadarID}" 
        #                     LIMIT 10;
        #                 """
        # cursor.execute(select_events)
        # records = cursor.fetchall()
        # cursor.close()
        # connection.close()
        # return records



