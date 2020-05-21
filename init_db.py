import sqlite3

DATABASE_FILE = "database.db"

# important:
#-------------------------------------------------------------
# This script initialises your database for you using SQLite,
# just to get you started... there are better ways to express
# the data you're going to need... especially outside SQLite.
# For example... maybe flag_pattern should be an ENUM (which
# is available in most other SQL databases), or a foreign key
# to a pattern table?
#
# Also... the name of the database (here, in SQLite, it's a
# filename) appears in more than one place in the project.
# That doesn't feel right, does it?
#
#-------------------------------------------------------------

con = sqlite3.connect(DATABASE_FILE)
print("- Opened database successfully in file \"{}\"".format(DATABASE_FILE))

# using Python's triple-quote for multi-line strings:

con.execute("""

  CREATE TABLE IF NOT EXISTS buggies (
    id                    INTEGER PRIMARY KEY,
    qty_wheels            INTEGER DEFAULT 4,
    power_type            VARCHAR(20)
    power_units           VARCHAR(20)
    aux_power_type        VARCHAR(20)
    aux_power_units       VARCHAR(20)
    hamster_booster       VARCHAR(20)
    flag_color            VARCHAR(20)
    flag_pattern          VARCHAR(20)
    flag_color_secondary  VARCHAR(20)
    tyres                 VARCHAR(20)
    qty_tyres             VARCHAR(20)
    armour                VARCHAR(20)
    attack                VARCHAR(20)
    qty_attacks           VARCHAR(20)
    fireproof             VARCHAR(20)
    insulated             VARCHAR(20)
    antibiotic            VARCHAR(20)
    banging               VARCHAR(20),
    algo                  VARCHAR(20),
  )

""")

print("- Table \"buggies\" exists OK")

cur = con.cursor()

cur.execute("SELECT * FROM buggies LIMIT 1")
rows = cur.fetchall()
if len(rows) == 0:
  cur.execute("INSERT INTO buggies (qty_wheels) VALUES (4)")
  con.commit()
  print("- Added one 4-wheeled buggy")
else:
  print("- Found a buggy in the database, nice")
print("- done")

con.close()