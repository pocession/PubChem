import requests
import pandas as pd
import time
import os

def get_pubchem_data(cids, max_retries=3, delay=0.4, batch_size=1000):
    """
    Fetches molecular properties from PubChem for a list of CIDs in batches.
    
    Parameters:
    - cids: List of PubChem CIDs (Chemical IDs).
    - max_retries: Maximum number of retries for API calls.
    - delay: Delay in seconds between consecutive API calls to comply with rate limits.
    - batch_size: Number of CIDs to process in each batch.
    
    Returns:
    - all_data: List of dictionaries containing the retrieved data.
    """
    base_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{}/property/MolecularFormula,MolecularWeight,CanonicalSMILES,InChIKey/JSON"
    all_data = []

    # Generate batches of CIDs
    batches = generate_batches(cids, batch_size)
    
    for batch_index, batch in enumerate(batches):
        print(f"Processing batch {batch_index + 1} with {len(batch)} compounds...")
        
        for cid in batch:
            success = False
            for attempt in range(max_retries):
                try:
                    response = requests.get(base_url.format(cid))

                    if response.status_code == 200:
                        data = response.json()
                        properties = data['PropertyTable']['Properties'][0]
                        all_data.append({
                            "CID": cid,
                            "Molecular Formula": properties.get('MolecularFormula'),
                            "Molecular Weight": properties.get('MolecularWeight'),
                            "Canonical SMILES": properties.get('CanonicalSMILES'),
                            "InChIKey": properties.get('InChIKey')
                        })
                        success = True
                        break
                    else:
                        print(f"Attempt {attempt + 1} failed for CID: {cid}. Retrying...")
                        time.sleep(delay)  # Small delay before retrying
                except requests.ConnectionError as e:
                    print(f"Connection error for CID: {cid}, attempt {attempt + 1}. Retrying...")
                    time.sleep(delay)
                except Exception as e:
                    print(f"An error occurred for CID: {cid}: {e}")
                    break  # Exit the retry loop on unexpected errors
            
            if not success:
                print(f"Failed to retrieve data for CID: {cid} after {max_retries} attempts. Returning NA.")
                all_data.append({
                    "CID": cid,
                    "Molecular Formula": 'NA',
                    "Molecular Weight": 'NA',
                    "Canonical SMILES": 'NA',
                    "InChIKey": 'NA'
                })
                time.sleep(delay)
            
    return all_data

def get_pubchem_bioassay_data(cids, aid, max_retries=3, delay=0.3, batch_size=1000):
    """
    Fetches bioassay data from PubChem for a list of CIDs and a single AID in batches.
    
    Parameters:
    - cids: List of PubChem CIDs (Chemical IDs).
    - aid: PubChem AID (Assay ID).
    - max_retries: Maximum number of retries for API calls.
    - delay: Delay in seconds between consecutive API calls to comply with rate limits.
    - batch_size: Number of CIDs to process in each batch.
    
    Returns:
    - all_data: List of dictionaries containing the retrieved data.
    """
    base_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/{}/CSV?cid={}"
    all_data = []

    # Generate batches of CIDs
    cid_batches = generate_batches(cids, batch_size)
    
    for batch_index, batch in enumerate(cid_batches):
        print(f"Processing batch {batch_index + 1} for AID {aid} with {len(batch)} compounds...")
        
        for cid in batch:
            success = False
            for attempt in range(max_retries):
                try:
                    response = requests.get(base_url.format(aid, cid))

                    if response.status_code == 200:
                        data = response.text
                        parsed_data = parse_bioassay_data(data, cid)
                        all_data.append(parsed_data)
                        success = True
                        break
                    else:
                        print(f"Attempt {attempt + 1} failed for AID: {aid}, CID: {cid}. Retrying...")
                        time.sleep(delay)  # Small delay before retrying
                except requests.ConnectionError as e:
                        print(f"Connection error for AID: {aid}, CID: {cid}, attempt {attempt + 1}. Retrying...")
                        time.sleep(delay)
                except Exception as e:
                        print(f"An error occurred for AID: {aid}, CID: {cid}: {e}")
                        break  # Exit the retry loop on unexpected errors
            
            if not success:
                print(f"Failed to retrieve data for AID: {aid}, CID: {cid} after {max_retries} attempts. Returning NA.")
                all_data.append({
                    "AID": aid,
                    "CID": cid,
                    "Data": 'NA'
                })
                time.sleep(delay)
                
    return all_data

def parse_bioassay_data(raw_data, cid):
    """
    Parses the raw bioassay data and extracts the 9th and 10th columns.

    Parameters:
    - raw_data: The raw bioassay data as a string.
    - cid: The CID associated with the bioassay data.

    Returns:
    - A dictionary containing the extracted data.
    """
    lines = raw_data.strip().split('\n')
    header = lines[0].split(',')
    data = lines[3].split(',')

    # Extract the 9th and 10th columns
    mean = data[8]
    stddev = data[9]

    return {
        "CID": cid,
        header[8]: mean,
        header[9]: stddev
    }

def generate_batches(data, batch_size):
    """
    Generates batches from the input list.
    
    Parameters:
    - data: List of items to be batched.
    - batch_size: Number of items per batch.
    
    Returns:
    - List of batches, where each batch is a list of items.
    """
    return [data[i:i + batch_size] for i in range(0, len(data), batch_size)]

def save_to_dataframe(data, output_file=None):
    """
    Converts the list of dictionaries to a Pandas DataFrame and saves it to a CSV file.
    
    Parameters:
    - data: List of dictionaries containing the retrieved data.
    - output_file: Path to the output CSV file. If None, the DataFrame will be saved to 'pubchem_data.csv' in the current directory.
    
    Returns:
    - output_file: Path to the output CSV file.
    """
    df = pd.DataFrame(data)

    if output_file is None:
        output_file = os.getcwd() + "/../Example/pubchem_data.csv"

    df.to_csv(output_file, index=False)
    print(f"DataFrame saved to CSV file: {output_file}")
    return df

def read_cids_from_csv(file_path):
    """
    Reads a list of CIDs from a CSV file.
    
    Parameters:
    - file_path: Path to the CSV file containing CIDs.
    
    Returns:
    - List of CIDs.
    
    Raises:
    - ValueError: If the CSV file does not contain a 'CID' column.
    """
    df = pd.read_csv(file_path)
    if 'CID' in df.columns:
        return df['CID'].tolist()
    else:
        raise ValueError("CSV file must contain a 'CID' column")
