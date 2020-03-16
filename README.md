# User Story Evaluation
#### Implemented using Django
Models are implemented using Django's ORM

###### Brief Description
This app has been designed as a REST service accepts JSON input and responds with JSON

There are two user_types considered here - 'user' and 'admin'

There is no login / token mechanism implemented to keep track of which user is accessing the endpoints - instead a primitive approach is used - `user= <username>` is passed as a query parameter to the all requests.

Note:
- `user=<username>` is a mandatory query parameter for all requests

##### 1. The following endpoints are exposed for users

1.1. `GET /stories/?user=<username>` 
    - returns list of all stories (for admin)
    - returns list of all stories created by user (for regular user)
    - `status=<status>` is an optional parameter to filter stories by status

1.2. `[GET|PUT] /stories/<id>?user=<username>`
    - users can query/edit stories that are created by them
    - admins may query/edit any story
    - for `PUT` requests,in the body of the request
      it is sufficient to pass parameters 
      of the story that require to be updated

1.3. `POST /stories/?user=<username>`
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

1.4. `PUT /stories/<id>/submit?user=<username>`
    - users can submit stories created by them for admin approval

1.5. `PUT /stories/<id>/approve?user=<username>`

1.6. `PUT /stories/<id>/reject?user=<username>`

   - admin users can approve/reject any items that are submitted for approval

##### 2. State transitions for user stories
When a user story is created, it is created with `status='DRAFT`

The following transitions are allowed for user stories:
- DRAFT -> FOR REVIEW (on submission by creator)
- FOR REVIEW -> APPROVED (on approval by admin)
- FOR REVIEW -> REJECTED (on rejection by admin)
- APPROVED -> DRAFT (if user/admin updates approved story)
- REJECTED -> DRAFT (if user/admin updates rejected story)
     

###### Setup
Requirements
1. django
2. django-rest-framework


