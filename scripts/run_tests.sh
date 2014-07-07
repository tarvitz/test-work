#!/bin/bash
GAE_LIB_ROOT=../google_appengine
nosetests --with-gae --without-sandbox --gae-lib-root=$GAE_LIB_ROOT --nologcapture $@
