from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///sqlite/subscribers.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy()
db.init_app(app)


class Subscriber(db.Model):
    __tablename__ = "subscribers"
    id = db.Column(db.Integer, primary_key=True)
    total_money = db.Column(db.Integer, nullable=True)
    other = db.Column(db.Integer, nullable=True)
    debts = db.Column(db.Integer, nullable=True)
    counter = db.Column(db.Integer, nullable=True)
    breaker = db.Column(db.Integer, nullable=True)
    curr_reading_at = db.Column(db.String, nullable=True)
    curr_reading = db.Column(db.Integer, nullable=True)
    prev_reading_at = db.Column(db.String, nullable=True)
    prev_reading = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String, nullable=True)
    account = db.Column(db.String, nullable=True)
    subscription = db.Column(db.Integer, nullable=True)
    address = db.Column(db.String, nullable=True)
    house_number = db.Column(db.Integer, nullable=True)

@app.route("/")
def index():

    layout = {
        "line_one": [("total_money", "other", "debts", "counter", "breaker", "curr_reading_at", "curr_reading",
                      "prev_reading_at", "prev_reading", "name", "account"),
                     (14, 28, 42, 50, 57, 69, 77, 89, 97)],
        "line_two": [("subscription", "address", "house_number"),
                     (9, 35)]
    }

    try:
        input_file = open("sss.txt", encoding='utf8')
        lines = input_file.readlines()
    except:
        print("error while reading input file")

    # will contain the data for one row entry in the db, this is done by scanning two lines relating to one subscriber keys "line_one" or "line_two"
    scanDict = {}

    # read lines one by one, and process lines for user by user (usually, process two lines)
    for newLine in lines:
        if newLine.count('/') >= 2:
            scanDict["line_one"] = newLine
            continue
        if scanDict.get("line_one") and (newLine[0] == " " and not newLine.count('*') >= 1):
            scanDict["line_two"] = newLine
            continue
        kwQuery = {}
        for key, line in scanDict.items():
            colName, colIndexes = layout[key]
            prev_index = 0
            cells = []
            for curr_index in colIndexes:
                cells.append(line[prev_index:curr_index].strip())
                prev_index = curr_index
            last_cell = line[prev_index:]
            if key == "line_one":
                m_index = last_cell.index('   ')
                cells.append(last_cell[:m_index - 1])
                cells.append(last_cell[m_index:])
            else:
                cells.append(last_cell)
            for i, cell in enumerate(cells):
                try:
                    col = colName[i]
                    kwQuery[col] = cell.strip()
                except:
                    print("Error while printing the values")
        db.session.add(Subscriber(**kwQuery))
        scanDict = {}  # clear the dictionary of the user, to start adding new users data.
    db.session.commit()
    return render_template("index.html", test=kwQuery)

if __name__ == "__main__":
	app.run(debug=True)
