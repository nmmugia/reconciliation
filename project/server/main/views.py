# project/server/main/views.py


from flask import render_template, Blueprint, flash, redirect, url_for, request, current_app
from project.server.main.helpers import CompareTwoDict, ConvertCSVtoDict, wrapper, SuggestPossibilities
from project.server.main.forms import UploadForm
from threading import Thread
from queue import Queue

main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def home():
    """
    Render the home page with upload form
    """

    uploadform = UploadForm()
    return render_template("main/home.html", uploadform=uploadform)


@main_blueprint.route("/about/")
def about():
    """
    Render the about page
    """
    return render_template("main/about.html")


@main_blueprint.route('/upload', methods=['POST'])
def upload():
    """
    /upload [POST]
    a function to handle file uploads of 2 csvs
    the function would compare the 2 csvs and return the result
    it will redirect to home with the result  
    """
    uploadform = UploadForm()
    if uploadform.validate_on_submit():
        # convert csv to dict
        q1, q2 = Queue(), Queue()
        Thread(target=wrapper, args=(ConvertCSVtoDict, uploadform.file1.data, q1)).start() 
        Thread(target=wrapper, args=(ConvertCSVtoDict, uploadform.file2.data, q2)).start()
        dict1, dict2 = q1.get(), q2.get()

        # validation if the header of two files is not the same
        if dict1["header"] != dict2["header"]:
            flash("The two files do not have the same header")
            return redirect(url_for('main.home'))
        # compare two dict
        dict_report1 = CompareTwoDict(dict1, dict2)
        dict_report2 = CompareTwoDict(dict2, dict1)
        if "errors" in dict_report1 and (dict_report1["errors"] != None or dict_report2["errors"] != None):
            flash("File is not compatible with the application")
            return redirect(url_for('main.home'))
        dict_report1, dict_report2 = SuggestPossibilities(dict_report1, dict_report2, dict1["header"])
        
        return render_template("main/home.html", uploadform=uploadform, dict_report={
            "data":[
                {
                    "filename": uploadform.file1.data.filename,
                    "dict_report": dict_report1,
                    "total_data": dict1["total_data"],
                    "header": dict1["header"],
                    "duplicate_data": dict1["duplicate_data"],
                }, {
                    "filename": uploadform.file2.data.filename,
                    "dict_report": dict_report2,
                    "total_data": dict2["total_data"],
                    "header": dict2["header"],
                    "duplicate_data": dict2["duplicate_data"],
                }
            ]
        })
    
    flash("file is invalid, kindly check the file again")
    return redirect(url_for('main.home'))
