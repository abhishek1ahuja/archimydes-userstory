# User Story Evaluation
#### Implemented using Django
Models are implemented using Django's ORM

### Brief Description
- This app has been designed as a REST service accepts JSON input and responds with JSON
- There are two user_types considered here - 'user' and 'admin'
- There is no login / token mechanism implemented to keep track of which user is accessing the endpoints - instead a primitive approach is used - `user=<username>` is passed as a query parameter to the all requests.

****

### API Specification
**For creating and editing users, the following endpoints are available**
- `POST /users`
    - for creating users
    - sample request body to pass to this request

            {
            "username":"boss",
            "name":"admin",
            "user_type":"admin"
            }
        
    - `user_type` may have values `user` or `admin` 
- `GET /users`
    - for getting list of all users
- `GET|PUT|DELETE /users/<user_id>`
    - for viewing, editing, deleting a user

**Note**:
- `user=<username>` is a mandatory query parameter for all requests below which query and manipulate stories

1. The following endpoints are exposed for users

    1. `GET /stories?user=<username>` 
        - returns list of all stories (for admin)
        - returns list of all stories created by user (for regular user)
        - `status=<status>` is an optional parameter to filter stories by status

    2. `[GET|PUT] /stories/<id>?user=<username>`
        - users can query/edit stories that are created by them
        - admins may query/edit any story
        - for `PUT` requests,in the body of the request
          it is sufficient to pass parameters 
             of the story that require to be updated

    3. `POST /stories?user=<username>`
         - body of post request expects to have a story object 
    with the following parameters as shown in this example 
        ```
        example
        { 
            "summary": "example story",
            "description": "this is a sample user story",
            "story_type": "code review",
            "complexity": "3",
            "estimated_time": "20:00:00",
            "cost": "18"  
        }
        ```
    4. `PUT /stories/<id>/submit?user=<username>`
        - users can submit stories created by them for admin approval
    5. `PUT /stories/<id>/approve?user=<username>`
    6. `PUT /stories/<id>/reject?user=<username>`
        - admin users can approve/reject any items that are submitted for approval

2. State transitions for user stories
- When a user story is created, it is created with `status='DRAFT'`
- The following transitions are allowed for user stories:
    - DRAFT -> FOR REVIEW (on submission by creator)
    - FOR REVIEW -> APPROVED (on approval by admin)
    - FOR REVIEW -> REJECTED (on rejection by admin)
    - APPROVED -> DRAFT (if user/admin updates approved story)
    - REJECTED -> DRAFT (if user/admin updates rejected story)
     
****

### Setup
**Requirements**
1. django
2. django-rest-framework
3. git

**Instructions to clone project and run:**

1. use `pip` to install `django` and `django-rest-framework`
    1. `pip install django`
    2. `pip install django-rest-framework`
2. clone the userstory project and checkout the `dev` branch
    1. `git clone https://github.com/abhishek1ahuja/archimydes-userstory.git`
    2. `git checkout dev`
3. run django migration to create required database tables
    1. `python3 manage.py migrate`
4. To run the app server
    1. `python3 manage.py runserver`
5. To run all tests
    1. `python3 manage.py test userstory`
    


