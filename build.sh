#Exit when error
set -o errexit

#Install used libary
pip install -r requirements.txt

#Convert static asset file
python manage.py collectstatic --no-input

#Apply database migration
python manage.py migrate