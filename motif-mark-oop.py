#!/usr/bin/env python
import re
import cairo
import argparse
import random

## ARGPARSE ##

def get_args():
    parser = argparse.ArgumentParser(description = "This program will take in a fasta file and a motif file to create an image of the introns, exons and motifs present")
    parser.add_argument("-f", "--fasta", help="Input the filename for the fasta file", required=True, type=str)
    parser.add_argument("-m", "--motif", help="Input the filename for the motif listing", required=True, type=str)
    return parser.parse_args()

args = get_args()
fasta = args.fasta
motif = args.motif

## VARIABLES ##

#Open the files
f_file = open(fasta,"r")
m_file = open(motif,"r")
of_file = open("temp.fa","w")
#Getting the new name for the context
out_file = fasta.split("/")[-1]
out_name = out_file.split(".")[0]+".svg"
out_png = out_file.split(".")[0]+".png"


#Creating dictionaries
motif_dict = {} #Motif of original and replaced motif Y-> [TC]
motif_color = {} #Motif of replaced motif and color

#Define context
surface = cairo.SVGSurface(out_name, 800, 1000)
context = cairo.Context(surface)

#Define the width of each class
gene_width = 5
exon_width = 35
motif_width = 30

#Define the start position in context (x-axis)
start = 100


## CLASSES ##

class Gene:

    def __init__(self, length, the_name):

        ## Data ##
        self.len = length
        self.end = start + length
        self.name = the_name

    ## Methods ##

    def draw(self,context,y_height):
        context.set_source_rgb(0, 0, 0)
        context.set_line_width(gene_width)
        context.move_to(start, y_height)
        context.line_to(self.end, y_height)
        context.stroke()
    


class Exon:

    def __init__(self, start_pos, length):
        '''Exon main data'''

        ## Data ##
        self.len = length
        self.start = start_pos + start
        self.end = self.start + length
    
    ## Methods ##

    def draw(self,context, y_height):
        context.set_source_rgb(0, 0, 0)
        context.set_line_width(exon_width)
        context.move_to(self.start, y_height)
        context.line_to(self.end, y_height)
        context.stroke()


class Motif:

    def __init__(self, start_pos, length, the_name):
        '''Motif main data'''

        ## Data ##
        self.len = length
        self.start = start_pos + start
        self.name = the_name #Motif Replaced name Y -> [TC]
        self.end = self.start + length
        self.color = motif_color[self.name]
        self.type = motif_dict[self.name]

    ## Methods ##

    def draw(self,context,y_height):
        context.set_source_rgb(self.color[0], self.color[1], self.color[2])
        context.set_line_width(motif_width)
        context.move_to(self.start, y_height)
        context.line_to(self.end, y_height)
        context.stroke()


