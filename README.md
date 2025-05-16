# DFIR ORC Project Documentation

This is the source for the content hosted at [dfir-orc.github.io](https://dfir-orc.github.io).

The documentation is built with [Sphinx](https://www.sphinx-doc.org).

## Installation

To install an environment in which you can build the doc (works on Windows and Linux):

    pip install sphinx
    pip install solar-theme
    git clone git@github.com:DFIR-ORC/dfir-orc-doc-src.git
    cd dfir-orc-doc-src/docs
    make html

## Tips on Sphinx


  - CSV tables should use the following attributes for a better rendering 

```
.. csv-table::
    :header: Value, Description
    :align: left
    :widths: auto
    
    Value 1, Description 1.
    Value 2, Description 2.
```  
  
## Guidelines for Style/Text Formatting

### Uppercase

The first letter of every word in a title should be in uppercase, except for:
  - Conjunctions, prepositions and articles which are less than three letters.
  - In the case of a compound word, only the first word should have an uppercase.

In addition, file types (i.e: "a CSV file") and cryptographic hashes (SHA1, MD5) should be entirely in uppercase.

### Usage Convention for Double Backquotation Marks

Double backquotes are used instead of simple backquotes in order not to have to worry about escaping '\' and such.

Double backquotes should be used for:
  - filenames,
  - filepaths,
  - volume names,
  - ressource names,
  - binary options (i.e. ``/key``)
  - possible values for an attribute (i.e. ``None``, ``Fastest``).
  
Double backquotes should **not** be used for:
  - tool names (i.e. NTFSInfo, FastFind but also DFIR ORC)

### Internal links

First of all: [Cross-referencing arbitrary locations in Sphinx](http://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html#ref-role).

  - As tags have a project-wide scope, tag names should be namespaced with the title of the page to avoid conflicts.

### Miscellaneous

  - Words which have to be replaced by user defined values should be enclosed between angled brackets ('<>') and in CamelCase:
    ``` /out=<OutputFolder>```

## General rules for writing a new page

When possible (and for the documentation of a tool in general), please use the following structure:
   - Description: describe what the tool is and what it can be used for.
   - Output: describe the different output file(s), including the columns for CSV files.
   - Usage: start with an input example (command-line or file) and then explain each element and/or option in a section.
  Example :
  
```
 ``ntfs_find`` or ``ntfs_exclude`` Element
-----------------------------------------

*optional=no, default=N/A*

Used to specify a set of rules which matches the hive in each previously specified location. For details on the ``<ntfs_find>`` element syntax, please refer to the :doc:`ntfs_find documentation <configuring_ntfs_opt>`.
```
