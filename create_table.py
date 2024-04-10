import sqlite3

# Connect to the database
conn = sqlite3.connect('final.db')
c = conn.cursor()

# Create table
c.execute('''
    CREATE TABLE em_lightfixes (
        fault_id INTEGER PRIMARY KEY,
        inspect TEXT,
        fault TEXT,
        remedy TEXT
    )
''')

# Insert rows
c.execute("INSERT INTO em_lightfixes ( inspect, fault, remedy) VALUES (?, ?, ?)", ('Check there has not been interruption to mains power in last 16 hours', 'Mains power has been disrupted', 'Can not test emergency lighting in service duration'))
c.execute("INSERT INTO em_lightfixes ( inspect, fault, remedy) VALUES (?, ?, ?)", ('Check directional beams for suitability', 'Directional beams shine into eyes', 'Adjust directional beams as required'))
c.execute("INSERT INTO em_lightfixes ( inspect, fault, remedy) VALUES (?, ?, ?)", ('Check any fluorescent lamps for blackened ends', 'Fluorescent lamp has blackened ends', 'Fluorescent lamp has to be replaced'))
c.execute("INSERT INTO em_lightfixes ( inspect, fault, remedy) VALUES (?, ?, ?)", ('Check emergency lighting operates in correct relationship with other lighting', 'Emergency lighting does not operates in correct relationship with other lighting', 'Make good emergency lighting to operate in correct relationship with other lighting'))
c.execute("INSERT INTO em_lightfixes ( inspect, fault, remedy) VALUES (?, ?, ?)", ('Carry out in-service duration test by isolating emergency lighting from mains power', 'The light failed in-service duration test 90m minutes', 'Change the back up battery and redo the test after 16 hours of constant power'))

# Commit the changes and close the connection
conn.commit()
conn.close()