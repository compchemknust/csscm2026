#!/usr/bin/bash


#This script is a general script I've written to do all the exercises in the day 4 tutorial sheet
#This will do everything...
#Please take your time to peruse this script and make sure you understand what every line is doing in here
#Built with love by Joseph Sedem
#Yes I am Psirdem, The better form of Awesome....

SCRIPTPATH="/home/$(whoami)/handson/shellscripts"

#creating a shellscripts directory in our handson directory and copy the handson_files.zip and the nickel_data.zip
rm -rf $SCRIPTPATH
mkdir -p $SCRIPTPATH && unzip -qo '*.zip' -d $SCRIPTPATH 

# #We are entering the just created directory
cd $SCRIPTPATH &&   rm -r __MACOSX && mkdir -p exercise_{1..3}

FILE1="exercise_1.sh"
# #first lets cd into the exercise_1 directory
cd exercise_1 && touch $FILE1 && chmod 755 $FILE1

#Now we dump the commands that will perform the Exercise 1 task
echo -e "#!$(which bash) \n grep -i 'final energy' ../handson_files/N2H4_qe_output.txt | awk -F ' ' '{print \$4}' > final_energy.txt">> $FILE1

# #Now we execute the $FILE1 script
source $FILE1 && echo "done with Exercise 1, $(whoami)"

# #Now we create and execute our $FILE2 script
FILE2="exercise_2.sh"
# #first lets cd into the exercise_2 directory  and create and make executable the $FILE2 file
cd ../exercise_2 && touch $FILE2 && chmod 755 $FILE2

# #Now we dump the commands that will perform the Exercise 2 task
echo -e "#!$(which bash) \n grep -ir 'final enthalpy' $SCRIPTPATH/nickel_data/ | sort | awk -F ' ' '{print \$5}' > enthalbuff.txt
\n paste $SCRIPTPATH/nickel_data/kine_ener.txt  $SCRIPTPATH/exercise_2/enthalbuff.txt  > kiv_vrs_enthalpy.dat
" >> $FILE2

# #Now we execute the $FILE1 script
source $FILE2 && rm enthalbuff.txt && echo "done with Exercise 2, $(whoami)"

# #Now we create and execute our $FILE3 script
FILE3="exercise_3.sh"
# #first lets cd into the exercise_3 directory and create and make executable the $FILE3 file
cd ../exercise_3 && touch $FILE3 && chmod 755 $FILE3


# #Now we dump the commands that will perform the Exercise 3 task
echo -e "#!$(which bash) 
\n grep -ir 'final enthalpy' ../nickel_data/ | sort | awk -F ' ' '{print \$5}' > enthalbuff.txt
\n paste $SCRIPTPATH/nickel_data/kine_ener.txt  $SCRIPTPATH/exercise_3/enthalbuff.txt  > kiv_vrs_enthalpy.dat
\n awk -F ' ' '{print \$2*13.605 }' kiv_vrs_enthalpy.dat >  evbuff.txt
\n paste kiv_vrs_enthalpy.dat evbuff.txt > final_ry_ev.dat">> $FILE3

# #Now we execute the $FILE3 script
source $FILE3 &&  rm enthalbuff.txt evbuff.txt kiv_vrs_enthalpy.dat && echo "done with Exercise 3, $(whoami)"
