from flask import Flask, request, render_template
import smtplib
import ssl

app = Flask(__name__)

# BASIC INFO
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "rajvspav@gmail.com"  # Enter your address
password = "rajvspav123$"


context = ssl.create_default_context()


class ViewerDB:
    def __init__(self):
        self.viewers = {}

    def get(self, name):
        if name in self.viewers:
            return self.viewers[name]
        return None

    def get_all(self):
        return self.viewers.values()

    def insert(self, viewer):
        if viewer.name in self.viewers.keys():
            return None
        self.viewers[viewer.name] = viewer
        viewer.send_email()


viewerDB = ViewerDB()


class Viewer:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def send_email(self):
        message = f"""
        Hi {self.name},

        You have been invited to Raj vs Pav. Please show this email to be admitted to the fight.

        Regards,
        Your friends at RajVsPav Inc.
        """
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, self.email, message)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/createuser", methods=["POST"])
def create_new_user():
    payload = request.form
    name, reciever_email = payload["name"], payload["email"]
    viewer = Viewer(name, reciever_email)
    viewerDB.insert(viewer)
    return "You have registered"
