# Movie Recommended System

This project was built using 
- HTML 
- CSS 
- Python 
- Flask (micro web framework) 
- Flask SQLAlchemy (Flask extension for managing database) 
  HTML file.
- Sqlite database.


The movie recommender app recommend movies based on KNN algorithm. In general, K-nearest neighbors (KNN) is a type of supervised learning algorithm used for both regression and classification. KNN tries to predict the correct class for the test data by calculating the distance between the test data and all the training points. Then select the K number of points which is closest to the test data. The KNN algorithm calculates the probability of the test data belonging to the classes of 'K' training data and the class that holds the highest probability will be selected. In the case of regression, the value is the mean of the 'K' selected training points.

<br /><br />
### To view this project

Go to https://wenjiemovierecommender.herokuapp.com/

### How to use this Project
Download the files using the git clone command.
```
$ git clone <link to project>
```
Create your virtual environment
```
$ python3 -m venv env
$ source env/bin/activate
```
I created the requirements.txt file using the pip freeze command.
Install all dependencies from the requirements.txt file.
```
$ pip install -r requirements.txt
```
Run the app.py file
```
$ python3 main.py
```
Type in http://localhost:5555 into your browser to view the project live.



