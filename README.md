

## arrange

Arrange questions into a categories.

Takes an input spreadsheet mapping question titles to categories, as well as an input Moodle XML with the questions, and produces a Moodle XML with the questions referred to in the spreadsheet sorted into their respective categories.

The column titles in the spreadsheet for the columns containing the question titles (default: 'Question Title') and category names (default: 'Category') can be specified as arguments. Each row of the input spreadsheet is processed by looking up the question referred to in the 'Question Title' column in the input question bank XML file.
If no question with matching name is found, a warning is issued. If multiple questions have the same name, a warning is issue and it is undetermined which of the questions is picked. The question is then sorted into the category specified in the category column.

The character `/` is used to indicate subcategories, for example `My Cat/My Subcat`.
If the category entry is empty, the question is omitted from the output.

Usage:

```
usage: arrange.py [-h] [--categorycolumn [CATEGORYCOLUMN]]
                  [--titlecolumn [TITLECOLUMN]]
                  inputcsv inxml outxml
```

Example:

`arrange.py categories.csv questionbank.xml out.xml --categorycolumn "Course 1"`