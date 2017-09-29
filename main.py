import re

# OPTIONS
histogram_height = 60; # makes the character arc taller and more spread.

properNouns = {};
endQuote = 0;
def quoterepl(matchobj):
    global endQuote;
    if endQuote == 1:
        endQuote = 0;
        return "</quote>";
    else:
        endQuote = 1;
        return "<quote>";

def isImportant(name):
    return not (name in "Twelve The But And You What She There They Her This How Well Then His For Why God Lady Not Had One That Thus Now When After Perhaps Come Since Please Does Can Old Yes Nowadays");

def sortMe(x):
    return len(x[1]);

def sortMeToo(x):
    return x[1];

def numInRange(arr, i, j):
    arr2 = list(arr);
    arr2 = [x for x in arr2 if x > i and x < j];
    # print arr2;
    return len(arr2)

with open('Blithedale_Romance.txt', 'r') as book:
    book_text = book.read()

with open('Blithedale_Romance_Tagged.xml', 'w') as tagged:
    tagged.write('<book>\n');
    tagged.write('<booktitle>The Blithedale Romance</booktitle>\n');
    tagged.write('<author>Nathaniel Hawthorne</author>\n');

    roman_nums = re.compile('\n\n[IVX]+\.\s')
    chapters = roman_nums.split(book_text);
    chapters.pop(0);
    num_chapters = len(chapters);

    for chapter in chapters:
        tagged.write('<chapter>\n');
        new_line = re.compile('\n{2,}')
        paragraphs = new_line.split(chapter);

        propers = re.findall('[A-Z][a-z]{2,}', chapter);
        for noun in propers:
            if (isImportant(noun)):
                if (properNouns.get(noun)):
                    properNouns[noun] += 1;
                else:
                    properNouns[noun] = 1;

        tagged.write('<chaptertitle>\n'+paragraphs[0]+'\n</chaptertitle>\n');
        tagged.write('<characters>\n');
        sortedProperNouns = sorted(properNouns.items(), key=sortMeToo, reverse=True)[:3];
        for i in sortedProperNouns:
            tagged.write("<character occurences=" + str(i[1]) + ">"+ i[0] + "</character>\n");
        tagged.write('</characters>\n');
        paragraphs.pop(0);

        for paragraph in paragraphs:
            paragraph = re.sub('"', quoterepl, paragraph)
            tagged.write('<paragraph>\n'+paragraph+'\n</paragraph>\n');
        tagged.write('</chapter>\n');

    tagged.write('</book>');
    properNouns = {};

max_pos = 0;
with open('Blithedale_Romance_Stats.txt', 'w') as stats:
    propers = re.finditer('[A-Z][a-z]{2,}', book_text);
    for noun in propers:
        pos = noun.start();
        if pos > max_pos:
            max_pos = pos
        name = noun.group();
        if (isImportant(name)):
            if (properNouns.get(name)):
                properNouns[name].append(pos);
            else:
                properNouns[name] = [pos];

    sortedProperNouns = sorted(properNouns.items(), key=sortMe, reverse=True)[:10];

    stats.write("\n\n-----------------------------------------------\n");
    stats.write("Occurences\n");
    stats.write("See how many times these names are mentioned in the book. These will be important to study!\n");
    stats.write("-----------------------------------------------\n\n");
    for noun in sortedProperNouns:
        stats.write(str(noun[0]) + " - " + str(len(noun[1])) + " occurences\n");

    stats.write("\n\n-----------------------------------------------\n");
    stats.write("Character Arcs!\n");
    stats.write("Each x is period in the book where that name appears more than once.\n");
    stats.write("to the left is percent through the book.\n");
    stats.write("-----------------------------------------------\n\n");
    stats.write("Start of Book\n");
    stats.write("----");
    for noun in sortedProperNouns:
        stats.write("| " + str(noun[0]).ljust(16));
    stats.write("\n");
    stats.write("----");
    for noun in sortedProperNouns:
        stats.write("-+-+".ljust(18));
    stats.write("\n");

    for i in range(histogram_height):
        stats.write(format((float(i)/histogram_height), '.2f'));
        for noun in sortedProperNouns:
            if numInRange(noun[1], ((max_pos/histogram_height)*i), ((max_pos/histogram_height)*(i+1))) > 1:
                stats.write("|" + "    x".ljust(17));
            else:
                stats.write("|" + " ".ljust(17));
        stats.write("\n");
    stats.write("----");
    for noun in sortedProperNouns:
        stats.write("-+-+".ljust(18));
    stats.write("\n");
    stats.write("End of Book\n");

    print "Done! Check Blithedale_Romance_Stats.txt for stats."
