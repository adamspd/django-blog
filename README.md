# django-blog
A package that helps integrate a django blog in your website project

Before launching the project, make sure to create migrations and run them. Otherwise, the new changes won't take effect 
and you will have a bunch of errors.

New changes include :
    Added 'django.contrib.sites', to settings

After finishing the migrations go to "/admin" of your site, in the sites section, change "example.com" to your site's
url. Always modify, never add a new one, otherwise, it will break.