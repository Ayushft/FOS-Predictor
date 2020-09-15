#Inputs
import time
import math 
import pandas as pd
import numpy as np

matdata = {
    'Material' : ['Aluminum','Brass','Bronze','Copper','Stainless Steel'],
    'Youngs Modulus' : [69,106,112,117,205],
    'Shear Modulus' : [26.1,38.8,42.4,44,79],
    'Poissons Ratio' : [0.33,0.318,0.324,0.28,0.265],
    'Density' : [2700,8490,8380,8960,7920],
    'Hardness' : [95,65.1,168,89,382],
    'Tensile Yield Strength' : [240,255,314,330,965],
    'Compressive Yield Strength' : [182.02,144,341,331,515],
    'Ultimate Tensile Strength' : [290,430,490,655,1276],
    'Ultimate Compressive Strength' : [220,165,490,505,720],
    }

matdb = pd.DataFrame(matdata)
matdb.set_index('Material',inplace=True)
print(matdb)

sigma_x = float(input("Please enter the Direct Stress in x-direction : "))
sigma_y = float(input("Please enter the Direct Stress in y-direction : "))
tau_xy = float(input("Please enter the Shear Stress in xy plane: "))
sigma_yt = float(input("Please enter the Tensile Yield Strength : "))
sigma_yc = float(input("Please enter the Compressive Yield Strength : "))
sigma_ut = float(input("Please enter the Ultimate Tension Strength : "))
sigma_uc = float(input("Please enter the Ultimate Compressive Strength : "))
epsilon_f = float(input("Please enter the True Strain at fracture : "))

def is_conservative():
    conservative = input("Need Accurate Results or Conservative Results? type 1 for accurate and 0 for conservative :" )
    if conservative == 1:
        return True
    if conservative == 0:
        return False
    return
is_conservative()

# default Values for plane stress condition
sigma_z = 0
tau_xz = 0
tau_yz = 0
gama_yz = 0
gama_xz = 0
sigma_3 = 0

# Preliminary Calculations
sigma_1 = ((sigma_x + sigma_y) / 2) + (((((sigma_x - sigma_y) / 2) ** 2) + (tau_xy ** 2)) ** 0.5)
sigma_2 = ((sigma_x + sigma_y) / 2) - (((((sigma_x - sigma_y) / 2) ** 2) + (tau_xy ** 2)) ** 0.5)
sigma_a = max(sigma_1, sigma_2)
sigma_b = min(sigma_1, sigma_2)
tau_1 = abs((sigma_2/2))
tau_2 = abs((sigma_1/2))
tau_3 = abs((sigma_1-sigma_2)/2)
tau_max = max((tau_1,tau_2,tau_3))
tau_min = min((tau_1,tau_2,tau_3))

#branching the practices
def practice_1() :
    variable1 = "Factor of safety using Modified Mohr Theory is :"
    if sigma_a >= sigma_b >= 0 :
        fos_1 = sigma_ut / sigma_a
        return (variable1+ str(fos_1))
    elif sigma_a >= 0 >= sigma_b :
        fos_1 = ((((sigma_uc - sigma_ut) * sigma_a) / (sigma_uc * sigma_ut)) - (sigma_b / sigma_uc)) ** -1
        return (variable1+ str(fos_1))
    elif 0 >= sigma_a >= sigma_b :
        fos_1 = (-sigma_uc/ sigma_b)
        return (variable1+ str(fos_1))
    return

def practice_2() :
    variable2 = "Factor of safety using Brittle Coulomb Mohr Theory is :"
    if sigma_a >= sigma_b >= 0 :
        fos_2 = sigma_ut / sigma_a
        return (variable2 + str(fos_2))
    elif sigma_a >= 0 >= sigma_b :
        fos_2 = (((sigma_uc * sigma_a) - (sigma_ut*sigma_b)) / (sigma_ut*sigma_uc)) ** -1
        return (variable2 + str(fos_2))
    elif 0 >= sigma_a >= sigma_b :
        fos_2 = (-sigma_uc/ sigma_b)
        return (variable2 + str(fos_2))
    return

