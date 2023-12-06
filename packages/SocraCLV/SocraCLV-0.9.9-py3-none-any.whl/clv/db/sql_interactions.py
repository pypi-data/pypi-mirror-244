import sqlite3
import logging 
import pandas as pd
import numpy as np
import os
from ..logger import CustomFormatter

logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)

class SqlHandler:
    """
    A class to handle common SQL operations on a database.

    Attributes:
    - dbname (str): The name of the database.
    - table_name (str): The name of the table to perform operations on.
    """
    def __init__(self, dbname:str,table_name:str) -> None:
        """
        Initialize the SqlHandler object with a database name and table name.

        Parameters:
        - dbname (str): The name of the database to connect to.
        - table_name (str): The name of the table to perform operations on.
        """        
        self.cnxn=sqlite3.connect(f'{dbname}.db')
        self.cursor=self.cnxn.cursor()
        self.dbname=dbname
        self.table_name=table_name

    def close_cnxn(self)->None:
        """
        Close the connection to the database.
        """

        logger.info('commiting the changes')
        self.cursor.close()
        self.cnxn.close()
        logger.info('the connection has been closed')

    def insert_one(self, values: dict) -> str:
        """
        Insert a single row into the table.

        Parameters:
            values (dict): A dictionary containing the column names and their respective values.

        Returns:
            str: A message indicating the success of the insertion.
        """
        columns = list(values.keys())
        ncolumns = len(columns) * '?'
        cols = ', '.join(columns)
        params = ', '.join(ncolumns)

        query = f"""INSERT INTO {self.table_name} ({cols}) VALUES ({params});"""

        try:
            self.cursor.execute(query, list(values.values()))
            self.cnxn.commit()
            return "Row inserted successfully."
        except Exception as e:
            return f"Error inserting row: {str(e)}"

    def get_table_columns(self)->list:
        """
        Retrieve a list of column names from the table in the database.
        
        This method uses the PRAGMA table_info SQL command to get metadata about the table's columns.
        
        Returns:
            list: A list of column names from the table.
        """
        self.cursor.execute(f"PRAGMA table_info({self.table_name});")
        columns = self.cursor.fetchall()
        
        column_names = [col[1] for col in columns]
        logger.info(f'the list of columns: {column_names}')
        # self.cursor.close()

        return column_names
    
    def truncate_table(self)->None:
        """
        Remove all data from the table by dropping it and creating a new one.
        
        This method drops the table if it exists, effectively removing all data from it.
        Use with caution as this will result in data loss.
        """
        
        query=f"DROP TABLE IF EXISTS {self.table_name};"
        self.cursor.execute(query)
        logging.info(f'the {self.table_name} is truncated')
        # self.cursor.close()

    def drop_table(self):
        """
        Drop the table from the database.
        
        This method drops the table if it exists. This action cannot be undone.
        """
        
        query = f"DROP TABLE IF EXISTS {self.table_name};"
        logging.info(query)

        self.cursor.execute(query)

        self.cnxn.commit()

        logging.info(f"table '{self.table_name}' deleted.")
        logger.debug('using drop table function')

    def insert_many(self, df:pd.DataFrame) -> str:
        """

        Parameters
        ----------
        df:pd.DataFrame :
            

        Returns
        -------

        """
        
        df=df.replace(np.nan, None) # for handling NULLS
        df.rename(columns=lambda x: x.lower(), inplace=True)
        columns = list(df.columns)
        logger.info(f'BEFORE the column intersection: {columns}')
        sql_column_names = [i.lower() for i in self.get_table_columns()]
        print("colsL", columns)
        print(sql_column_names)
        columns = list(set(columns) & set(sql_column_names))
        logger.info(f'AFTER the column intersection: {columns}')
        ncolumns=list(len(columns)*'?')
        data_to_insert=df.loc[:,columns]
        print("colsL", columns)
    
        values=[tuple(i) for i in data_to_insert.values]
        logger.info(f'the shape of the table which is going to be imported {data_to_insert.shape}')
        # if 'geometry' in columns: #! This block is usefull in case of geometry/geography data types
        #     df['geometry'] = df['geometry'].apply(lambda geom: dumps(geom))
        #     ncolumns[columns.index('geometry')]= 'geography::STGeomFromText(?, 4326)'
        
        if len(columns)>1:
            cols,params =', '.join(columns), ', '.join(ncolumns)
        else:
            cols,params =columns[0],ncolumns[0]
            
        logger.info(f'insert structure: colnames: {cols} params: {params}')
        logger.info(values[0])
        query=f"""INSERT INTO  {self.table_name} ({cols}) VALUES ({params});"""
        
        logger.info(f'QUERY: {query}')

        self.cursor.executemany(query, values)
        try:
            for i in self.cursor.messages:
                logger.info(i)
        except:
            pass


        self.cnxn.commit()
      
        
        logger.warning('the data is loaded')


    def from_sql_to_pandas(self, chunksize:int, id_value:str) -> pd.DataFrame:
        """

        Parameters
        ----------
        chunksize:int :
            
        id_value:str :
            

        Returns
        -------

        """
        
        offset=0
        dfs=[]
       
        
        while True:
            query=f"""
            SELECT * FROM {self.table_name}
                ORDER BY {id_value}
                OFFSET  {offset}  ROWS
                FETCH NEXT {chunksize} ROWS ONLY  
            """
            data = pd.read_sql_query(query,self.cnxn) 
            logger.info(f'the shape of the chunk: {data.shape}')
            dfs.append(data)
            offset += chunksize
            if len(dfs[-1]) < chunksize:
                logger.warning('loading the data from SQL is finished')
                logger.debug('connection is closed')
                break
        df = pd.concat(dfs)

        return df


    def update_table(self,condition):
        """

        Parameters
        ----------
        condition :
            

        Returns
        -------

        """
        pass
        # TODO: complete on your own

    def select_row(self, column_name, value):
        """
        Select a row from the table based on a specific column name and its value.

        Parameters:
        - column_name (str): The name of the column to filter on.
        - value: The value to filter rows by in the specified column.

        Returns:
        - A tuple containing the selected row.
        """
        query = f"SELECT * FROM {self.table_name} WHERE {column_name} = ?;"
        self.cursor.execute(query, (value,))
        rows = self.cursor.fetchall()
        if not rows:
            return "No matching data found."
        else:
            return rows


    def get_table_data(self, columns: list = None, condition: str = None) -> pd.DataFrame:
        """
        Retrieve data from the table based on the specified columns and optional condition.

        Parameters:
            columns (list): A list of column names to retrieve. If not specified, all columns will be retrieved.
            condition (str): An optional SQL condition to filter the data (e.g., "column_name = 'value'"). If not specified, all data will be retrieved.

        Returns:
            pd.DataFrame: A DataFrame containing the retrieved data.
        """
        if columns is None:
            columns = self.get_table_columns()

        if not columns:
            return pd.DataFrame()

        column_names = ', '.join(columns)

        query = f"SELECT {column_names} FROM {self.table_name}"
        if condition:
            query += f" WHERE {condition}"

        data = pd.read_sql_query(query, self.cnxn)
        return data
   
        



