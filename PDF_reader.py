import PyPDF2 as pdf
import re
import unicodedata

__author__ = 'HP'

class pdf_reader:

    def __init__(self):
        self.pdffile = object  # holds pdf file
        self.page = object  # holds each individual page one at a time
        self.morals = object  # holds the split page after being split by moral
        self.morID = object  # holds the moral specification for each comment
        self.outcomes = object  # holds the split page after being split by outcome
        self.outID = object  # holds the outcome ID for each comment
        # self.scores = object  # holds the split page after being split by score
        self.score = object  # holds the score ID for each comment
        self.sits = object
        self.opts = object
        self.comments = object  # holds the split page after being split by comments, situation and option ID
        self.comment = object  # holds the actual mentor comment
        self.entry = object  # holds the entry data to be put in the database
        self.list_of_entries = []  # holds all of the entries
        self.open_pdf('../../Desktop/Spring 2015/BIT 197 BUSTED/MC_Situationsbusted.pdf')
        self.get_comments()

    def open_pdf(self, p_filename):
        self.pdffile = pdf.PdfFileReader(p_filename)

    def get_comments(self):
        idx = 0
        while idx < self.pdffile.numPages:
            self.fix_page(idx)
            self.sits = re.split('Situation ID\s*[0-9]{2,3}\s*', self.page)
            for s in self.sits:
                self.opts = re.split('Option ID\s*[0-9]{2,3}\s*', s)
                for p in self.opts:
                    self.morals = re.split('Moral\s*', p)
                    for m in self.morals:
                        self.morID = re.findall('(Negative)|(Neutral)|(Positive)', m)
                        if self.morID:
                            for y in self.morID:
                                for x in y:
                                    if x == 'Negative':
                                        self.morID = -1
                                    elif x == 'Neutral':
                                        self.morID = 0
                                    elif x == 'Positive':
                                        self.morID = 1
                                    else:
                                        continue
                                    self.outcomes = re.split('Outcome ID\s*', m)
                                    for o in self.outcomes:
                                        self.outID = re.findall('^[0-9]{2,3}', o)
                                        if self.outID:
                                            self.outID = self.outID[0]
                                            self.outID = int(self.outID)
                                            self.score = re.findall('Score\s*-?[0-9]', o)
                                            if self.score:
                                                self.score = re.findall('-?[0-9]', self.score[0])
                                                self.score = self.score[0]
                                                self.score = int(self.score)
                                                if self.score <= 0:
                                                    self.score = 0
                                                else:
                                                    self.score = 1
                                                self.comments = re.findall('Mentor Comments .*', o)
                                                if self.comments:
                                                    for c in self.comments:
                                                            self.comment = re.split('Mentor Comments\s*', o)
                                                            for mc in self.comment:
                                                                if mc != '' and not re.search('[0-9]{2,3}', mc):
                                                                    self.comment = mc
                                                                    self.make_entry()
            idx += 1

    def make_entry(self):
        self.entry = (0, self.outID, 0, self.morID, self.score, self.comment, 'fill')
        self.list_of_entries.append(self.entry)

    def print_entries(self):
        for entry in self.list_of_entries:
            print entry

    def fix_page(self, num):
        self.page = self.pdffile.getPage(num).extractText()
        self.page = self.page.replace(u'\2122', u"'")  # replaces tm character with the apostrophe.
        self.page = self.page.encode('ascii', 'ignore')  # encodes to regular string from unicode