def practice_3() :
    variable3 = "Factor of safety using Ductile Coulomb Mohr Theory is :"
    if sigma_a >= sigma_b >= 0 :
        fos_3 = sigma_yt / sigma_a
        return (variable3 + str(fos_3))
    elif sigma_a >= 0 >= sigma_b :
        fos_3 = (((sigma_yc * sigma_a) - (sigma_yt*sigma_b)) / (sigma_yt*sigma_yc)) ** -1
        return (variable3 + str(fos_3))
    elif 0 >= sigma_a >= sigma_b :
        fos_3 = (-sigma_yc/ sigma_b)
        return (variable3 + str(fos_3))
    return

def practice_4() :
    variable4 = "Factor of safety using Distortion Energy Theory is :"
    if sigma_a >= sigma_b :
        fos_4 = sigma_yt / (((sigma_a ** 2) - (sigma_a * sigma_b) + (sigma_b ** 2)) ** 0.5)
        return (variable4 + str(fos_4))
    return

def practice_5() :
    variable5 = "Factor of safety using Maximum Shear Stress Theory is :"
    if sigma_a >= sigma_b >= 0 :
        fos_5 = sigma_yt/ sigma_a
        return (variable5 + str(fos_5))
    elif sigma_a >= 0 >= sigma_b :
        fos_5 = sigma_yt / (sigma_a - sigma_b)
        return (variable5 + str(fos_5))
    elif 0 >= sigma_a >= sigma_b :
        fos_5 = -sigma_yt / sigma_b
        return (variable5 + str(fos_5))
    return


def Factor_Safety() :
    if epsilon_f < 0.05 :
        if is_conservative == False :
            return practice_1()
        else :
            return practice_2()
    else :
            if ((sigma_yt == sigma_yc) == False) :
                return practice_3()
            else :
                if is_conservative == False :
                    return practice_4()
                else :
                    return practice_5()
    return

A = Factor_Safety()

#printing main output
print(A)


# Additional Detailed Results
def is_additional(additional) :
    if additional == 1:
        youngsmod = float(input("Please enter the Young's Modulus of the material :"))
        shearmod = float(input("Please enter the Shear Modulus of the material :"))
        poisson = float(input("Please enter the Poisson's Ratio of the material :"))

        epsilon_x = ((sigma_x - poisson * sigma_y) / youngsmod)
        epsilon_y = ((sigma_y - poisson * sigma_x) / youngsmod)
        epsilon_z = ((-poisson*(sigma_x + sigma_y)) / youngsmod)
        gama_xy = (tau_xy / shearmod)
        strain_energy = (0.5 * ((sigma_x * epsilon_x) + (sigma_y * epsilon_y) + (tau_xy * gama_xy)))
        bulkmod = (youngsmod / (3 * (1 - 2 * poisson)))

        print("Youngs Modulus of Material :", youngsmod)
        print("Shear Modulus of Material :", shearmod)
        print("Poisson's Ratio of the Material :", poisson)
        print("Bulk modulus of the Material :", bulkmod)
        print("Strain Energy :", strain_energy)
        print("Normal Stress in x-direction :", sigma_x)
        print("Normal Stress in y-direction :", sigma_y)
        print("Normal Stress in z-direction :", sigma_z)
        print("Shear Stress on xy plane :", tau_xy)
        print("Shear Stress on yz plane :", tau_yz)
        print("Shear Stress on xz plane :", tau_xz)
        print("Normal Strain is x direction :", epsilon_x)
        print("Normal Strain is y direction :", epsilon_y)
        print("Normal Strain is z direction :", epsilon_z)
        print("Shear Strain is xy plane :", gama_xy)
        print("Shear Strain is yz plane :", gama_yz)
        print("Shear Strain is xz plane :", gama_xz)
        print("First Principal Normal Stress :", sigma_1)
        print("Second Principal Normal Stress :", sigma_2)
        print("Third Principal Normal Stress :", sigma_3)
        print("Maximum Principal Normal Stress :", sigma_a)
        print("Minimum Principal Normal Stress :", sigma_b)
        print("First Principal Shear Stress :", tau_1)
        print("Second Principal Shear Stress :", tau_2)
        print("Third Principal Shear Stress :", tau_3)
        print("Absolute Maximum Shear Stress :", tau_max)
        print("Absolute Minimum Shear Stress :", tau_min)

    else:
         exit()
    return

additional = int(input("please type 1 for Additional Detailed Results or 0 to exit : "))
is_additional(additional)

