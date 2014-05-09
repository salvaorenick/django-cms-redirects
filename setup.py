"""Setup for django-cms-redirects."""
from setuptools import setup, find_packages


version = __import__('cms_redirects').__version__

setup(
    name="django-cms-redirects",
    version=version,
    url='http://github.com/salvaorenick/django-cms-redirects',
    license='BSD',
    platforms=['OS Independent'],
    description="",
    author="Andrew Schoen",
    author_email='andrew.schoen@gmail.com',
    packages=find_packages(),
    install_requires=[
        'setuptools',
        'django <1.6',
        'django-cms <3'
    ],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking',
    ],
    package_dir={
        'cms_redirects': 'cms_redirects',
    },
    tests_require=[
        'django-nose'
    ],
    test_suite='django',
    test_loader='run_tests:RunTests'
)
