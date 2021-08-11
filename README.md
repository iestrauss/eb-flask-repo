# README #

This README would normally document whatever steps are necessary to get your application up and running.

### Fakenews Extension ###
* Quick summary
Drives reviews and reviewers.
* Version
0.0.1
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### Development Tasks ###
-- Last updated: 09/29/2019

1. Ilana: link to results and vote page from home page ASAP
1. Ilana go to home from any page ASAP

1. Jim: ~~provide comments to results page articlevote.query all ish~~ 09/29
1. Ilana: loop comments in results page articlevote.query all ish

1. Ilana cleaning up CSS
1. Jim: ~~clean up vote choice~~ 09/26
1. Jim: ~~make vote summary more efficient~~ 09/26
1. Jim: ~~eliminate errors when articles have zero votes~~ 09/26
1. Jim: ~~make sure articles only inserted once~~ 09/27
1. Jim: ~~make sure users only vote once~~ 09/27
1. Ilana to design admin process - learn how wikipedia actually work

### Branch managment convention ###
* To list local and remote branchs
    * git branch
    * git branch -r
* When undergoing a development effort create a new branch to modify and test
    * Select a new new_branch_name
        * For normal developmnet I might use "hobmij_working"
        * For a bug fix the name might be specfic e.g. "fix_user_permission_bug"
    * To create a new branch
        * git checkout -b [new_branch_name]
    * To commit your changes to your local repository
        * git commit -a -m 'description of changes'
    * To push changes to remote repository
        * git push
    * To merge: set back to master branch, and merge
        * git checkout master
        * git merge [new_branch_name]
    * You may optionally delete your branch after you're satisfied with the merged code
        * git branch -d [new_branch_name]

### How do I get set up? ###

* Summary of set up
* Configuration
* Dependencies
+ Database configuration
    * python db_create_tables.py
    * python db_insert_data.py
+ How to run tests
    * python3 fakenews.py
    * localhost:5000/enterdata
* Deployment instructions
    * > rm /usr/local/var/apehouse.db
    * > python db_create_table.py
    * > python db_inser_data.py

# eb-flask-repo
