# DiskusForums
A Minimal Forums Django App

See it Live here : http://diskusforums.herokuapp.com/

#### Things Done:

* Login/Register/Forgot Password
* Profile Page and Edit
* Categories
* Threads
* Posts
* Awesome WYSIWYG Editor using SummerNote.js(https://github.com/summernote/summernote/)

#### Things Pending (Can be done by django admin panel, but not on Front End) : 

* Add Avatar Image to Profile during Registration and Profile View
* New Category(admin only)
* Report Post
* Delete Thread
* Lock Thread
* Pin Thread
* Profile Page (View All posts and Threads, currently only top 5 are shown)

#### Improvements:

* Permalink ( For now, it just takes you to the thread page number on which the post is and doesn't scroll to the post)
* Moderator,Super Admin management

#### Bugs:

* Post made by a user(not moderator and not super admin) is not editable in future
* If a post is quoted in another and if quoted post gets deleted it still stays in latter.(i.e. There is no post quote tracking) 
* No hard deletion allowed yet

#### Features to add:

* Search
* Messages
* Private Messages/Threads
* reCaptcha
* Like a Post

#### Note:

* All Images are uploaded to ultraimg.com as heroku gives me no server space :|