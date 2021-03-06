# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

###################################################### DOCUMENTATION ####################################################

Endpoints
GET '/categories'
GET '/questions'
GET '/categories/category_id/questions'
POST '/questions'
POST '/search_questions'
POST '/quizzes'
DELETE '/questions/question_id'

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

GET '/questions'
- Fetches a dictinoary of questions in which the kays are the ids and values are the corresponding string of the Question , Answer , Categries . and integres for total questions, current_category
- Request Arguments: None
- Returns: objects with a multiplay keys, categries,questions,current category,Total questions that contains a objects of categories : category_string ,current_category: category_int , questions : question_collection ,total_questions : total_questions_int . key:categories , current_category ,questions, total_questions. 

-Return
{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "current_category": [
    "4", 
    "3", 
    "5", 
    "6"
  ], 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": "5", 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": "5", 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": "4", 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": "5", 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": "4", 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": "6", 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": "6", 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": "4", 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": "3", 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": "3", 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "total_questions": 20
}


GET '/categories/category_id/questions'
-Fetches : Questions that related to a certen category using the category_id to get question of that category 
-Request Arguments: category_id : id of wanted category
-Returns : object with a multiplay keys, categries,questions,current category,Total questions that contains a objects of 
categories : category_string ,current_category: category_int , questions : question_collection, total_questions: total_questions_int.  key :categories , current_category ,questions, total_questions. 

-Return
  "categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    }, 
    {
      "id": 3, 
      "type": "Geography"
    }, 
    {
      "id": 4, 
      "type": "History"
    }, 
    {
      "id": 5, 
      "type": "Entertainment"
    }, 
    {
      "id": 6, 
      "type": "Sports"
    }
  ], 
  "current_category": [
    "1"
  ], 
  "questions": [
    {
      "answer": "The Liver", 
      "category": "1", 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": "1", 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": "1", 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ], 

  "total_questions": 3
}


POST '/questions'
-Fetches: adding a question to the list of questions by selecting the Question , Answer , Difficulty , Category 
-Request Arguments: Question,Answer,Difficulty,Category
-Returns : a boolean object that indicate whether the adding is successful or not. object: Success_boolean .          key : success 

-Return
{
"success": true
}


POST '/search_questions'
-Fetchs: a search string object that filters question based on it , and view and only the questions with that search term.
-Request Arguments: Search Term 
-Returns an object of questions based on searchTerm. object : question_collection .key: questions, 

-Return 
{
  	"questions": [
    {
      "answer": "Apollo 13", 
      "category": "5", 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
      ]
    }



POST '/quizzes'
-Fetches: playing the trivia returing a random questions within the given category, if provided, and that is not one of the previous questions.
-Request Arguments: category: category in which the pool of questions is from , previous question: an aready answerd question 
-Returns: a score of 5 based on 5 questions answerd correctly also, an object of previous question and category,  objects : previous_questions:previous_questions_collection , quiz_category: quiz_category_collection. key:previous_questions, quiz_category

-Return
 {
"previous_questions": [47], quiz_category: {type: "Geography", id: "1"}}
"previous_questions": [47]
"quiz_category": {type: "Geography", id: "1"}
 }



DELETE '/questions/question_id'
-Fetchs: deleting a question based on the questions_id.
-Request Arguments: question_id : id of question wanted to be deleted 
-Returns:  a boolean object that indicate whether the deleting was successful or not. object: Success_boolean .          key : success 

-Return
 {
"success": true
 }

################################################## Error Handlers ######################################################

-Error 400 : happen when a request is somehow incorrect.
-return:
{
'success':False,
'error':400,
'message':'Bad request ,Something went wrong try again later'
}

-Error 401 : happen when a request is not authorized.
-return:
{
  'success':False,
  'error':401,
  'message':'Unauthorized , Try again later'
}

-Error 404 : happen when a question is not found .
-return:
{
'success':False,
'error':404,
'message':'Sorry question was not found'
}

-Error 405 : happen when a request(method) is not allowed.
-return:
{
'success':False,
'error':405,
'message':'Sorry this method is Not Allowed'
}

-Error 422: happen when a request is not unprocessable.
-Return:
{
'success':False,
'error':422,
'message':'Unprocessable Entity , the server unable to process the contained instructions.'
}

-Error 500 : happen when there is a Server Error .
-Return:
{
'success':False,
'error':500,
'message':'Internal Server Error,Try again later'  
}
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```