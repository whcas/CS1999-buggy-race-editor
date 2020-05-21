from flask import Flask, render_template, request, jsonify
import sqlite3 as sql
app = Flask(__name__)

DATABASE_FILE = "database.db"
DEFAULT_BUGGY_ID = "1"

BUGGY_RACE_SERVER_URL = "http://rhul.buggyrace.net"


#------------------------------------------------------------
# the index page
#------------------------------------------------------------
@app.route('/')
def home():
   return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL)

#------------------------------------------------------------
# creating a new buggy:
#  if it's a POST request process the submitted data
#  but if it's a GET request, just show the form
#------------------------------------------------------------
@app.route('/new', methods = ['POST', 'GET'])
def create_buggy():
  if request.method == 'GET':
    return render_template("buggy-form.html")
  elif request.method == 'POST':
    msg=""
    ValidCart = True

    qty_wheels = 4
    power_type = power_type = request.form['power_type']
    power_units = 1
    aux_power_type = request.form['aux_power_type']
    aux_power_units = 0
    hamster_booster = 0
    flag_color = request.form['flag_color']
    flag_pattern = request.form['flag_pattern']
    flag_color_secondary = request.form['flag_color_secondary']
    tyres = request.form['tyres']
    qty_tyres = 4
    armour = request.form['armour']
    attack = request.form['attack']
    qty_attacks = 0
    algo = request.form['algo']
  
    if request.form['fireproof'] == "true":
      fireproof = 1
    else:
      fireproof = 0
    if request.form['insulated'] == "true":
      insulated = 1
    else:
      insulated = 0
    if request.form['antibiotic'] == "true":
      antibiotic = 1
    else:
      antibiotic = 0
    if request.form['banging'] == "true":
      banging = 1
    else:
      banging = 0

    try:
      qty_wheels = int(request.form['qty_wheels'])
      if (qty_wheels % 2 != 0) or (qty_wheels < 4):
        raise Exception('Invalid number of wheels')
      msg = f"qty_wheels={qty_wheels}"
    except ValueError:
      ValidCart = False
      msg += (' The NUMBER of wheels has to be an integer.')
    except Exception:
      ValidCart = False
      if (qty_wheels % 2 != 0):
        msg += " Wheels not even."
      if (qty_wheels < 4):
        msg += " Not enough wheels."

    try:
      power_units = int(request.form['power_units'])
      if power_units < 0:
        raise Exception("You can't have negative fuel")
    except ValueError:
      ValidCart = False
      msg += (' The amount of fuel has to be an integer.')
    except Exception:
      ValidCart = False
      msg += " You can't have negative fuel."

    try:
      aux_power_units = int(request.form['aux_power_units'])
      if power_units < 0:
        raise Exception("You can't have negative fuel")
    except ValueError:
      ValidCart = False
      msg += (' The amount of fuel has to be an integer.')
    except Exception:
      ValidCart = False
      msg += " You can't have negative fuel."

    try:
      hamster_booster = int(request.form['hamster_booster'])
      if power_units < 0:
        raise Exception("You can't have negative steroids")
    except ValueError:
      ValidCart = False
      msg += (' The amount of steroids for the hampster has to be an integer.')
    except Exception:
      ValidCart = False
      msg += " You can't have a negative ammount of steroids."

    try:
      qty_tyres = int(request.form['qty_tyres'])
      if qty_tyres < qty_wheels:
        raise Exception("You need at least as many tyres as wheels")
    except ValueError:
      ValidCart = False
      msg += (' The amount of tyres has to be an integer.')
    except Exception:
      ValidCart = False
      msg += " You need at least as many tyres as you have wheels."

    try:
      qty_attacks = int(request.form['qty_attacks'])
      if power_units < 0:
        raise Exception("You can't have negative attacks")
    except ValueError:
      ValidCart = False
      msg += (' The number of attacks has to be an integer.')
    except Exception:
      ValidCart = False
      msg += " You can't have a negative number of attacks."

    if ValidCart == True:
      try:
        with sql.connect(DATABASE_FILE) as con:
          cur = con.cursor()
          cur.execute("UPDATE buggies set qty_wheels=? WHERE id=?", (qty_wheels, DEFAULT_BUGGY_ID))
          cur.execute("UPDATE buggies set power_type=? WHERE id=?", (power_type, DEFAULT_BUGGY_ID))
          cur.execute("UPDATE buggies set power_units=? WHERE id=?", (power_units, DEFAULT_BUGGY_ID))
          cur.execute("UPDATE buggies set aux_power_type=? WHERE id=?", (aux_power_type, DEFAULT_BUGGY_ID))
          cur.execute("UPDATE buggies set aux_power_units=? WHERE id=?", (aux_power_units, DEFAULT_BUGGY_ID))
          cur.execute("UPDATE buggies set hamster_booster=? WHERE id=?", (hamster_booster, DEFAULT_BUGGY_ID))
          cur.execute("UPDATE buggies set flag_color=? WHERE id=?", (flag_color, DEFAULT_BUGGY_ID))
          cur.execute("UPDATE buggies set flag_pattern=? WHERE id=?", (flag_pattern, DEFAULT_BUGGY_ID))
          cur.execute("UPDATE buggies set flag_color_secondary=? WHERE id=?", (flag_color_secondary, DEFAULT_BUGGY_ID))
          cur.execute("UPDATE buggies set tyres=? WHERE id=?", (tyres, DEFAULT_BUGGY_ID))
          cur.execute("UPDATE buggies set qty_tyres=? WHERE id=?", (qty_tyres, DEFAULT_BUGGY_ID))
          cur.execute("UPDATE buggies set armour=? WHERE id=?", (armour, DEFAULT_BUGGY_ID))
          cur.execute("UPDATE buggies set attack=? WHERE id=?", (attack, DEFAULT_BUGGY_ID))
          cur.execute("UPDATE buggies set qty_attacks=? WHERE id=?", (qty_attacks, DEFAULT_BUGGY_ID))
          cur.execute("UPDATE buggies set fireproof=? WHERE id=?", (fireproof, DEFAULT_BUGGY_ID))
          cur.execute("UPDATE buggies set insulated=? WHERE id=?", (insulated, DEFAULT_BUGGY_ID))
          cur.execute("UPDATE buggies set antibiotic=? WHERE id=?", (antibiotic, DEFAULT_BUGGY_ID))
          cur.execute("UPDATE buggies set banging=? WHERE id=?", (banging, DEFAULT_BUGGY_ID))
          cur.execute("UPDATE buggies set algo=? WHERE id=?", (algo, DEFAULT_BUGGY_ID))
          con.commit()
          msg = "Record successfully saved"
      # except:
      #   con.rollback()
      #   msg = "error in update operation"
      finally:
        try:
          con.close()
        except:
          pass
    return render_template("updated.html", msg = msg)

