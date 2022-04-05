import csv
import sys

from copy import deepcopy

def main():

    if len(sys.argv) != 3:
        print(sys.argv)
        sys.exit("Usage: python tournament.py FILENAME")


    sequence  = []
    with open(sys.argv[2]) as file:
      reader = csv.reader(file)
      for i in reader:
          sequence.append(i)
      sequence = ''.join(sequence[0])
      sequence = ''.join(sequence)
    # print(sequence)

    with open(sys.argv[2]) as file:
        reader = csv.DictReader(file)
        for row in reader:
            pacientes.append(row)

    pacientes = []
    with open(sys.argv[1]) as file:
        reader = csv.DictReader(file)
        for row in reader:
            pacientes.append(row)


    small_keys = [" ","AGATC","AATG","TATC"]
    large_keys = [" ","AGATC","TTTTTTCT","AATG","TCTAG","GATA","TATC","GAAA","TCTG"]
    has_no_match = True
    pa = 0
    if "small" in sys.argv[1]:
        for paciente in pacientes:
            run = []
            new_pac = deepcopy(paciente)
            del new_pac["name"]
            fields = []
            for x in new_pac.values():
                fields.append(int(x))
            for value in range(1,len(paciente)):
                subsequence = small_keys[value]
                run.append(longest_match(sequence, subsequence))
            if(set(run) == set(fields)):
                match = True
                has_no_match = False
                pa = paciente
                break
    elif "large" in sys.argv[1]:
        for paciente in pacientes:
            run = []
            new_pac = deepcopy(paciente)
            del new_pac["name"]
            fields = []
            for x in new_pac.values():
                fields.append(int(x))
            for value in range(1,len(paciente)):
                subsequence = large_keys[value]
                run.append(longest_match(sequence, subsequence))
            if(set(run) == set(fields)):
                match = True
                has_no_match = False
                pa = paciente
                break

    if has_no_match:
        print("No match")
        return
    print(pa["name"])
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
