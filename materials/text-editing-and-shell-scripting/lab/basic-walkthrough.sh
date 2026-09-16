#!/usr/bin/bash


#This script is a general script I've written to do all the exercises in the day 4 tutorial sheet
#This will do everything...
#Please take your time to peruse this script and make sure you understand what every line is doing in here
#Built with love by Joseph Sedem
#Yes Psirdem, The better form of Awesome....

#DISCLAIMAR !!!!! This Script is not that smart... 
#It is written very basically so that you can read and understand what is going on
#I will attach a more sofisticated script that will do the same thing in a more optimized way for those interested...



#creating a shellscripts directory in our handson directory
rm -rf ~/handson/shellscripts/
mkdir -p ~/handson/shellscripts/

# we copy the handson_files.zip and the nickel_data.zip
cp handson_files.zip nickel_data.zip ~/handson/shellscripts/

#We are entering the just created directory
cd ~/handson/shellscripts/

#We quietly unzip the zip files into the the shellscripts directory
unzip -q handson_files.zip 
unzip -q nickel_data.zip
rm -r __MACOSX
rm handson_files.zip nickel_data.zip

#We create the respective exercise directories
mkdir -p exercise_1 exercise_2 exercise_3

#Now we create and execute our exercise_1.sh script

#first lets cd into the exercise_1 directory
cd exercise_1

#then we create and make executable the exercise_1.sh file
touch exercise_1.sh && chmod 755 exercise_1.sh

#Now we dump the commands that will perform the Exercise 1 task
echo "#!$(which bash)">> exercise_1.sh
echo "grep -i 'final energy' ../handson_files/N2H4_qe_output.txt | awk -F ' ' '{print \$4}' > final_energy.txt" >> exercise_1.sh

#Now we execute the exercise_1.sh script
source exercise_1.sh
echo "done with Exercise 1, $(whoami)"

#Now we create and execute our exercise_2.sh script

#first lets cd into the exercise_2 directory
cd ~/handson/shellscripts/exercise_2

#then we create and make executable the exercise_2.sh file
touch exercise_2.sh && chmod 755 exercise_2.sh

#Now we dump the commands that will perform the Exercise 2 task
echo "#!$(which bash)">> exercise_2.sh

echo "grep -ir 'final enthalpy' ~/handson/shellscripts/nickel_data/ | sort | awk -F ' ' '{print \$5}' > enthalbuff.txt
" >> exercise_2.sh

echo "paste ~/handson/shellscripts/nickel_data/kine_ener.txt  ~/handson/shellscripts/exercise_2/enthalbuff.txt  > kiv_vrs_enthalpy.dat
" >> exercise_2.sh

#Now we execute the exercise_1.sh script
source exercise_2.sh
rm enthalbuff.txt
echo "done with Exercise 2, $(whoami)"




#Now we create and execute our exercise_3.sh script

#first lets cd into the exercise_3 directory
cd ~/handson/shellscripts/exercise_3

#then we create and make executable the exercise_3.sh file
touch exercise_3.sh && chmod 755 exercise_3.sh

#Now we dump the commands that will perform the Exercise 3 task
echo "#!$(which bash)">> exercise_3.sh

echo "grep -ir 'final enthalpy' ~/handson/shellscripts/nickel_data/ | sort | awk -F ' ' '{print \$5}' > enthalbuff.txt
" >> exercise_3.sh

echo "paste ~/handson/shellscripts/nickel_data/kine_ener.txt  ~/handson/shellscripts/exercise_3/enthalbuff.txt  > kiv_vrs_enthalpy.dat
" >> exercise_3.sh

echo "awk -F ' ' '{print \$2*13.605 }' kiv_vrs_enthalpy.dat >  evbuff.txt" >> exercise_3.sh

echo "paste kiv_vrs_enthalpy.dat evbuff.txt > final_ry_ev.dat" >> exercise_3.sh


#Now we execute the exercise_3.sh script
source exercise_3.sh
rm enthalbuff.txt evbuff.txt kiv_vrs_enthalpy.dat
echo "done with Exercise 3, $(whoami)"
