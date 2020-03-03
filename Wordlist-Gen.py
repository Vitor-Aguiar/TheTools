import os
import sys


#       -t @,%^
#              Specifies  a pattern, eg: @@god@@@@ where the only the @'s, ,'s,
#              %'s, and ^'s will change.
#              @ will insert lower case characters
#              , will insert upper case characters
#              % will insert numbers
#              ^ will insert symbols


if len(sys.argv) != 3:
	print "Usage: python gen.py word wordlist.txt"
	sys.exit()

word = sys.argv[1]
wordlist = sys.argv[2]

masks = [word+"^%" , word+"^%%" , word+"^%%%" , word+"^%%%%" , #word+"^%%%%%" , word+"^%%%%%%" ,
	 word+"%^" , word+"%%^" , word+"%%%^" , word+"%%%%^" , #word+"%%%%%^" , word+"%%%%%%^" ,
	 "^%"+word , "^%%"+word , "^%%%"+word , "^%%%%"+word , #"^%%%%%"+word , "^%%%%%%"+word ,
	 "%^"+word , "%%^"+word , "%%%^"+word , "%%%%^"+word , #"%%%%%^"+word , "%%%%%%^"+word
	 "^"+word  , word+"^" , 
	 "^"+word+"%" , "^"+word+"%%" , "^"+word+"%%%" , "^"+word+"%%%%" , # "^"+word+"%%%%%" ,
	 "%"+word+"^" , "%%"+word+"^" , "%%%"+word+"^" , "%%%%"+word+"^" , # "%%%%%"+word+"^" ,
	 word ,
	 word+"%" , word+"%%" , word+"%%%" , word+"%%%%" , 
	 "%"+word , "%%"+word , "%%%"+word , "%%%%"+word
	]

for n,mask in enumerate(masks):
	tamanho = str(len(mask))
	comando = "crunch "+tamanho+" "+tamanho+" -t "+mask+" -o "+str(n)+wordlist+".txt"
	print "Comando: ",comando
	os.system(comando)
os.system('cat *'+wordlist+'.txt >> '+wordlist+'_wordlist.txt')
os.system('rm *'+wordlist+'.txt')
