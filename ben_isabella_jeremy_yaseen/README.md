Blog Nation
===========

## TO RUN
* run `mongod` in one window
* run `./app.py` in another
* run `./utils.py` as a third
* Open localhost:5000 in your web browser

## Members
* Benjamin Attal (Leader)
* Yaseen Islam (Frontend)
* Jeremy Karson (Backend)
* Isabella Siu (Middleware)

## Idea

### Bloginator
* We are implementing the bloginator idea

### Multiple users
* We had the idea of allowing users to have their own blogposts and pages
* There is still only one system administrator to moderate comments and posts

### Tags
* Tags would be useful as a tool to search related blogposts

### Searching
* There will be a search bar to find posts, tags, and comments
* [ElasticSearch] (http://www.elasticsearch.org/)
    * MongoDB lends itself to searching very well, but (as a sort of pet project), I would like to use ElasticSearch on the backend because of its utilities, and its speed
    * Data from MongoDB and ElasticSearch are stored as JSON-like documents, so it will be easy for the ElasticSearch server to index data from MongoDB
    * [Official Python client for ES] (https://github.com/elasticsearch/elasticsearch-py)

## Time table

### By Monday 10/28
* Finish backend design for posts and for users
* Map of html pages we want to create
* Stylistic ideas for the website

### By Monday 11/03
* Implement search
* Implement search by tags
* Creating and deleting users
* Displaying blogposts
* CSS
