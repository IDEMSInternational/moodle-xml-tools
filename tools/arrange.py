from category import QuestionCollection, Question, Category
import argparse
import csv


def main():
    description = 'Arrange questions from an input question bank into categories, as specified in a spreadsheet.\n\n'\
                  'Example usage: \n'\
                  'arrange.py tests/input/example1/content_index.csv --output=out.json --format=csv --datamodels=tests.input.example1.nestedmodel'
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('inputcsv', help='Input spreadsheet assigning categories to questions.')
    parser.add_argument('inxml', help='Input Moodle XML question bank filename')
    parser.add_argument('outxml', help='Output Moodle XML question bank filename')
    parser.add_argument('--categorycolumn', default='Category', help='Title of the column in inputcsv containing the categories')
    parser.add_argument('--titlecolumn', default='Question Title', help='Title of the column in inputcsv containing the question titles')
    args = parser.parse_args()

    categorycolumn = args.categorycolumn
    inputcsv = args.inputcsv
    inxml = args.inxml
    outxml = args.outxml
    titlecolumn = args.titlecolumn

    qc = QuestionCollection.from_questionbank_file(inxml)
    qc_new = QuestionCollection()

    with open(inputcsv, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        if categorycolumn not in reader.fieldnames:
            print(f'Error: {categorycolumn} is not a header in {inputcsv}')
            exit(1)
        if titlecolumn not in reader.fieldnames:
            print(f'Error: {titlecolumn} is not a header in {inputcsv}')
            exit(1)
        for i, row in enumerate(reader):
            qname = row[titlecolumn]
            catname = row[categorycolumn]
            if not catname:
                continue
            question = qc.get_question(qname)
            if question is not None:
                qc_new.add_question(question, catname)
            else:
                print(f'Row {i+2}: {qname} is not in question bank.')

    qc_new.to_file(outxml)

if __name__ == '__main__':
    main()