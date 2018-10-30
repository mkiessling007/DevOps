from flask import Flask
from flask import render_template
import subprocess
import rest_call

from gui import app
from gui.forms import RestApiForm

@app.route("/")
def tools():
    return render_template('index.html', title = 'SDN', toolname = 'RestAPI')

@app.route("/restapicall", methods=['GET', 'POST'])
def get_arguments():
    form = RestApiForm()
    if form.validate_on_submit():
        cli_arguments = '/Users/michael/GitHub/DevOps/rest_call.py -a {} -u {} -p {} -c {} --html'.format(
                        form.hostname.data.encode('utf-8'),
                        form.username.data.encode('utf-8'),
                        form.password.data.encode('utf-8'),
                        form.restapicall.data.encode('utf-8'))
        if form.prime:
            cli_arguments = cli_arguments + ' --prime'
            text = subprocess.check_output(cli_arguments, shell=True)
        else:
            text = subprocess.check_output(cli_arguments, shell=True)
        return text
    return render_template('tools.html', title = 'Sign In', form = form)

@app.route("/test")
def cliTest():
    text = subprocess.check_output(['/home/ec2-user/GitHub/DevOps/rest_call.py',
                                    '-asandboxapicem.cisco.com','-udevnetuser','-pCisco123!','-c/api/v1/network-device', '--html'])
    return text
    #return render_template('tools.html', title='Home', toolname='RestAPI', results=text)
