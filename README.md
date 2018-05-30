# Observable Collections
A Rx based collections implementation in Python

[![Build Status](https://travis-ci.org/shyam-s00/ObservableCollections.svg?branch=master)](https://travis-ci.org/shyam-s00/ObservableCollections)
[![Coveralls github](https://coveralls.io/repos/github/shyam-s00/ObservableCollections/badge.svg)](https://coveralls.io/github/shyam-s00/ObservableCollections?branch=master)

It contains following Observable collections and internally depends on [RxPy](https://github.com/ReactiveX/RxPY)

    * ObservableList
    * ObservableDict
    * ObservableSet

These collections expose ```when_collection_changes()``` method that creates an Observable which can be subscribed. 

Any changes to the ```ObservableList / ObservableSet / ObservableDict``` that modifies the collection, publishes the event either via on_next or error via on_error

**Installation**

#####*Requires Python 3.5+*

```commandline
pip install observable-collections
```

**Example**

```python
from reactive.ObservableList import ObservableList

ol = ObservableList([1, 2, 3, 4])
ol.when_collection_changes() \
    .map(lambda x: x.Items) \
    .subscribe(print, print)

ol.append(5)

```
