Test-work
=========

.. contents:: :local:
    :depth: 2

Backend зависимости
-------------------

* python 2.7.x
* virtualenv
* google app engine (1.9.x)
* flask
* wtforms

Установка зависимостей
~~~~~~~~~~~~~~~~~~~~~~

Backend зависимости
```````````````````
Python все python зависимости расположены в `requirements/base.txt` и могут быть установлены с
помощью `pip`

Frontend зависимости
````````````````````
Опциональны, устанавливаются через bower (требуется nodejs 0.10.x+)

.. code-block:: bash

    user@localhost ~$ sudo npm install -g bower
    user@localhost atm$ bower install

Тесты
-----

Для запуска тестов необходимо выполнить

.. code-block:: bash

    user@localhost amt$ python tests.py <расположение google_appengine> application.tests

DEMO
````
Демонстрационный сайт можно найти по `ссылке<http://test-work-amt.appspot.com/>`_
