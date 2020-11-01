# google-keep-clone<br />
Tech Stack - Python, Django REST, JavaScript, HTML, Bootstrap. <br />
Custom user model has been used, where user can login/signup using email and password rather than username. <br />
Authentication is checked for every api. If the user is not logged in, then none of the view functions are accessible. <br />
A user cannot add/edit/delete a note belonging to another user! <br />
Each note has a foreign key which references the user id. <br /> 
A user can only access those notes whose foreign key is equal to the current user id.
