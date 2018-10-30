from flask import Flask
from flask import render_template
import subprocess

from gui import app
from gui.forms import RestApiForm

@app.route("/")
def tools():
    return render_template('index.html', title='SDN', toolname='RestAPI')

@app.route("/restapicall", methods=['GET', 'POST'])
def get_arguments():
    form = RestApiForm()
    if form.validate_on_submit():
     text = subprocess.check_output(['/home/ec2-user/GitHub/DevOps/rest_call.py','-a' + form.hostname.data,
                                     '-u' + form.username.data,'-p' + form.password.data,'-c' + form.restapicall.data, '--html'])
     return text
    return render_template('tools.html', title='Sign In', form=form)

@app.route("/test")
def hello():
    text = subprocess.check_output(['/home/ec2-user/GitHub/DevOps/rest_call.py','-asandboxapicem.cisco.com','-udevnetuser','-pCisco123!','-c/api/v1/network-device', '--html'])
    return text
    #return render_template('tools.html', title='Home', toolname='RestAPI', results=text)
