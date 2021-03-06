# Makefile for TimeStamper
#
# (c) Copyright 2013 Juha Autero. All Rights Reserved. 
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

VIRTUALENV_VERSION := 1.10
VIRTUALENV_TAR := virtualenv-$(VIRTUALENV_VERSION).tar.gz
VIRTUALENV_BASEURL := https://pypi.python.org/packages/source/v/virtualenv
APACHELOG := testenv/lib/python2.7/site-packages/apachelog.py
PIPLOGFILE := pip.log

all: test

virtualenv: virtualenv-$(VIRTUALENV_VERSION)
	-rm $@
	ln -s $< $@

virtualenv-$(VIRTUALENV_VERSION):
	curl -O $(VIRTUALENV_BASEURL)/$(VIRTUALENV_TAR)
	tar xvzf $(VIRTUALENV_TAR)
	-rm $(VIRTUALENV_TAR)

.PHONY: virtualenv-clean
	
virtualenv-clean:
	-rm virtualenv $(VIRTUALENV_TAR)
	-rm -rf virtualenv-$(VIRTUALENV_VERSION)

testenv: virtualenv
	python virtualenv/virtualenv.py testenv

testenv/bin/nosetests: testenv
	testenv/bin/pip install nose --log $(PIPLOGFILE)
	
$(APACHELOG): testenv
	testenv/bin/pip install apachelog --log $(PIPLOGFILE)

.PHONY: testenv-clean dist-clean clean

clean:
	-rm nosetests.xml
	
testenv-clean:
	-rm -rf testenv
	
dist-clean: virtualenv-clean testenv-clean clean

nosetests.xml: testenv/bin/nosetests $(APACHELOG) src/*.py
	testenv/bin/nosetests --with-xunit src/

test: nosetests.xml
