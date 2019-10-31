#import modules
import gzip
import tarfile
import json
from asciitree import LeftAligned
from collections import OrderedDict as OD
from toposort import toposort_flatten

#open gzipped tar file
tar = tarfile.open('tables.tar.gz', "r:gz")

TABLES = []

#store json tables in list
for i in tar:
    #extract file from list
    tar_extract = tar.extractfile(i)

    try:
        #convert to json
        table_json = json.loads(tar_extract.read())

        #store json
        TABLES.append(table_json)
        
    except:
        None


query_info = []

#iterate through each json file stored in list
for i in TABLES:  
    #get schema name
    schema_name = i['schema']['S']
    #get table name
    table_name = i['table']['S']
    #combine in 'schema-name.table-name' format
    name_combined = schema_name + "." + table_name
    
    try:
        #get FROM clause with implicit table dependencies
        from_clause = i['query']['L'][0]['M']['from']['S']
    except:
        #get FROM clause in json format
        from_clause = i['query']['M']['from']['S']
        
    #store in dictionary format
    dict_ = {'table_name':name_combined, 'from':from_clause}
    
    #append to our list above
    query_info.append(dict_)

#function to get first word in string
def get_dependencies(n):
    return n.split()[0]

#to be stored in ORDERED DICTIONARY FORMAT for ascii tree library
dependencies = OD([])

#iterate through each FROM clause and grab the dependencies
for i in query_info:
    
    #conditional for multiple dependencies
    if 'join' in i['from'].lower():
        #split the string on each join
        string = i['from'].lower().split('join')
        #grab the first word after each join
        tables = list(map(get_dependencies, string))
         
        #store each dependency in OD format again
        tables_OD = OD([])
        for j in tables:
            tables_OD[j] = {}
        
        #create an OD instance with table and its dependencies
        table_name = 'table_name'
        dependencies[f"{i[table_name]}"] = tables_OD
        
    #conditional for single dependencies
    else:
        
        tables = i['from'].split()[0] 
        #create a dictionary with table and its dependencies
        table_dependency = {i['table_name']: tables}
        
        #create an OD instance with table and its dependencies
        table_name = 'table_name'
        dependencies[f"{i[table_name]}"] = OD([(tables,{})])

#through topological sorting, we can map the dependencies of the simplest tables first and build on those as we gain complexity
#this prevents extensive imbedded for loops...
graph = dict(zip(dependencies.keys(), map(set, dependencies.values())))
sorted_graph = toposort_flatten(graph, sort=True)
#items sorted as most complex will always be the key values
sorted_graph = sorted_graph[-len(dependencies):]

#starting with the least complex dependencies, insert table dependencies
for i in sorted_graph:
    for j in dependencies[i]:
        try:
            #if key values of tables are actual table names, replace them with these table dependencies instead
            dependencies[i][j] = dependencies[j]
        except:
            None

#function that accepts table name and outputs visual of its dependencies
def ascii_tree(table_name):
    tree = {table_name: dependencies[table_name]}
    tr = LeftAligned()
    print(tr(tree))

for i in sorted_graph:
    print(f"-------------- {i} DEPENDENCIES --------------")
    print("")
    ascii_tree(i)
    print("")