#!/bin/bash

testres_funct(){
    TIMESTAMP=$(head -n 1 build.x86_64-co7-gcc48-o2g/Testing/TAG)
    pygmentize build.x86_64-co7-gcc48-o2g/Testing/$TIMESTAMP/Test.xml
}

alias testres=testres_funct
