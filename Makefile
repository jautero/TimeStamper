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

virtualenv: virtualenv-$(VIRTUALENV_VERSION)
	-rm $@
	ln -s $< $@

virtualenv-$(VIRTUALENV_VERSION):
	curl -O $(VIRTUALENV_BASEURL)/$(VIRTUALENV_TAR)
	tar xvzf $(VIRTUALENV_TAR)
	-rm $(VIRTUALENV_TAR)

dist-clean:
	-rm virtualenv $(VIRTUALENV_TAR)
	-rm -rf virtualenv-$(VIRTUALENV_VERSION)

testenv: virtualenv
	python virtualenv/virtualenv.py testenv
