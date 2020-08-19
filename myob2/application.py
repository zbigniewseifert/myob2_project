#!/usr/bin/python3
from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory
from service import FileDBService, Tools
from models import Schema
import re
import os
import string
import random
from healthcheck import HealthCheck, EnvironmentDump
import json

app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif', '.jpeg']
app.config['UPLOAD_PATH'] = 'upload_files'
app.config['APP_FILES'] = 'app_files'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

health = HealthCheck(app, "/health")
health.add_check(Tools.healthcheck_db)
health.add_check(Tools.healthcheck_uploads_dir)

@app.before_request
def before_request_func():
    print("before_request is running!")

@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] =  "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods']=  "POST, GET, PUT, DELETE, OPTIONS"
    return response


@app.route('/')
@app.route('/index')
def index():
    files_data = []
    files = os.listdir(app.config['UPLOAD_PATH'])

    if len(files) > 0:
        for file in files:
            try:
                ID = Tools.get_file_id(file)
                PATH = Tools.get_file_path(file)
                RANK = Tools.get_file_rank(ID)
                DESC = Tools.get_file_description(file)
                file_data = {'file_id': ID,'filename':file, 'filepath': PATH,'file_rank': RANK,'description':DESC}
                files_data.append(file_data)
            except:
                print("Exception for path {P} and file {F}".format(P=app.config['UPLOAD_PATH'],F=file))
                continue

    else:
        files_data = [{'file_id':0,'filename':'NoFiles.jpeg','filepath': 'app_files','file_rank':0}]
    return render_template('index.html', title='Home', files_data=sorted(files_data, key = lambda i: i['file_rank']) )


@app.route('/search', methods=['GET', 'POST'])
def search_item():
    if request.method == 'POST':
        item_nr = request.form['item']
        if item_nr == "":
            search_result = FileDBService().list(where_clause="")
        else:
            try:
                item_nr = int(item_nr)
            except:
                return render_template('search.html')
            search_result = FileDBService().list(where_clause=" AND ID={I}".format(I=item_nr))

        return render_template('search_result.html', items=search_result )
    return render_template('search.html',action='search')

@app.route('/vote',methods=['GET','POST'])
def vote_item():
    if request.method == 'POST':
        search_result = FileDBService().list(where_clause="")
        try:
            file_id = int(request.form['file_id'])
        except:
            return render_template('vote.html',current_list=search_result)
        if len(list(filter(lambda file: file['id'] == file_id, search_result))) > 0:
            update_result = Tools.vote_for_file(request.form['file_id'])
            return render_template('vote_result.html', item=update_result[0])
        else:
            return render_template('vote.html',current_list=search_result)
    else:
        search_result = FileDBService().list(where_clause="")
        return render_template('vote.html',current_list=search_result)

@app.route("/del",methods=['GET','POST'])
def del_item():
    if request.method == 'POST':
        item_nr = request.form['item']
        if item_nr == "":
            return render_template('delete.html',action='del')
        else:
            try:
                item_nr = int(item_nr)
            except:
                return render_template('delete.html',action='del')
            if Tools.delete_upload_file(item_nr): #FileDBService().delete(item_nr):
                return render_template('delete_result.html', item="Deleted",action='del' )
    return render_template('delete.html',action='del')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            file_ext = os.path.splitext(uploaded_file.filename)[1]
            new_file_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))+file_ext
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                return render_template('upload.html')
            #uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], uploaded_file.filename))
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], new_file_name))
            Tools.add_file_data(new_file_name,app.config['UPLOAD_PATH'],request.form['description'])
        return redirect(url_for('index'))
    return render_template('upload.html')

@app.route('/upload_files/<filename>')
def upload_files(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

@app.route('/app_files/<filename>')
def app_files(filename):
    return send_from_directory(app.config['APP_FILES'], filename)

@app.route('/metadata')
def metadata_check():
    return  jsonify(Tools.read_app_metadata())



if __name__ == "__main__":
    Schema()
    app.run(host='0.0.0.0', port=8888)
