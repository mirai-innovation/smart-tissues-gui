# smart-tissues-gui
Programa Enfutech Mirai Innovation

Folder "DataConvert" :
To tranforms PDF to txt we have to use the program pdftotxt.py in the same folder it only transform all the pdf in the DataPDF folder to txt files.

Then to create the model or train it, use the Modelo\Trainmodel.py, please read the  line 7 and 8, you only need to modify this lines to changes the model or the data to train the model, but you can just add the new data to the data.json file just following the json format that is include

to run program that get the csv, you just run the textspliv2.py without modificate any file from any folder, this program will trow a csv in the folder extracted_sections.

if you want to update the csv from the web page, you just have to changes the file named datos.csv in the next direction:
smts\static\ 

changes the existent file with thew new one

Steps to run the web pages:
run the following commands in the terminal of the project
1.- smarttissuesENV\Scripts\activatettissuesENV
2.- py .\smts\manage.py runserver
