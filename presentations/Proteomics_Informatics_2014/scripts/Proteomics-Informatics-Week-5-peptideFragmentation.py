
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
#     a. User input at cmd prompt
#     b. more complex storage data structures (list of dictionaries); 'value' in dict key-value pairs as a computation
#     c. more complex operations and logic
#     d. 'ipdb' library to explore code
#     e. Combining 'if' block with 'for' loop for more complex branching/looping (HW-2)
#     f. embedded for loops (multiply charged ions)
#===============================================================================

# import ipdb         ## Interactive Python debugger. Also useful for exploring code.
# ipdb.set_trace()    ## If it is not available, install it from system cmd prompt: $pip install ipdb  

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

#===============================================================================
# User input
#===============================================================================
pepseq = "DGHTNNLRPK"   
z_pep = 2
neutralLoss = "n"
multiCharge = "n"
# pepseq = raw_input("Enter peptide sequence: ")    ## raw_input(): function to accept raw keyboard input
# z_pep = int(raw_input("Enter charge state: "))
# neutralLoss = raw_input("Neutral losses [Enter choice: y(yes) or n(no)]: ")
# multiCharge = raw_input("Multiply charged ions [Enter choice: y(yes) or n(no)]: ")
       

#===============================================================================
# Computations
#===============================================================================

## Peptide mass
pepmass = 0   ## running mass of the peptide
for aa in pepseq:
    pepmass = pepmass + monoMassAA[aa]
pepmass = pepmass + m_h2o  ## monoMassAA excludes N-terminal 'H' & C-terminal 'OH'

#===============================================================================
# Compute fragment ion m/z values (first, only singly charged ions, i.e. z=1)
#===============================================================================
b_ions = []
y_ions = []
b_currentValue = m_proton    ## Adding a proton mass to residue mass (Remember: lecture from de novo sequencing; Add 1 to 1st b-ion and 19 to 1st y-ion)
for index in xrange(len(pepseq)-1):
    ## b-ions
    b_mz = b_currentValue + monoMassAA[pepseq[index]]
    b_pos = index + 1           ## In the domain, ion position starts from 1, but in python str/list index starts from 0 
    b_seq = pepseq[:index+1]    ## Slicing operation on "character strings" (str)
    b_ions.append({'type': 'b', 'pos': b_pos, 'seq': b_seq, 'z': 1, 'mz': b_mz})
        
    ## y-ions
    y_mz = pepmass - b_mz + 2*m_proton  ## y-ions need extra 19 adjustment (H + OH + proton); pepmass already has H+OH, but b_mz removes 1 proton... plus we need to add one proton for the y-ion, hence add 2*m_proton  
    y_pos = len(pepseq) - b_pos
    y_seq = pepseq[index+1:]
    y_ions.append({'type': 'y', 'pos': y_pos, 'seq': y_seq, 'z': 1, 'mz': y_mz})
    
    ## Update current value for next iteration
    b_currentValue = b_mz


#===============================================================================
# Compute Neutral Losses:
#===============================================================================
if neutralLoss == 'y':
    # b-ions neutral h2o loss (only if there is an S/T/E/D in the fragment sequence)
    b_ions_neutralLoss = []
    for b_ion in b_ions:
        if 'S' in b_ion['seq'] or 'T' in b_ion['seq'] or 'E' in b_ion['seq'] or 'D' in b_ion['seq']:
            b_minus_h2o_mz = b_ion['mz'] - m_h2o ## charge state = 1; o.w. (b_mz*z - m_h2o)/z
            b_ions_neutralLoss.append({'type': 'b-h2o', 'pos': b_ion['pos'], 'seq': b_ion['seq'], 'z': b_ion['z'], 'mz': b_minus_h2o_mz})
    
        ## HW-2: Add b-ions neutral nh3 loss (another "if" block within the same for loop)
        ##          -> nh3 loss occurs only if there is R/K/N/Q in the fragment sequence                                  
    
    b_ions.extend(b_ions_neutralLoss)   ## Chk documentation of this function from ipython (list.extend?? or b_ions.extend??)
    
    
    ## HW-2: Add y-ions neutral h2o & nh3 losses (new "for loop" for y ions, with 2 if blocsk)
    ## Remember that a "statement block" in python is marked using indentation
    y_ions_neutralLoss = []

    y_ions.extend(y_ions_neutralLoss)



#===============================================================================
# Compute multiply charged ions
#===============================================================================
if multiCharge == 'y':
    ## multiply charged b-ions
    b_ions_multiCharge = []
    ## For each ion, compute higher charge states and add the new ion to the above list 
    for b_ion in b_ions:
        for curr_charge in range(2, z_pep+1): 
            b_ion_multiCharge_mz = (b_ion['mz']*b_ion['z'] + (curr_charge-1)*m_proton)/curr_charge
            b_ions_multiCharge.append({'type': 'b+', 'pos': b_ion['pos'], 'seq': b_ion['seq'], 'z': curr_charge, 'mz': b_ion_multiCharge_mz})
        
    b_ions.extend(b_ions_multiCharge)
    
    ## HW-2: multiply charged y-ions
    y_ions_multiCharge = []
    
    y_ions.extend(y_ions_multiCharge)


#===============================================================================
# Print final output
#===============================================================================
# for ion in b_ions:
#     print ion
# print "\n" 
# for ion in y_ions:
#     print ion
    
