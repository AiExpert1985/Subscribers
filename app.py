from flask import Flask, render_template, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///sqlite/subscribers.sqlite3'
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

UPLOAD_FOLDER = './db'
ALLOWED_EXTENSIONS = set(['txt'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config["SQLALCHEMY_DATABASE_URI"] = "access+pyodbc://@subscribers"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy()
db.init_app(app)

class Subscriber(db.Model):
    __tablename__ = "subscribers"
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.String, nullable=True)
    other = db.Column(db.String, nullable=True)
    debts = db.Column(db.String, nullable=True)
    counter = db.Column(db.String, nullable=True)
    breaker = db.Column(db.String, nullable=True)
    curr_reading_at = db.Column(db.String, nullable=True)
    curr_reading = db.Column(db.String, nullable=True)
    prev_reading_at = db.Column(db.String, nullable=True)
    prev_reading = db.Column(db.String, nullable=True)
    name = db.Column(db.String, nullable=True)
    account = db.Column(db.String, nullable=True)
    subscription = db.Column(db.String, nullable=True)
    address = db.Column(db.String, nullable=True)
    house_number = db.Column(db.String, nullable=True)
    meem_yaa = db.Column(db.String, nullable=True)
    record = db.Column(db.String, nullable=True)
    page = db.Column(db.String, nullable=True)
    meem_yaa_at = db.Column(db.String, nullable=True)

    @property
    def serialize(self):
        """ Changing Model objects to dictionary which will be used later as json (for Ajax)"""
        return {
            'total': self.total,
            'other': self.other,
            'debts': self.debts,
            'counter': self.counter,
            'breaker': self.breaker,
            'curr_reading_at': self.curr_reading_at,
            'curr_reading': self.curr_reading,
            'prev_reading_at': self.prev_reading_at,
            'prev_reading': self.prev_reading,
            'name': self.name,
            'account': self.account,
            'subscription': self.subscription,
            'address': self.address,
            'house_number': self.house_number,
            'meem_yaa': self.meem_yaa,
            'record': self.record,
            'page': self.page,
            'meem_yaa_at': self.meem_yaa_at
        }

def scanFile():

    with app.app_context():
        db.drop_all()
        db.create_all()

    layout = {
        "line_one": [("total", "other", "debts", "counter", "breaker", "curr_reading_at", "curr_reading",
                      "prev_reading_at", "prev_reading", "name", "account"),
                     ((0, 14), (14, 28), (28, 42), (42, 50), (50, 57), (57, 69), (69, 77), (77, 89), (89, 97),
                      (-33, -9), (-9, -1))],
        "line_two": [("subscription", "address", "house_number"),
                     ((0, 9), (9, 35), (35, -1))],
        "title": [("meem_yaa", "record", "page", "meem_yaa_at"),
                  ((43, 49), (94, 97), (113, 117), (120, -1))]
    }

    try:
        input_file = open("subscribers.txt", encoding='utf8')
        lines = input_file.readlines()
    except:
        exit(1)
    scanDict = {}
    for newLine in lines:
        if "جدول القوائم المطبوعة" in newLine:
            scanDict["title"] = newLine
            continue
        if newLine.count('/') >= 2 and len(newLine) > 100:
            scanDict["line_one"] = newLine
            continue
        if scanDict.get("line_one") and (newLine[0] == " " and not newLine.count('*') >= 1):
            scanDict["line_two"] = newLine
        if scanDict.get("line_one"):
            kwQuery = {}
            for line_name, line_data in scanDict.items():
                col_names, col_indexes = layout[line_name]
                for n, indexes in enumerate(col_indexes):
                    db_col_name = col_names[n]
                    start = indexes[0]
                    end = indexes[1]
                    db_col_data = line_data[start:end]
                    try:
                        kwQuery[db_col_name] = db_col_data.strip()
                    except:
                        exit(1)
            if scanDict:
                db.session.add(Subscriber(**kwQuery))
            del scanDict["line_one"]
            if scanDict.get("line_two"):
                del scanDict["line_two"]
    db.session.commit()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/subscribers")
def subscribers():
    scanFile()
    return jsonify([x.serialize for x in Subscriber.query.all()])

@app.route("/download")
def download():
    return send_from_directory(app.config['UPLOAD_FOLDER'], "subscribers.accdb", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
