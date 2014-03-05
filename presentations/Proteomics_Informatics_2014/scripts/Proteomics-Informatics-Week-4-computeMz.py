
## Compute m/z for a peptide with a given charge state

## Constants, parameters etc.
monoMassAA = {'G':57.02146360, 'A':71.03711360, 'S':87.03202820, 'P':97.05276360,
              'V':99.06841360, 'T':101.0476782, 'C':103.0091854, 'L':113.0840636,
              'I':113.0840636, 'N':114.0429272, 'D':115.0269428, 'Q':128.0585772,
              'K':128.0949626, 'E':129.0425928, 'M':131.0404854, 'H':137.0589116,
              'F':147.0684136, 'R':156.1011106, 'Y':163.0633282, 'W' : 186.0793126
              }
mw_h2o = 18.010564684
mw_h = 1.00728

## User input
z = 2
seq = "PEPTIDE"

## Data processing
mass = 0   ## running mass of the peptide

# Step 1: Scan the seq character by character using for loop
#         At each iteration, add mass of current character/AA to the running mass

# Step 2: Add mass of (H+OH) or water

# Step 3: Compute (and store in a variable) m/z for the given charge-state: (mass + z*mw_h)/z

# Step 4: print "Seq: %s\tz: %d\tm/z: %f"%(seq, z, mz)

