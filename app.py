from flask import Flask, render_template, send_from_directory, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///sqlite/subscribers.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

UPLOAD_FOLDER = './upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt'])

# app.config["SQLALCHEMY_DATABASE_URI"] = "access+pyodbc://@subscribers"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

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
    unknwon = db.Column(db.String, nullable=True)
    meem_yaa = db.Column(db.String, nullable=True)
    record = db.Column(db.String, nullable=True)
    page = db.Column(db.String, nullable=True)
    meem_yaa_at = db.Column(db.String, nullable=True)
    hissab = db.Column(db.String, nullable=True)

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
            'unknown': self.unknown,
            'meem_yaa': self.meem_yaa,
            'record': self.record,
            'page': self.page,
            'meem_yaa_at': self.meem_yaa_at,
            'hissab': self.hissab
        }


def log_error(error):
    try:
        file_name = "error_log.txt"
        with open(file_name, "a") as errors_log:
            errors_log.write(f"{error}\n{datetime.now()}\n \n")
    except Exception as e:
        "do nothing"


def scan_file(file_names):
    layout = {
        "line_one": [("total", "other", "debts", "counter", "breaker", "curr_reading_at", "curr_reading",
                      "prev_reading_at", "prev_reading", "name", "account"),
                     ((0, 14), (14, 28), (28, 42), (42, 50), (50, 57), (57, 69), (69, 77), (77, 89), (89, 97),
                      (-33, -9), (-9, -1))],
        "line_two": [("subscription", "address", "house_number", "unknwon"),
                     ((0, 9), (9, 34), (35, 52), (52, -1))],
        "title": [("meem_yaa", "record", "page", "meem_yaa_at"),
                  ((39, 45), (90, 94), (108, 114), (116, -1))]
    }
    # del previous database content, to prepare it for the new files
    with app.app_context():
        db.drop_all()
        db.create_all()
    for file_name in file_names:
        try:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'],file_name)
            input_file = open(file_path, encoding="utf-8")
            lines = input_file.readlines()
        except:
            log_error(f"error while read {file_name}")
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
                            log_error("error while read the inserting subscribers data to the database")
                kwQuery['hissab'] = f"{kwQuery['record']}{kwQuery['account'][2:]}"
                if scanDict:
                    db.session.add(Subscriber(**kwQuery))
                del scanDict["line_one"]
                if scanDict.get("line_two"):
                    del scanDict["line_two"]
    db.session.commit()


@app.route("/")
def index():
    # scan_file()
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():
    temp_names = []
    for temp_file in request.files.getlist("file[]"):
        temp_file.save(os.path.join(app.config["UPLOAD_FOLDER"], temp_file.filename))
        temp_names.append(temp_file.filename)
    scan_file(temp_names)
    # removing files after finishing reading them
    for temp_name in temp_names:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'],temp_name))
    # os.system('copy hhh.txt mmm.txt') # this executes in command line !
    return render_template("index.html", test="done")
    return send_from_directory(app.config['UPLOAD_FOLDER'], "subscribers.accdb", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
