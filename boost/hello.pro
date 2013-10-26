INCLUDEPATH += /usr/include/python2.7/ \
    /usr/include/ \

LIBS += -L/user/lib/ -lboost_python -L/usr/lib/python2.7/config -lpython2.7

HEADERS +=

SOURCES += \
    hello.cpp

TEMPLATE = lib
TARGET = hello
DESTDIR = ./

CONFIG += debug

QT -= gui
QT -= core

OTHER_FILES += 
