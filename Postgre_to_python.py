import psycopg2
import psycopg2.extras

#connection details
hostname = 'localhost'
database = 'demo'
username = 'postgres'
pwd = 11111
port_id = 5432

conn = None

#display() function defined before calling
def display():
    cur.execute('SELECT * FROM carmax2')
    for x in cur.fetchall():
        print(x)

# try and error exception
try:
     with psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id
    ) as conn:

        #defined cursor to execute SQL query
         with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

            # creating a table in postgreSQL
            cur.execute('Drop Table IF EXISTS carmax2')

            #Create Command
            create_script = '''  CREATE TABLE IF NOT EXISTS carmax2 (
                                name varchar(20) not null,
                                buildyear date,
                                miles int,
                                color varchar(10),
                                title varchar(20) not null 
                                 )
            '''
            cur.execute(create_script)

            #insert Command
            insert_script = 'INSERT INTO carmax2 (name, buildyear,miles,color,title) VALUES (%s,%s,%s,%s,%s) '
            insert_values = [('BMW1','2015-04-02',56000,'silver','clean'),
                         ('Hyundai','2015-08-11',75000,'Red','clean'),
                         ('Hyundai', '2012-03-02',176000, 'silver','Rebuild'),
                         ('BMW2', '2010-07-02',90000, 'Black','clean'),
                         ('Hyundai', '2017-04-15',93890, 'White','Rebuild')
                             ]

            for record in insert_values:
                cur.execute(insert_script, record)

            #Read Command
            cur.execute('SELECT * FROM carmax2')
            for x in cur.fetchall():
                print(x['name'], x['color'])

            #Alter Command
            print('Adding Column COST')
            update_1 = 'ALTER TABLE carmax2 ADD COLUMN Cost int;'
            cur.execute(update_1)


            #update Command
            print('Updating Column COST with Values')
            update_query = "UPDATE carmax2 SET Cost = %s WHERE name = %s;"
            update_values = [
                (30000, 'BMW1'),
                (6000, 'Hyundai'),
                (2500, 'Hyundai'),
                (10000, 'BMW2'),
                (7000, 'Hyundai')
            ]
            for i in update_values:
                cur.execute(update_query, i)
            display()
            print("Added Cost column and data into cost column completed")

            #Update Command
            update_3 = 'UPDATE carmax2 SET cost = cost-2500'
            cur.execute(update_3)
            display()
            print(' Car Costs reduction Updated-------------')

            #Delect command
            delete_s='Delete From carmax2 where color= %s and name=%s;'
            delete_values = ('silver','Hyundai')
            cur.execute(delete_s, delete_values)
            display()
            print('Deleted Hyundai Silver car')

# we don't need to commit as we use WITH clause
        #conn.commit()

except Exception as e:
    print(e)

finally:
# we don't need to close cur , it closes by itself, as we are using WITH clause

    #if cur is not None:
        #cur.close()
    if conn is not None:
        conn.close()

