from flask import g
import sqlite3
from sqlite3 import Error
from datetime import datetime
import os

# Utility class. Contains methods to connect to database, create table, rename column, add entry
# to table, update an existing entry, retrieve an existing entry, and delete an existing entry.
class DatabaseOperations:

    def __init__(self, path):
        self.db_file = path

    # Establishes connection to DB if path is valid. NOTE: connection must be closed by calling method.
    def connect_to_db(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
        except Error as e:
            print(e)
        finally:
            return conn

    # Closes an existing connection.
    def close_connection(self, conn):
        if conn:
            conn.close()

    # Inserts one item into a given table and verifies that values added to table match expected.
    def insert_into_db(self, table_name, primary_key, c2, c3, c4, c5):
        conn = self.connect_to_db()
        if conn:
            c = conn.cursor()
            c.execute("INSERT INTO "+table_name+" VALUES(?, ?, ?, ?, ?)", (primary_key, c2, c3, c4, c5))
            conn.commit()
            self.close_connection(conn)
        else:
            print("Failed to connect")

    # Updates an existing entry. Column to search should probably be some unique identifier.
    def update_existing_entry(self, table_name, column_to_search, column_to_update, value_to_search, value_to_update):
        conn = self.connect_to_db()
        if conn:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            c.execute("UPDATE "+table_name+" SET "+column_to_update+" = ? WHERE "+column_to_search+" = ?", (value_to_update, value_to_search))
            conn.commit()
            self.close_connection(conn)
        else:
            print("Failed to connect")

    # Retrieves all items that match the value in the specified column.
    def retrieve_by_column_value(self, table_name, column_to_search, value):
        row = None
        conn = self.connect_to_db()
        if conn:
            c = conn.cursor()
            c.execute("SELECT * FROM "+table_name+" WHERE "+column_to_search+" = ?", (value,))
            row = c.fetchall()
            self.close_connection(conn)
        else:
            print("Failed to connect")
        return row

    # Renames column.
    def rename_column(self, table_name, current_column_name, new_column_name):
        conn = connect_to_db()
        if conn:
            c = conn.cursor()
            c.execute("ALTER TABLE "+table_name+" RENAME COLUMN "+current_column_name+" TO "+new_column_name+"")
            conn.commit()
            close_connection(conn)

    # Creates a new table based on parameters.
    def create_table(self, table_name, columns, types):
        conn = connect_to_db()
        if conn:
            num_columns = len(columns)
            num_types = len(types)
            if num_columns != num_types:
                print("Mismatching number of columns and types. Please double check your entry and try again.")
            else:
                conn = sqlite3.connect(self.db_file)
                c = conn.cursor()
                sql = "CREATE TABLE "+table_name+"("
                for i in range(0, num_columns):
                    sql += columns[i] + " "
                    sql += types[i]
                    if i + 1 != num_columns:
                        sql += ", "
                sql += ");"
                print(sql)
                c.execute(sql)
                conn.commit()
                close_connection(conn)


class ItemsTableOps:

    def __init__(self, path):
        self.item_id_col = "ID"
        self.title_col = "Title"
        self.linked_id_col = "LinkedID"
        self.service_col = "Service"
        self.type_col = "Type"
        self.table_name = "Items"
        self.db_ops = DatabaseOperations(path)
    
    # # # RETRIEVE METHODS FOR ITEMS TABLE # # #

    def retrieve_by_item_id(self, item_id):
        return db_ops.retrieve_by_column_value(self.table_name, self.item_id_col, item_id)

    def retrieve_by_title(self, name):
        return db_ops.retrieve_by_column_value(self.table_name, self.title_col, name)

    def retrieve_by_linked_id(self, linked_id):
        return db_ops.retrieve_by_column_value(self.table_name, self.linked_id_col, linked_id)

    def retrieve_by_service(self, service):
        return db_ops.retrieve_by_service(self.table_name, self.service_col, service)
    
    def retrieve_by_type(self, type_):
        return db_ops.retrieve_by_service(self.table_name, self.type_col, type_)

     # # # UPDATE METHODS FOR ITEMS TABLE # # #

     # Updates item title based on unique integer id.
    def update_item_title(self, unique_id, new_title):
        db_ops.update_existing_entry(self.table_name, self.item_id_col, self.title_col, unique_id, new_title)

    # Takes unique integer ID and updates corresponding entry's linked id value.
    def update_linked_id(self, unique_id, new_linked_id):
        db_ops.update_existing_entry(self.table_name, self.item_id_col, self.linked_id_col, unique_id, new_linked_id)

    def update_type(self, unique_id, new_type):
        db_ops.update_existing_entry(self.table_name, self.item_id_col, self.type_col, unique_id, new_type)

    def update_service(self, unique_id, new_service):
        db_ops.update_existing_entry(self.table_name, self.item_id_col, self.service_col, unique_id, new_service)

    def update_item_id(self, unique_id, new_unique_id):
        db_ops.update_existing_entry(self.table_name, self.item_id_col, self.item_id_col, unique_id, new_unique_id)

    # # # INSERT METHODS FOR ITEMS TABLE # # #
    
    # Inserts one item into the Items table.
    def insert_into_items_table(self, id, title, type, service, linked_id):
        db_ops.insert_into_db(self.table_name, id, title, type, service, linked_id)


class FieldsTableOps:
    # field_id is primary key (unique identifier in table.)
    def __init__(self, path):
        self.field_id_col = "FieldID"
        self.item_id_col = "ItemID"
        self.last_updated_col = "LastUpdated"
        self.jira_name_col = "JiraName"
        self.jama_name_col = "JamaName"
        self.table_name = "Fields"
        self.db_ops = DatabaseOperations(path)

    # # # RETRIEVE METHODS FOR FIELDS TABLE # # #

    def retrieve_by_field_id(self, field_id):
        return self.db_ops.retrieve_by_column_value(self.table_name, self.field_id_col, field_id)

    def retrieve_by_item_id(self, item_id):
        return self.db_ops.retrieve_by_column_value(self.table_name, self.item_id_col, item_id)

    def retrieve_by_last_updated(self, last_updated):
        return self.db_ops.retrieve_by_column_value(self.table_name, self.last_updated_col, last_updated)

    def retrieve_by_jama_name(self, jama_name):
        return self.db_ops.retrieve_by_column_value(self.table_name, self.jama_name_col, jama_name)

    def retrieve_by_jira_name(self, jira_name):
        return self.db_ops.retrieve_by_column_value(self.table_name, self.jira_name_col, jira_name)

    # # # UPDATE METHODS FOR FIELDS TABLE # # #

    def update_field_id(self, unique_id, new_unique_id):
        self.db_ops.update_existing_entry(self.table_name, self.field_id_col, self.field_id_col, unique_id, new_unique_id)

    def update_item_id(self, unique_id, new_item_id):
        self.db_ops.update_existing_entry(self.table_name, self.field_id_col, self.item_id_col, unique_id, new_item_id)

    def update_last_updated_time(self, unique_id, new_time_updated):
        self.db_ops.update_existing_entry(self.table_name, self.field_id_col, self.last_updated_col, unique_id, new_time_updated)
    
    def update_jama_name(self, unique_id, new_jama_name):
        self.db_ops.update_existing_entry(self.table_name, self.field_id_col, self.jama_name_col, unique_id, new_jama_name)
            
    def update_jira_name(self, unique_id, new_jira_name):
        self.db_ops.update_existing_entry(self.table_name, self.field_id_col, self.jira_name_col, unique_id, new_jira_name)

    # # # INSERT METHODS FOR FIELDS TABLE # # #

    # Inserts one item into the Fields table.
    def insert_into_fields_table(self, item_id, field_id, last_updated, jira_name, jama_name):
        self.db_ops.insert_into_db(self.table_name, item_id, field_id, last_updated, jira_name, jama_name)



class SyncInformationTableOps:

    def __init__(self, path):
        self.sync_id_col = "SyncID"
        self.start_time_col = "StartTime"
        self.end_time_col = "EndTime"
        self.completed_successfully_col = "CompletedSuccessfully"
        self.table_name = "SyncInformation"


# Main method to demo functionality. Uncomment blocks to observe how they function.
if __name__ == '__main__':
    fields_table = "Fields"
    items_table = "Items"
    fields_column = "FieldID"
    items_column = "ID"
    item_id = 20006
    field_id = 161
    # Gets absolute path to root folder and appends database file. Should work on any machine.
    db_path = os.path.join(os.path.dirname(os.getcwd()), "JamaJiraConnectDataBase.db")
    db_ops = DatabaseOperations(db_path)
    items_table_ops = ItemsTableOps(db_path)
    fields_table_ops = FieldsTableOps(db_path)

    # Demo create table. Define list of types and columns to pass in to method.
    '''columns = ["SyncID", "StartTime", "EndTime", "CompletedSuccessfully"]
    types = ["INT PRIMARY KEY NOT NULL", "DATETIME DEFAULT(STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW'))", "DATETIME DEFAULT(NULL)", "INT"]
    db_ops.create_table("SyncInformation", columns, types)'''

    # Demo rename column. Takes the table name, current column name and updated column name as args.
    '''db_ops.rename_column(fields_table, "Item", "ItemID")'''

    # Demo INSERT query. NOTE: field id and item id must be unique in order to be added.
    '''time = datetime.now().strftime('%Y-%m-%d %H:%M:%f')
    items_table_ops.insert_into_items_table(item_id, 'ticketx', 'ticket', 'Jama', 'NULL')
    fields_table_ops.insert_into_fields_table(field_id, item_id, time, 'Issue', 'Ticket')'''

    # Demo SELECT query.
    item_row = items_table_ops.retrieve_by_item_id(item_id)
    print("Retrieved from items table: ", item_row)
    field_row = fields_table_ops.retrieve_by_item_id("1")
    print("Retrieved from fields table: ", field_row)

    # Demo UPDATE query.
    items_table_ops.update_linked_id(item_id, "1002")
    item_row = items_table_ops.retrieve_by_item_id(item_id)
    print("Updated items row: ", item_row)

    fields_table_ops.update_jama_name(field_id, "FancyIssue")
    field_row = fields_table_ops.retrieve_by_field_id(field_id)
    print("Updated fields row: ", field_row)