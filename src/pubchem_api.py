import requests
import pandas as pd
import time

def get_pubchem_data(cids, max_retries=3, delay=0.3, batch_size=1000):
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
                    time.sleep(1)  # Small delay before retrying
            
            if not success:
                print(f"Failed to retrieve data for CID: {cid} after {max_retries} attempts. Returning NA.")
                all_data.append({
                    "CID": cid,
                    "Molecular Formula": 'NA',
                    "Molecular Weight": 'NA',
                    "Canonical SMILES": 'NA',
                    "InChIKey": 'NA'
                })
            
            # Add delay to comply with PubChem's rate limit
            time.sleep(delay)
    
    return all_data

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

def save_to_dataframe(data):
    """
    Converts the list of dictionaries to a Pandas DataFrame.
    
    Parameters:
    - data: List of dictionaries containing the retrieved data.
    
    Returns:
    - df: Pandas DataFrame with the data.
    """
    df = pd.DataFrame(data)
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
