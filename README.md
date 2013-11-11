TimeStamper
===========

Tool to creating and processing timestamp logs.

Development environment
-----------------------

TimeStamper is developed under virtualenv. That way it can use Python packages that are not necessarily installed on development machine. This need rose from the fact that python (2.7 on OS X) does not come with tools to generate JUnit like xml files from unit test results. 

Makefile has rules to fetch VIRTUALENV from pypi and use it locally to create testenv environment where all tests are run. 