<h1>Capstone Project: Casting Agency</h1>

<h2>Introduction</h2>

<p>This last project is a combination of all the skills I was tought throughout the course of the Full Stack Developer Nanodegree(FSDN), 
including:</p>
<ul>
    <li>SQL and Data Modeling for the Web</li>
    <li>API Development and Documentation</li>
    <li>Identity and Access Management</li>
    <li>Server Deployment, Containerization and Testing</li>
</ul>

<h2>Dependencies</h2>

<h3>### Python 3.7.4</h3>
<p>
Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/windows.html?highlight=installing%20latest%20version%20python)
</p>

<h3>### PIP Dependencies</h3>
<p>

```bash
pip install -r requirements.txt
```
This will install all of the required packages for this project.
</p>

<h3>### Running the server</h3>
<p>
To run the server inside the root directory, open a new terminal session, and run:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
```

To run the server, execute:

```bash
flask run 
```



<h2>Tasks</h2>
<p> in order to use the app properly follow the fowling steps:
</p><br>
<h3>### Setup Auth0</h3>
<ol>
    <li>Create a new Auth0 Account</li>
    <li>Select a unique tenant domain</li>
    <li>Create a new, single page web application</li>
    <li>Create a new API
        - in API Settings:
            <ul>
                <li>Enable RBAC</li>
                <li>Enable Add Permissions in the Access Token</li>
            </ul>
    </li>
    <li>Create new API permissions:
        <ul>
            <li>get:actors</li>
            <li>get:movies</li>
            <li>post:actor</li>
            <li>post:movie</li>
            <li>patch:actor</li>
            <li>patch:movie</li>
            <li>delete:actor</li>
            <li>delete:movie</li>
        </ul>
    </li>
    <li>Create new roles for:
        <ul>
            <li> Assistant<br/>
                - can get:actors and get: movies
            </li>
            <li> Director<br/>
                - can get:actors and get: movies<br/>
                - can post:actor and delete:actor<br/>
                - can patch:actor and patch:movie<br/>
            </li>
            <li> Producer<br/>
                - can perform all actions<br/>
            </li>
        </ul>
    </li>
    <li>Register 3 users
        <ul>
            <li>Assign the  Assistant role to one</li>
            <li>Assign the  Director role to another</li>
            <li>Assign the  Producer role to the last one </li>
        </ul>
    </li>
    <li>Sign into each account and make note of the JWT.</li>
    <li>Test the endpoints with the latest version of [Postman](https://getpostman.com). 
        <ul>
            <li>Import the postman collection "./CastingAgency_FSND.postman_collection.json"</li>
            <li>Right-clicking the collection folder for Assistant, Director and Producer, navigate to the authorization tab, and include the JWT in the token field (you should have noted these JWTs).</li>
            <li>Run the collection.</li>
            <li>The collection points to heroku app hosted on : https://appv22.herokuapp.com/</li>
        </ul>
    </li>
</ol>

<h3>### Testing</h3>
To run the unit tests, execute:

```bash
python3 test_app.py
```
Note - make sure the 3 header variables(assistant_header , director_header , producer_header) are updated for each role JWT collected.

<h2>API behavior and RBAC controls</h2>
<h3>### Endpoints</h3>
<ul>
    <li>GET /actors</li>
    <li>GET /movies</li>
    <li>PATCH /actors/&lt;id&gt;</li>
    <li>PATCH /movies/&lt;id&gt;</li>
    <li>POST /actors</li>
    <li>POST /movies</li>
    <li>DELETE /actors/&lt;id&gt;</li>
    <li>DELETE /movies/&lt;id&gt;</li>
</ul>

<h3>GET /actors</h3>
<ul>
    <li>Returns a list of all actors</li>
    <li>Requires auth permission get:actors</li>
    <li>Request: None</li>
    <li>Response:
    
    {
    "actors": [
        {
            'name': 'Daniel Craig',
            'age': '52',
            'gender': 'Male',
            'id': 1
        },
        {
            name': 'Chris Evans',
            'age': '38',
            'gender': 'Male',
            'id': 2
        }
    ],
    "success": true
    }
</li>
</ul>
<h3>GET /movies</h3>
<ul>
    <li>Returns a list of all movies</li>
    <li>Requires auth permission get:movies</li>
    <li>Request: None</li>
    <li>Response:

    {
    "movies": [
        {
            "id": 1,
            'title': 'Space',
            'release_date': '2020'
        },
        {
            "id": 2,
            'title': 'Knives Out ',
            'release_date': '2019'
        }
    ],
    "success": true
    }
</li>
</ul>
<h3>PATCH /actors/&lt;id&gt;</h3>
<ul>
    <li>Updates a selected actor by id</li>
    <li>Requires auth permission patch:actor</li>
    <li>Request:
        
    {
        "name": "Updated name",
        "age": 49,
        "gender": "Male"
    }
</li>
    <li>Response:

    {
        "success": true
    }
</li>
</ul>
<h3>PATCH /movies/&lt;id&gt;</h3>
<ul>
    <li>Updates a selected movie by id</li>
    <li>Requires auth permission patch:movie</li>
    <li>Request: 
    
    {
        "title": "Updated title",
        "release_date": "2015"
    }
</li>
    <li>Response:

    {
        "success": true
    }
</li>
</ul>
<h3>POST /actors</h3>
<ul>
    <li>Adds a new actor</li>
    <li>Requires auth permission post:actor</li>
    <li>Request: 
    
    {
        'name': 'Daniel Craig',
        'age': '52',
        'gender': 'Male'
        
    }
</li>
    <li>Response:
    
    {
        "id": 3,
        "success": true
    }
</li>
</ul>
<h3>POST /movies</h3>
<ul>
    <li>Adds a new movie</li>
    <li>Requires auth permission post:movie</li>
    <li>Request: 

    {
        'title': 'Knives Out ',
        'release_date': '2019'
    }
</li>
    <li>Response:

    {
        "id": 3,
        "success": true
    }
</li>
</ul>
<h3>DELETE /actors/&lt;id&gt;</h3>
<ul>
    <li>Deletes an actor by id</li>
    <li>Requires auth permission delete:actor</li>
    <li>Request: None</li>
    <li>Response:

    {
        "success": true
    }
</li>
</ul>
<h3>DELETE /movies/&lt;id&gt;</h3>
<ul>
    <li>Deletes a movie by id</li>
    <li>Requires auth permission delete:movie</li>
    <li>Request: None</li>
    <li>Response:
        
    {
        "success": true
    }
</li>

