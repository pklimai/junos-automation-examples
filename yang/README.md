## YANG Demo

#### To install pyang:

sudo pip install pyang
sudo apt-get install xsltproc
sudo apt-get install libxml2-utils

#### To validate a particular YANG model:

pyang yang-sample.yang 

#### To validate data in XML file against a YANG model:

yang2dsdl -v yang-sample.xml yang-sample.yang

#### To create a sample XML skeleton from a YANG model:

pyang yang-sample.yang -f sample-xml-skeleton
