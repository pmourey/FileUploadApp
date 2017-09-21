#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from flask import Flask, render_template, request, flash, redirect, url_for

import json
# get this object prout
from flask import Response, make_response

from flask_debugtoolbar import DebugToolbarExtension
from var_dump import var_dump
from werkzeug.utils import secure_filename
from flask import send_file

app = Flask('__name__')

app.config.update(
    DEBUG=True,
    SECRET_KEY='d66HR8dç"f_-àgjYYic*dh',
    UPLOAD_FOLDER='/Users/philippemourey/upwork/files/',
    UPLOAD_DEV_FOLDER='/Users/philippemourey/upwork/files/DEV/',
    UPLOAD_TEST_FOLDER='/Users/philippemourey/upwork/files/TEST/',
    UPLOAD_PROD_FOLDER='/Users/philippemourey/upwork/files/PROD/'
)

#Easier Debugging of Your Flask Apps With Debug Toolbar 
toolbar = DebugToolbarExtension(app)
app. config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# returns the environment selected in the ComboBox
def get_env_path(envName):
    if envName == 'DEV':
        envPath = app.config['UPLOAD_DEV_FOLDER']
    elif envName == 'TEST':
        envPath = app.config['UPLOAD_TEST_FOLDER']
    elif envName == 'PROD':
        envPath = app.config['UPLOAD_PROD_FOLDER']
    else:
        flash('No selected environment!', 'error')
    return envPath

# returns the directory's list belonging to the selected environment
def get_dir_path(envPath):
    targetDirs = list()
    for file in os.listdir(envPath):
        if os.path.isdir(os.path.join(envPath, file)):
            targetDirs.append(file)
    return targetDirs

# route called by an AJAX request to update the HTML form when the user selects a new environment
@app.route('/dirlist/<string:env_name>/', methods=['POST'])
def update_DestDir(env_name):
    envPath = get_env_path(env_name)
    targetDirs=get_dir_path(envPath)
    response = make_response(json.dumps(targetDirs))
    response.content_type = 'application/json'
    return response

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    envPath = app.config['UPLOAD_DEV_FOLDER']
    targetDirs=get_dir_path(envPath)
    #var_dump(targetDirs)
    if request.method == 'POST':
        if request.form['pw'] == 'up': # check password is correct
            envName = request.form.get('EnvName')
            envPath = get_env_path(envName)
            dirName = request.form.get('DestDir')
            targetDir = os.path.join(envPath, dirName)
            # check if the post request has the file part
            file1 = request.files['UploadFile1']
            file2 = request.files['UploadFile2']
            file3 = request.files['UploadFile3']
            if file1 or file2 or file3:
                if file1:
                    filename1 = secure_filename(file1.filename)
                    file1.save(os.path.join(targetDir, filename1))
                    flash('{filename} successfully sent ! Here is <a href="{lien}">the link</a>.'.format(lien=url_for('upped', envName=envName, dirName=dirName, fileName=filename1), filename=filename1), 'succes')
                if file2:
                    filename2 = secure_filename(file2.filename)
                    file2.save(os.path.join(targetDir, filename2))
                    flash('{filename} successfully sent ! Here is <a href="{lien}">the link</a>.'.format(lien=url_for('upped', envName=envName, dirName=dirName, fileName=filename2), filename=filename2), 'succes')
                if file3:
                    filename3 = secure_filename(file3.filename)
                    file3.save(os.path.join(targetDir, filename3))
                    flash('{filename} successfully sent ! Here is <a href="{lien}">the link</a>.'.format(lien=url_for('upped', envName=envName, dirName=dirName, fileName=filename3), filename=filename3), 'succes')
            else:
                flash('No selected file !', 'error')
                #return redirect(url_for('upload_file'))
                return redirect(request.url)
        else:
            flash('Incorrect password!', 'error')    
    return render_template('up_up.html', target_dirs=targetDirs)

@app.route('/view/<string:envName>/<string:dirName>/')
def liste_upped(envName, dirName):
    envPath = get_env_path(envName)
    dirPath = os.path.join(envPath, dirName)
    fileNames = [filename for filename in os.listdir(dirPath)] # la liste des images dans le dossier
    return render_template('up_liste.html', envName=envName, dirName=dirName, fileNames=fileNames)

@app.route('/view/<string:envName>/<string:dirName>/<string:fileName>')
def upped(envName, dirName, fileName):
    envPath = get_env_path(envName)
    dirPath = os.path.join(envPath, dirName)
    nom = secure_filename(fileName)
    if os.path.isfile(dirPath + '/' + nom): # si le fichier existe
        return send_file(dirPath + '/' + nom, as_attachment=True) # on l'envoie
    else:
        flash('Fichier {nom} inexistant.'.format(nom=nom), 'error')
        return redirect(url_for('liste_upped', envName=envName, dirName=dirName)) # sinon on redirige vers la liste des images, avec un message d'erreur

if __name__ == '__main__':
    #app.run()
    app.run(host='0.0.0.0',debug=True)
