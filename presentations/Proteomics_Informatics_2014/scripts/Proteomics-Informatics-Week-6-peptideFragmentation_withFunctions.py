
#===============================================================================
# Given a peptide sequence and charge-state, compute the theoretical spectrum
#    -> Check against the website ("http://db.systemsbiology.net:8080/proteomicsToolkit/FragIonServlet.html")
# Possible extensions:
#     a. Neutral Losses (HW-2)
#     b. Higher charge states (HW-2)
#     c. Other ion-types (a/c/x/z-ions, ETD spectra etc.) (later)
#     d. PTMs (later)
#             mods = [{'aa': 'C', 'index': 0, 'modValue': 57.02147}, \
#                     {'aa': 'C', 'index': 0, 'modValue': -17.02655}]
# New Concepts:
#     a. writing functions and procedural programs
#===============================================================================

import ipdb         ## Interactive Python debugger. Also useful for exploring code.
ipdb.set_trace()    ## If it is not available, install it from system cmd prompt: $pip install ipdb  

#===============================================================================
# Constants, parameters etc.
#===============================================================================
m_proton = 1.007276

## Atomic masses
m_H = 1.007825035
m_O = 15.99491463
m_N = 14.003074
m_C = 12.0
m_S = 31.9720707
m_P = 30.973762

## Molecular masses
m_h2o = 2*m_H + m_O
m_nh3 = m_N + 3*m_H
monoMassAA = {'A' : 3*m_C + 5*m_H + m_O + m_N, 
              'C' : 3*m_C + 5*m_H + m_O + m_N + m_S,
              'D' : 4*m_C + 5*m_H + 3*m_O + m_N,
              'E' : 5*m_C + 7*m_H + 3*m_O + m_N,
              'F' : 9*m_C + 9*m_H + m_O + m_N,
              'G' : 2*m_C + 3*m_H + m_O + m_N,
              'H' : 6*m_C + 7*m_H + m_O + 3*m_N,
              'I' : 6*m_C + 11*m_H + m_O + m_N,
              'K' : 6*m_C + 12*m_H + m_O + 2*m_N,
              'L' : 6*m_C + 11*m_H + m_O + m_N,
              'M' : 5*m_C + 9*m_H + m_O + m_N + m_S,
              'N' : 4*m_C + 6*m_H + 2*m_O + 2*m_N,
              'P' : 5*m_C + 7*m_H + m_O + m_N,
              'Q' : 5*m_C + 8*m_H + 2*m_O + 2*m_N,
              'R' : 6*m_C + 12*m_H + m_O + 4*m_N,
              'S' : 3*m_C + 5*m_H + 2*m_O + m_N,
              'T' : 4*m_C + 7*m_H + 2*m_O + m_N,
              'V' : 5*m_C + 9*m_H + m_O + m_N,
              'W' : 11*m_C + 10*m_H + m_O + 2*m_N,
              'Y' : 9*m_C + 9*m_H + 2*m_O + m_N }


def compute_pepMass(pepSeq):
    pepMass = 0   ## running mass of the peptide    --------> pepMass is a local variable
    for aa in pepSeq:
        pepMass = pepMass + monoMassAA[aa]         #--------> monoMassAA is a global variable
    pepMass = pepMass + m_h2o  ## monoMassAA excludes N-terminal 'H' & C-terminal 'OH'
    return pepMass 

#def compute_multiCharge(fragList):
    ## Body goes here (HW-2)

#def compute_neutralLosses(fragList):
    ## Body goes here (HW-2)
    
def compute_fragments(pepSeq, z):
    pepMass = compute_pepMass(pepSeq)
    b_ions = []
    y_ions = []
    b_currentValue = m_proton    ## Adding a proton mass to residue mass (Remember: lecture from de novo sequencing; Add 1 to 1st b-ion and 19 to 1st y-ion)
    for index in range(len(pepSeq)-1):
        ## b-ions
        b_mz = b_currentValue + monoMassAA[pepSeq[index]]
        b_pos = index + 1           ## In the domain, ion position starts from 1, but in python str/list index starts from 0 
        b_seq = pepSeq[:index+1]    ## Slicing operation on "character strings" (str)
        b_ions.append({'type': 'b', 'pos': b_pos, 'seq': b_seq, 'z': 1, 'mz': b_mz})
            
        ## y-ions
        y_mz = pepMass - b_mz + 2*m_proton  ## y-ions need extra 19 adjustment (H + OH + proton); pepmass already has H+OH, but b_mz removes 1 proton... plus we need to add one proton for the y-ion, hence add 2*m_proton  
        y_pos = len(pepSeq) - b_pos
        y_seq = pepSeq[index+1:]
        y_ions.append({'type': 'y', 'pos': y_pos, 'seq': y_seq, 'z': 1, 'mz': y_mz})
        
        ## Update current value for next iteration
        b_currentValue = b_mz

    return (b_ions, y_ions)

print

#===============================================================================
# User input
#===============================================================================
#pepseq = "DGHTNNLRPK"   
#z_pep = 2
#neutralLoss = "n"
#multiCharge = "n"
pepSeq = raw_input("Enter peptide sequence: ")    ## raw_input(): function to accept raw keyboard input
z_pep = int(raw_input("Enter charge state: "))
neutralLoss = raw_input("Neutral losses [Enter choice: y(yes) or n(no)]: ")
multiCharge = raw_input("Multiply charged ions [Enter choice: y(yes) or n(no)]: ")
       

#===============================================================================
# Computations
#===============================================================================
b_ions, y_ions = compute_fragments(pepSeq, z_pep)

#===============================================================================
# Compute Neutral Losses: HW-2
#===============================================================================
# if neutralLoss == 'y':
#     b_ions.extend(compute_neutralLosses(b_ions))
#     y_ions.extend(compute_neutralLosses(y_ions))

#===============================================================================
# Compute multiply charged ions: HW-2
#===============================================================================
# if multiCharge == 'y':
#     b_ions.extend(compute_multiCharge(b_ions))
#     y_ions.extend(compute_multiCharge(y_ions))

#===============================================================================
# Print final output
#===============================================================================
# for ion in b_ions:
#     print ion
# print "\n" 
# for ion in y_ions:
#     print ion
    
