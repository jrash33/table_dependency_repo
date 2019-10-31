# table_dependency_repo

Joey Ashcroft
10/31/2019

Challenge:  
determine the relationships between database tables as described across a series of configuration files. The configuration files are JSON documents which describe a SQL query that has been broken up into SELECT, FROM and WHERE clauses to facilitate automated execution. You can safely ignore primary key and foreign key relationships in this case. The relationship we are interested in, is the implicit dependency between the table joins as described in each FROM clause within each document. A unique table name is of the format schema-name.table-name. Your code will determine these relationships and then "pretty print" those in some human readable ascii format.


1. A description of the solution approach taken:
My code was implemented in Jupyter Notebooks using Python 3 so the code should be intuitive and easy to follow!

        Here is a quick summary of my approach:
        - Extract data from tar.gz
        - store JSON data in list
        - Harvest data of interest (from clause/table names/schema names), clean it, and format in dictionary
        - Obtain table dependencies from each from clause
        - Sort these dependencies from simple to complex
        - If dependencies in some tables exist in the table elsewhere, replace these dependencies with those dependencies
        - Display in ASCII tree format


2. How to compile and or execute your code
        - Pip install the necessary modules listed at the top
        - I would advise first looking at the Juptyer Notebook script to see outputs/comments/user friendly format
        - I have attached a main.py file that can be executed in an IDE of your choosing as long as it is in the same folder as the data