#------------------------------------------------------------
# a page for displaying the buggy
#------------------------------------------------------------
@app.route('/buggy')
def show_buggies():
  con = sql.connect(DATABASE_FILE)
  con.row_factory = sql.Row
  cur = con.cursor()
  cur.execute("SELECT * FROM buggies")
  record = cur.fetchone();
  return render_template("buggy.html", buggy = record)

#------------------------------------------------------------
# a page for displaying the buggy
#------------------------------------------------------------
@app.route('/new')
def edit_buggy():
  return render_template("buggy-form.html")


#------------------------------------------------------------
# get JSON from current record
#   this is still probably right, but we won't be
#   using it because we'll be dipping diectly into the
#   database
#------------------------------------------------------------
@app.route('/json')
def summary():
  con = sql.connect(DATABASE_FILE)
  con.row_factory = sql.Row
  cur = con.cursor()
  cur.execute("SELECT * FROM buggies WHERE id=? LIMIT 1", (DEFAULT_BUGGY_ID))
  return jsonify(
      {k: v for k, v in dict(zip(
        [column[0] for column in cur.description], cur.fetchone())).items()
        if (v != "" and v is not None)
      }
    )

#------------------------------------------------------------
# delete the buggy
#   don't want DELETE here, because we're anticipating
#   there always being a record to update (because the
#   student needs to change that!)
#------------------------------------------------------------
@app.route('/delete', methods = ['POST'])
def delete_buggy():
  try:
    msg = "deleting buggy"
    with sql.connect(DATABASE_FILE) as con:
      cur = con.cursor()
      cur.execute("DELETE FROM buggies")
      con.commit()
      msg = "Buggy deleted"
  except:
    con.rollback()
    msg = "error in delete operation"
  finally:
    con.close()
    return render_template("updated.html", msg = msg)


if __name__ == '__main__':
   app.run(debug = True, host="0.0.0.0")
