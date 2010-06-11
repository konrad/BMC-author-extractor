"""
FUNCTION: Extracts journal and author information from a BMC article
          XML files and prints them to the standard output.

USAGE: bmc_author_extractor.py <BMC_ARTICLE_XML_FILE>

e.g. bmc_author_extractor.py 1471-2180-10-137.xml

To apply this script to all articles of BMC at once do the following:

* Download the zipped article:
  "wget -c --user=datamining --password='$8Xguppy' ftp://ftp.biomedcentral.com/articles.zip"
  Check out http://www.biomedcentral.com/info/about/datamining/ for further details
* Unzip the file
  "unzip articles.zip"
* Use find to apply the script on every article file
  "find BMC_FTP/ -name "*xml" -exec python bmc_author_extractor.py {} \; > author_info.txt"

Copyright (c) 2010, Konrad Foerstner <konrad@foerstner.org>

Permission to use, copy, modify, and/or distribute this software for
any purpose with or without fee is hereby granted, provided that the
above copyright notice and this permission notice appear in all
copies.

THE SOFTWARE IS PROVIDED 'AS IS' AND THE AUTHOR DISCLAIMS ALL
WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE
AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL
DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR
PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.
"""
__author__ = "Konrad Foerstner <konrad@foerstner.org>"
__copyright__ = "2010 by Konrad Foerstner <konrad@foerstner.org>"
__license__ = "ISC license"

import sys
from BeautifulSoup import BeautifulStoneSoup

def main():
    if not len(sys.argv) == 2:
        print __doc__
        sys.exit(2)
    bmc_author_extractor = BMCAuthorExtractor(sys.argv[1])
    bmc_author_extractor.generate_output()

class BMCAuthorExtractor(object):

    def __init__(self, file_name):
        self.soup = BeautifulStoneSoup(open(file_name).read())

    def journal(self):
        self.journal = self.soup.art.source.string

    def authors(self):
        try:
            self.authors = [
                {'surname' : author.snm.string,
                 'firstname' : author.fnm.string,
                 'middle_name' : self._middle_name(author),
                 'institute_id' : author.insr['iid']}
                for author in self.soup.art.aug.findAll('au')]
        except:
            sys.stderr.write("No author information in file %s\n" % (sys.argv[1]))
            sys.exit(2)

    def _middle_name(self, author):
        try:
            return author.mi.string
        except AttributeError:
            return ''

    def institutes(self):
        self.institutes = {}
        for intitute in self.soup.art.insg.findAll('ins'):
            self.institutes[intitute['id']] = intitute.p.string
    
    def generate_output(self):
        self.journal()
        self.authors()
        self.institutes()
        for author in self.authors:
            try:
                institute = self.institutes[author['institute_id']]
            except:
                institute = ''
            print "%s\t%s\t%s\t%s\t%s\t%s" % (
                self.journal, author['firstname'], author['middle_name'],
                author['surname'], institute, sys.argv[1].split('/')[-1])
    
if __name__ == '__main__': main()
