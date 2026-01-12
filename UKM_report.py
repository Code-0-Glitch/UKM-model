from cycler import K
from matplotlib.pylab import int8
import numpy as np;
import pandas as pd;
import matplotlib.pyplot as plt
from pyparsing import line


Dialysis_Adequacy = 0.00;
# HUME WAYERS FORMULA FOR CALCULATION OF THE UREA DISTRIBUTION VOLUME Vu
vu = 0.00;
Patient_weight = input("ENTER THE WEIGHT OF PATIENT (kg): ");
Patient_weight = float(Patient_weight);
Patient_height = input("ENTER THE HEIGHT OF THE PATIENT (cm): ");
Patient_height = float(Patient_height);
Gender_spell=False;
while (Gender_spell==False):
    Patient_gender = input("ENTER THE GENDER OF THE PATIENT IS: ");
    Patient_gender  = Patient_gender.upper();
    if(Patient_gender == "MALE"):
        Vu = (0.194786 * Patient_height) + (0.29678 * Patient_weight) - 14.012934;
        Gender_spell=True;
    elif(Patient_gender == "FEMALE"):
        Vu = (0.34454 * Patient_height) + (0.183809 * Patient_weight) - 35.270121;
        Gender_spell=True;
    else:
        print("PLEASE ENTER CORRECT GENDER (MALE/FEMALE) ONLY")
         
Starting_Conc = input("ENTER STARTING BUN MEASUREMENT: ")
Starting_Conc = float(Starting_Conc)
# print(f"starting BUN measure: ", Starting_Conc)
Target_Conc = (Starting_Conc*30)/100
Dialysis_time = int(input("ENTER DIALYSIS TIME (HOURS): "))
Sampling_time = int(Dialysis_time) * 60;

time_interval = [];
for i in range(0, int(Sampling_time), 5):
    time_interval.append(i)
Decay = 1;
Target_DATA = False;
print(Decay)
BUN_at_time_t = []
CONC_T = 0.0;
iteration = 0;
while (Target_DATA == False):
    if (CONC_T == 0.0):
        CONC_T = Starting_Conc
        BUN_at_time_t.append(CONC_T)
    for i in range(0, int(Sampling_time), 1):
        CONC_T = CONC_T * np.exp(Decay)
        BUN_at_time_t.append(CONC_T)
    iteration += 1         
    if(BUN_at_time_t[-1] > (Target_Conc-1) and BUN_at_time_t[-1] < (Target_Conc+1)):
        Target_DATA = True;
        print("******************* TARGET_REACHED: TERMINATING ITERATIONS *******************")
        print(f"Iteration No. {iteration}, BUN at {Sampling_time} min: {BUN_at_time_t[-1]}, Decay: {Decay}")
        print(f"Patient Urea Distribution Volume: ",Vu)
        Dialysis_Adequacy = float(Decay * Sampling_time)
        break;
    elif (BUN_at_time_t[-1] > Target_Conc):
        print(f"Iteration No. {iteration}, BUN at {Sampling_time} min: {BUN_at_time_t[-1]}, Decay: {Decay}")
        print("*** OUT OF RANGE: REIERATING DECAY EXPONENT ***")
        Decay -= 0.0001
        BUN_at_time_t.clear()
        CONC_T = 0.0;
    elif (BUN_at_time_t[-1] < Target_Conc):
        print(f"Iteration No. {iteration}, BUN at {Sampling_time} min: {BUN_at_time_t[-1]}, Decay: {Decay}")
        print("*** OUT OF RANGE: REIERATING DECAY EXPONENT ***")
        Decay += 0.0001
        BUN_at_time_t.clear()
        CONC_T = 0.0;

# creating the data-file comprising of data related to the final iteration:

conc_at_sampling_T = []
Sampling_interval  = []
index_Report = []
j = 0;
for i in range(0, Sampling_time, 5):
    conc_at_sampling_T.append(BUN_at_time_t[i]);
    Sampling_interval.append(i);
    j +=1;
    index_Report.append(j)
print("\n************************************************************************************************")
print("                                             REPORT                                             ")
print("************************************************************************************************")
print(f"\nDecay_Constant:   {Decay}\nStarting_BUN:  {Starting_Conc}\nPatient_Urea_Distribution_Volume:  {Vu}\nHemodialysis_Adequacy:    {abs(Dialysis_Adequacy)}\nClearance(K):  {abs(Decay*(Vu*1000))} mL/min\n")
DataFile = {"BUN_at_time(t)": conc_at_sampling_T,
            "Sampling_interval": Sampling_interval};
Report = pd.DataFrame(data= DataFile, index=index_Report)
Report = Report.rename_axis(index = None, columns="Serial No")
print(Report)
print("************************************************************************************************")
print("************************************************************************************************")
x= np.array(Sampling_interval);
y= np.array(conc_at_sampling_T);
plt.plot(x, y)
plt.xlabel("Time");
plt.ylabel("BUN(mg/dL)");
plt.title("Hemodialysis_Adequacy")
plt.show()