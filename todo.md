fix volume data. this tx didnt work - 0x7352c5d6746061c02564a23c2a3c1a754e044643cb6a2f7b412e867514e6fe1e

docker build works.
docker run with env variables and confirm that it works.

fix for env variables

docker run -e ENV1=XXX ENV2=XXX <image_name>

env variables exported but not viewable by cron so cron needs to export them manually

to do this, do setup.sh file on docker run which does the following:-
- creates .env file in app directory