import sys
import re
import os
 
title_search = re.compile(r"""
  (title:\s*) # searches for "title"
  (?P<title>( # named group
    (\S*      # 0 or more non-white spaces
      (\ ?)   # escapes the space in the verbose regex (0 or 1)
      )+      # 1 or more of stated pattern
)
(\n+          # searches for new line (1 or more)
  (\ *))      # looks for 0 or more spaces from the new line
(\S*          # o or more non-white spaces
  (\ ?)       # escapes the space in the verbose regex (0 or 1)
  )+)""", re.IGNORECASE | re.VERBOSE) 

author_search = re.compile(r'(author:)(?P<author>.*)', re.IGNORECASE)
translator_search = re.compile(r'(translator:)(?P<translator>.*)', re.IGNORECASE)
illustrator_search = re.compile(r'(illustrator:)(?P<illustrator>.*)', re.IGNORECASE)

docinfo = dict(title = title_search,
              author = author_search,
              translator = translator_search,
              illustrator = illustrator_search)

def info_search (docinfo, text):
  results = {}
  for k in docinfo:
    result = re.search(docinfo[k], text)
    if result:
      results[k] = result.group(k)
    else:
      results[k] = None
  return results

def kwsrch(kws):
  result = {kw:re.compile(r'\b' + kw + r'\b', re.IGNORECASE) for kw in kws} 
  return result


def file_opener(fl_path):
  with open(fl_path, 'r') as f:   #open the file as f
    return f.read()

def kw_counter(pattern, text):
  matches = re.findall(pattern,text)
  return len(matches)

def path(directory, fl_name):
  return os.path.join(directory, fl_name) #the full path to the file is the directory plus

def doc_tagger(directory, kws):
  for fl in os.listdir(directory):
    if fl.endswith('.txt'):
      fl_path = path (directory, fl)
      text = file_opener (fl_path) 
      info = info_search (docinfo, text)   
      kwsearch = kwsrch (kws)   #if it's a text file

    print "\n\nHere's the info for {}".format(fl) 
    for k in info:
      print "{0} : {1}".format(k.capitalize(), info[k])
    print "\nKeywords searched for:\n"
    for kw in kwsearch:
      print "{0} : {1}".format(kw, kw_counter(kwsearch[kw], text))
    print "****" * 25

def main():
  directory = sys.argv[1]
  kws = [i for i in sys.argv[2:]]
  doc_tagger (directory, kws)

if __name__ == '__main__':
  main()