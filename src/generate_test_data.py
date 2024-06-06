import random
import csv
import os

def generate_random_cid(num):
    """
    Generates random Compound IDs (CIDs) and saves them to a CSV file.
    
    Parameters:
    - num: Number of random CIDs to generate.
    
    Returns:
    - None
    """
    # Generate random CIDs
    random_cids = random.sample(range(1, 10000000), num)

    # Write the CIDs to a CSV file
    output = os.getcwd() + '/../Example/random_cids.csv'  # Output file path
    with open(output, 'w', newline='') as csvfile:
        fieldnames = ['CID']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for cid in random_cids:
            writer.writerow({'CID': cid})

    print("Random CIDs generated and saved to {0}".format(output))