class Cabinet:

    def __init__(self, gene:Gene, exon:Exon, motifs:list[Motif], header, the_y):
        '''Filing all genes with their specific motifs and exons'''

        ## Data ##
        self.genes = gene
        self.exons = exon
        self.motif_lst = motifs
        self.header = header
        self.y= the_y
        

    ## Methods ##

    def draw(self,context,y):
        # Print the header
        context.set_source_rgb(0,0,0)
        context.set_font_size(20)
        context.select_font_face(
        "Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        context.move_to(start, y-40)
        context.show_text(self.header)
        context.stroke()

        # Write the motif for color
        self.genes.draw(context,y)
        self.exons.draw(context,y)
        for mo in self.motif_lst:
            mo.draw(context,y)



## FUNCTIONS ##

#This function will create fasta files with only one line
def oneline_fasta(input_file, out_file: str):
    '''This function takes two file names (input and output) which converts an unwrapped fasta file
    to a two line convention'''
    data = []
    header = ""
    count = 0
    for line in input_file:
        line  = line.strip()
        if ">" in line: #To identify the header
            if header == "": #For the first line prot_id wont have a value
                header = line
            else:    #For the rest of the lines
                seq = "".join(data)
                data.clear()
                count += 1
                out_file.write(f'{header}\n{seq}\n')
                header = line
        else:
            data.append(line)
    seq = "".join(data)
    data.clear()
    count += 1
    out_file.write(f'{header}\n{seq}\n')
    return(count)

# Read through FASTA File

def read_fa(f: str):
    ''''This function will read through the FASTA file per record and will return a list with the data'''
    head = f.readline().strip()
    seq = f.readline().strip()
    seq_len = len(seq)
    if head == "":
        return 0
    return [head, seq, seq_len]

# Read and create a list of possible motifs
def read_mot(motif_file:str):
    '''This function will read through the file of motifs and create a set with all possible motifs and create a dictionary of possible colors'''
    n=0
    random_list = []
    motif_types = []
    type_color = {}
    for line in motif_file:
        line = line.strip("\n")
        motif_types.append(line)
        n+=1
        for i in range(0,3):
            a = round(random.uniform(0, 0.9),1)
            random_list.append(a)
        if re.search("[Yy]",line):
            type_color[line] = random_list
            new_line = re.sub("[Yy]", "[TCtc]", line)
            motif_dict[new_line] = line
            motif_color[new_line] = random_list
        if re.search("[Uu]", line):
            type_color[line] = random_list
            new_line = re.sub("[Uu]", "[Tt]", line)
            motif_dict[new_line] = line
            motif_color[new_line] = random_list
        else:
            type_color[line] = random_list
            motif_color[line] = random_list
            motif_dict[line] = line
        random_list = []
    return(motif_dict, motif_color, motif_types, type_color)

def exon_finder(seq:str):
    '''Find the Exons (capital letters) and return the position and length'''
    length = []
    for pos,letter in enumerate(seq):
        if re.findall("[ATCG]",letter):
            length.append(pos)
    start = length[0]
    exon_length = len(length)
    return(start, exon_length)

def motif_finder(seq:str, motif_dic:dict):
    '''Find all possible motifs and return a tuple with the motif type, start_pos and length'''
    motif_lists = []
    for type,mot in motif_dic.items():
        motif_match = re.finditer(type, seq)
        for item in motif_match:
            indx = item.span()[0]
            item_len = item.span()[1] - indx
            motif_lists.append((indx, item_len, type))
    return(motif_lists)

## CODE ##

# Creating the new one-line fasta file
qty_genes = oneline_fasta(f_file, of_file)
of_file.close()
#Get the y position for each gene
y = 800/qty_genes

# Read in the motif file and create necessary dictionaries
dict_motifs, dict_colors, motif_types, type_b_color= read_mot(m_file)


# Parse through Fasta file
# For each record;
    #Obtain length of the sequence ; create gene object

x=0
with open("temp.fa","r") as fr:
    while True:
        R1 = read_fa(fr)
        #If the read 1 encounters an empty line it will stop reading and break the loop
        if  R1 == 0:
            break
        x+=1
        #Giving the comprehensible names ; create gene object
        header, seq, seq_len = R1
        genex=Gene(seq_len,header)
        #Find the exon (start position, length) ; create exon object
        exon_start, exon_len = exon_finder(seq)
        exonx=Exon(exon_start,exon_len)
        #Find all possible motifs (Create a list of all; start position, length, type of motif) ; create list of objects
        motif_lists = motif_finder(seq,dict_motifs)
        m=0
        motifs_object_list = []
        for mot in motif_lists:
            m+=1
            variant = str(m)
            motif_name = "motif_"+variant
            motif_name = Motif(mot[0],mot[1],mot[2])
            motifs_object_list.append(motif_name)
        #Create the cabinet object
        cabinet_name = "cabinet"+str(x)
        cabinet_name = Cabinet(genex,exonx,motifs_object_list,header,y)
        cabinet_name.draw(context,y)

        y+=200

'''Write all titles for motifs'''
context.set_source_rgb(0, 0, 0)
#Writing the font for motifs
context.set_font_size(20)
context.select_font_face(
    "Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
context.move_to(650, 50)
context.show_text("Motifs")
context.stroke()

#For each type
x=70
for type in motif_types:
    context.set_font_size(10)
    context.select_font_face("Arial")
    context.move_to(670, x)
    context.show_text(type)
    context.stroke()
    x+=23
x=70

for type,coloring in type_b_color.items():
    color = type_b_color[type]
    context.set_source_rgb(color[0], color[1], color[2])
    context.set_line_width(10)
    context.move_to(650, x)
    context.line_to(665, x)
    context.stroke()
    x+=22


surface.write_to_png(out_png)
surface.finish()
f_file.close()
m_file.close()