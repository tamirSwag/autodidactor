import appearances
import re
from flask import jsonify
import terms_provider
# encoding=utf8
import sys
from multiprocessing.dummy import Pool as ThreadPool
import categoryAutocomleter

reload(sys)
sys.setdefaultencoding('utf8')

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def remove_parentheses(str):
    return re.sub(r"[\(\[].*?[\)\]]", "", str)

@app.route("/")
def asdf():
    return "asdf"

@app.route("/getGraph/<subject>")
def getGraph(subject):
    terms = list(terms_provider.get_final_terms(subject, 0))
    print 'terms count: ' + str(len(terms))
    terms_passed = list(map(lambda x: (remove_parentheses(x).lower().strip(), terms, subject), terms))
    print terms_passed
    pool = ThreadPool(100)
    results = pool.map(appearances.build_appearances_dict, terms_passed)
    return jsonify(results)

@app.route("/getAutocomplete/<input>")
def getAutocomplete(input):
    options = categoryAutocomleter.getOptions(input)
    optionsDict = { "options" : options }
    return jsonify(optionsDict)

app.run()