django-cms-redirects
=================
A django app that lets you store simple redirects in a database and handles the redirecting for you.  Integrated with Django CMS to allow you to link directly to a page object.  Based off django.contrib.redirects.

Dependancies
============

- django
- django-cms

Getting Started
=============

To get started simply install using ``pip``:
::
    pip install django-cms-redirects

Add ``cms_redirects`` to your installed apps and ``syncdb``.

Your installed apps should look something like this:
::
	INSTALLED_APPS = (
	    'django.contrib.auth',
	    'django.contrib.contenttypes',
	    'django.contrib.sessions',
	    'django.contrib.sites',
	    'django.contrib.messages',
	    'django.contrib.admin',
	    'cms',
	    'cms_redirects',
	)

Finally, add 'cms_redirects.middleware.RedirectFallbackMiddleware' to your MIDDLEWARE_CLASSES setting.



