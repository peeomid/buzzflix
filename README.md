# Buzzflix
This is developed using Django as a very simple backend APIs.

## Setup
- Clone the repo.
- [optional] You can create a virtual environment of your choice, activate it and install required packages
```
$ cd path/to/this/
$ pip install -r requirements.txt
```

This comes with a sqlite database pre-populated with sample data (thousands of movies and tracking), so you can start the server by:

```
./manage.py runserver
```

Then you can access the server at default port 8000. When you navigate to each API below, there will be browsable UI to try them out, for example
`http://localhost:8000/api/movies/`.

There's also an admin UI to check the data at `http://localhost:8000/admin`. Default username and password are admin/abc12345.

## Movie List API

There are 2 APIs for this part:

1. `/api/home/`: is the one requested. This is the API to call for home screen, used to show one highlighted movie and all movie categories.
	+ Highlighted movie is marked as `is_highlighted` field in movie model. In case of multiple movies being marked as highlighted, the highlighted one is selected based on date, so it's consistent during the day and identical between users.
	+ Each category show only show movies that has `display_on_home` as True. This is a toggle field being added to the model to determine which one to show on home screen for that category. 
	This is rather simple logic, like `is_highlighted`, and should be more sophisticated in production. The reason for this, is that we can't show all movies on home screen but just a few for each category. For more movies of a given category (as users go into that category to browse), frontend should call the movie list API below.
	
2. `/api/movies/`: This is one additional API to call to get movies of a given category. The call should be `/api/movies/?category=70`, where `70` is category id.

## Analytics API
 This is desired to track logged in users
 
 There're 2 APIs for this part as well:
 
 1. `/api/track/`: this is the API frontend should call to track users' activities.
	 - This is `POST` call only.
	 - Value should be passed in request body, with following parameters:
		 +  `event_name` [required]: name of the event. Some predefined event name are below. Frontend can send additional custom event as well.
			 + `MOVIE_VIEW`: user open movie details
			 + `MOVIE_START`: start watching session
			 + `MOVIE_END`: end a watching session, with value of timestamp at which the movie stops
			 + `MOVIE_FINISH`: a movie is watched till the end
		 + `movie` [optional]: id of the movie to track
		 + `value` [optional]: value to measure. For example, `MOVIE_END` event can be sent with `value` of the timestamp of the movie at which user stop watching.
		 + `metadata` [optional]: additional json data if needed
2. `/api/analytics`: this is the API that return sample reports for analytics. Right now there're 2 sample reports as examples in requirements.
	- `/api/analytics/?report=top_view`: Top 50 most viewed movie in the last 7 days.
	- `/api/analytics/?report=top_aband`: 50 most abandoned movies in the last 7 days.


## Ideas to determine personalised highlighted movies for each user


- The very first step is to log all user's view history. A few pieces of information that we should care about:
	+ The genre of movies. 
	+ Time of the day
	+ Day of week
	+ Whether users watch the whole movie, or go half way through. Do they often go back to those half-way through movies to finish them.
	+ Devices users watch the movie on, whether it's on their phones, tablets, computers or TVs

- Then base on that history, we can do 2 broad things:
	+ Normal habit of many people, to determine common pattern among them. This might include people who watch film A, normally will watch film B. Or people will normally watch certain film at certain time of the day, day of week, or some near some events during the year.
	+ Personalised pattern for every single individual. Say person A generally watches short movies on mobile phone, while watching longer movies on TV.

- Then each criteria is given a weight to determine to recommended movies.

- Some ideas:
	+ Show movies of the same genres that user normally watch
	+ Show movies that people with similar habit will normally watch together with movies current user watched.
	+ Show movies that people in the same area are watching a lot.
	+ Show movies that people normally watch during the time of the year, say during Christmas, show more Christmas movies.
	+ Show movies of actors/actresses that users normally watch, especially newly released
	+ Show the genres of movies that users normally watch during that time of day/day of week. For example, the family might share the same account on the TV in living room. During dinner time, it's normally family related movies, but late at night, it can be more parent favourite movies.
	+ Do not show movies the user watch half way through but never finish. This can be a pattern across users, so similar movies are discouraged to show as well. There should be a session for people to continue watching these though, since they might be busy half-way through
	+ Show less of movies that the user checked movie info and probably watched trailer but never watch. Find pattern and limit showing movies of the same types/pattern.



