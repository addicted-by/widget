from importlib.resources import path
import json
import pickle
import math
import os

from pyexpat import model
from flask import request, abort, make_response, redirect, render_template
from flask import Flask
from flask import jsonify
from json import dumps

#from torch import negative_

app = Flask(__name__)

@app.before_first_request
def load_global_data():
    global model
    
    with open(os.path.join('models/', 'knn_classifier.pkl'), 'rb') as fid:
        model = pickle.load(fid)

def bad_request(message, code=400):
    abort(make_response(jsonify(message=message), code))

@app.route('/analyse', methods=['GET'])
def analyze():
    url = request.args.get('link', type=str)

    ml_comment_color = 'red'
    ml_comment_sentences = ["I'm impressed", "but just kidding"]
    ml_comment_sentence_colors = ['green', 'red']
    ml_comment_json = json.dumps({
            'color': ml_comment_color, 
            'sentences': ml_comment_sentences, 
            'sentence_colors': ml_comment_sentence_colors})

    mc_comment_color = 'green'
    mc_comment_sentences = ["I really like it"]
    mc_comment_sentence_colors = ['green']
    mc_comment_json = json.dumps({
            'color': mc_comment_color, 
            'sentences': mc_comment_sentences, 
            'sentence_colors': mc_comment_sentence_colors})
    
    youtube_title = "Focus Official Trailer #1 (2015) - Will Smith, Margot Robbie Movie HD"
    path_word_clouds = os.path.join('./static/', 'wordscloud.png')
    positive_percentage = "40%"
    negative_percentage = "60%"
    ml_value_of_likes = "400"
    ml_value_of_comments = "14"
    mc_value_of_likes = "40"
    mc_value_of_comments = "4"
    return render_template('analysis.html', 
                            youtube_title=youtube_title,
                            path_word_clouds=path_word_clouds,
                            positive_percentage=positive_percentage,
                            negative_percentage=negative_percentage,
                            context_str=url,

                            ml_comment_json=ml_comment_json,
                            mc_comment_json=mc_comment_json,

                            ml_value_of_likes=ml_value_of_likes,
                            ml_value_of_comments=ml_value_of_comments,
                            mc_value_of_likes=mc_value_of_likes,
                            mc_value_of_comments=mc_value_of_comments
                            )

@app.route('/')
def main_page():
    return render_template('main_page.html')
    
if __name__ == '__main__':
    app.run()