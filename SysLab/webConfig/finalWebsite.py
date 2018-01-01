from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
#from clueSolver import solveClue
#from visionCrossword import getGrid

app = Flask(__name__)

@app.route('/')
def hello_world():
	#answers = []
	return render_template('webTemplateCrossword.html')
	#return render_template('webTemplate.html', answers=answers)
	#return 'Hello World!'

@app.route('/possibleAnswers', methods = ['POST'])
def possibleAnswers():
	clue = request.form['clue']
	length = request.form['length']
	#print(str(request.form['pic']))
	#print("The email address is '" + email + "'")
	answers = solveClue(clue,int(length))
	grid = getGrid(str(request.form['pic']))
	return render_template('webTemplateCrossword.html', answers=answers)

 
if __name__ == "__main__":
	app.run()