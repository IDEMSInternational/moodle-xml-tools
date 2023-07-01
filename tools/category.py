import copy
import lxml.etree as etree
from collections import defaultdict

class Category:
    '''A category may contain subcategories and questions'''

    def from_xml(xml_element):
        '''The XML element excludes questions/subcategories'''
        # TODO: Validation
        return Category(xml_element=copy.deepcopy(xml_element))

    def __init__(self, name=None, description='', id=None, xml_element=None):
        self.questions = []
        self.subcategories = []
        if xml_element is not None:
            self.root = xml_element
        elif name is not None:
            self.root = etree.Element("question", type="category")
            category = etree.SubElement(self.root, "category")
            categorytext = etree.SubElement(category, "text")
            categorytext.text = name
            info = etree.SubElement(self.root, "info", format="html")
            infotext = etree.SubElement(info, "text")
            infotext.text = description
            idnumber = etree.SubElement(self.root, "idnumber")
            idnumber.text = id if id is not None else ''
        else:
            raise ValueError("Either an xml_element or a name have to be provided")
# <!-- question: 0  -->
#   <question type="category">
#     <category>
#       <text>top/Default for Linear Algebra II- Maseno University/WeeK 2 Quizzes: Overview of linear dependence and basis of a vector space</text>
#     </category>
#     <info format="html">
#       <text></text>
#     </info>
#     <idnumber></idnumber>
#   </question>

    def name(self):
        return self.root.find('category').find('text').text

    def add_question(self, question):
        self.questions.append(question)

    def add_subcategory(self, category):
        self.subcategories.append(category)

    def to_xml(self):
        return self.root

    def add_children_to_xml(self, root):
        '''Adds everything in this category (including itself) to the
        XML element that is passed to this method.
        '''
        root.append(self.to_xml())
        for question in self.questions:
            root.append(question.to_xml())
        for category in self.subcategories:
            category.add_children_to_xml(root)


class Question:
    def from_xml(xml_element):
        return Question(copy.deepcopy(xml_element))

    def __init__(self, xml_element):
        # TODO: Validation
        self.root = xml_element

    def name(self):
        return self.root.find('name').find('text').text

    def to_xml(self):
        return self.root


class QuestionCollection(Category):
    '''A collection of questions sorted into categories'''

    def from_questionbank_file(filename):
        parser = etree.XMLParser(strip_cdata=False)
        tree = etree.parse(filename, parser)
        root = tree.getroot()
        return QuestionCollection.from_questionbank_xml(root)

    def from_questionbank_xml(xml_element):
        # TODO: Process and validate the xml
        qc = QuestionCollection()
        questions = xml_element.findall(".//question")
        current_category = None
        for question in questions:
            if question.get("type") == "category":
                current_category = Category.from_xml(question)
                qc.add_category(current_category)
            else:
                qc.add_question(Question.from_xml(question), current_category.name())
        return qc

    def __init__(self):
        # top-level questions only
        self.questions = []
        # top-level categories only
        self.categories = []
        # the lookup contains all categories
        self.category_lookup = {}
        self.question_lookup = {}

    def add_question(self, question, category_name=None):
        if category_name is None:
            self.questions.append(question.xml())
        if category_name not in self.category_lookup:
            self.add_new_category(category_name)
        self.category_lookup[category_name].add_question(question)
        if question.name() in self.question_lookup:
            print(f'Warning: Multiple questions with title "{question.name()}"')
        self.question_lookup[question.name()] = question

    def add_category(self, category):
        '''Cateory is a Category object here'''
        split = category.name().rsplit('/', 1)
        if len(split) == 1:
            parent, child = '', split[0]
        else:
            parent, child = split
        if parent in self.category_lookup:
            parent_cat = self.category_lookup[parent]
            parent_cat.add_subcategory(category)
        else:
            self.categories.append(category)
        self.category_lookup[category.name()] = category

    def add_new_category(self, category_name):
        category = Category(category_name)
        self.add_category(category)

    def get_question(self, name):
        return self.question_lookup.get(name)

    def to_file(self, filename):
        root = etree.Element("quiz")
        for question in self.questions:
            root.append(question.to_xml())
        for category in self.categories:
            category.add_children_to_xml(root)
        with open(filename, 'wb') as f:
            # f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write(etree.tostring(root, pretty_print=True, encoding='UTF-8', xml_declaration=True))

    def apply_for_all_questions(self, function):
        pass


if __name__ == "__main__":
    c = Category('wurst')
    bb = etree.tostring(c.to_xml(), pretty_print=True)
    print(bb.decode(encoding='utf-8', errors='strict'))

    filename = "la.xml"
    parser = etree.XMLParser(strip_cdata=False)
    tree = etree.parse(filename, parser)
    root = tree.getroot()
    qc = QuestionCollection.from_questionbank_xml(root)
    qc.to_file("out.xml")
