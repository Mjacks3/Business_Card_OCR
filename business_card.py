from nltk import word_tokenize, pos_tag, ne_chunk


class ContactInfo:
  def __init__(self,document):
        self.document = document
        self.name = ""
        self.phone = ""
        self.email = ""
        
        self.getName()
        self.getPhoneNumber()
        self.getEmailAddress()
        self.print_info()
    
  def getName(self):
      
        #if Name Heading appears, strip that line and use that.
        if "name" in "".join(self.document).lower():
            for line in self.document:
                if "name" in line.lower():
                            self.name = " ".join(str(piece) for piece in line.split()[1:])
                            
                            
                            
        #Use nltk's named entity parsing to best identify human names from the input
        #Not always accurate:
        # Some human names and nonhuman names might not be accepted
        #Gracefully handle, like most application parsers would do
        else:
            for line in self.document:
                annotated_chunks = ne_chunk(pos_tag(word_tokenize(line)))
                for single_chunk, source_word  in zip(annotated_chunks, line.split()):
                        try:
                                if single_chunk.label() == "PERSON":
                                    self.name += source_word
                                    self.name += " "
                        except AttributeError:
                            pass

  def getPhoneNumber(self):

        #if Name Heading appears, strip that line and use that.
        if any(phone_words in "".join(self.document).lower() for phone_words in ["phone","ph","telephone","tel"]): #how else might phone # heading appear?
            for line in self.document:
                if any(phone_words in line.lower() for phone_words in ["phone","ph","telephone","tel"]):
                    for char in line:
                        if char.isnumeric():
                            self.phone += char
           
        #some line should have 7+ digits, make sure it's not the fax # and use that             
        else:
            for line in self.document:
                if  not any(fax_words in line.lower() for fax_words in ["fax", "fx"]):
                    potiential_phone_number = ""

                    for char in line:
                        if char.isnumeric():
                            potiential_phone_number += char

                    if len(potiential_phone_number) >= 7:
                        self.phone = potiential_phone_number 
                        
    
  def getEmailAddress(self):
    
        #if Email Heading appears, strip that line and use that.
        if "email" in "".join(self.document).lower():
            for line in self.document:
                if "email" in line.lower():
                            self.email = " ".join(str(piece) for piece in line.split()[1:])
                            
        #Check for an @ symbol...all emails need this right?
        else:
            for line in self.document:
                if "@" in line:
                    for chunk in line.split():
                        if "@" in chunk:
                            self.email = chunk
                        
    
  def print_info(self):       
        print("Name:", self.name)
        print("Phone:",self.phone)
        print("Email:",self.email)



class BusinessCardParser:
  def __init__(self):
        pass
    
  def getContactInfo(self,document):
        new_contact_info = ContactInfo(document)
        return new_contact_info
    

f = open("input.txt", "r")
ContactInfo(f.readlines())
