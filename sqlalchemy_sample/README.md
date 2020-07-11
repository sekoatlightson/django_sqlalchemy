
conda create -n django2.1
conda activate django2.1
conda install -c anaconda django==2.1.5
conda install -c anaconda sqlalchemy

django-admin startproject project
ディレクトの中に入って
python manage.py startapp rental
