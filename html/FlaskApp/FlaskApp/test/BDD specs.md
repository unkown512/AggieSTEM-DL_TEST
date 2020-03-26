# behavior test

## feature 1: signup
### scenario 1: sad path, sign up fail
* should stay in /signup page
* should have certain error flash message

###  scenario 2: happy path, sign up success
* should be redirected to /signin page

## feature 2: signin
### scenario 1: sad path, login error
* should stay in /signin page
* should have certain error flash message
### scenario 2: happy path, login 
* should be redirected to /dashboard page
* should have matching username displayed in /dashboard page

## feature 3: navigation
* after login, should be able to navigate to /user_profile page
### scenario 1: happy path, navigation success
* should check for certain elements in the page
### scenario 2: sad path, navigation fail
* not expected, unless user is not logged in.

## feature 4: keyword query
* search for dataset with matching name in /user_profile page
### scenario 1: default behavior
* /user_profile page should display granted dataset in certain style
### scenario 2: happy path, search success
* search with keyword 'MNIST', page should display corresponding dataset row with matched style.
### scenario 3: sad path, search fail
* search with keyword 'nonsense', should expect no row changes style from default behavior
