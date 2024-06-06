# PubChem
This is a code base to demonstrate how to use API calls to retrieve data from PubChem - the world's largest collection of freely accessible chemical information. The main function includes various API calls, for searching chemicals by name, molecular formula, structure, and other identifiers. The main function is also scalable. You can execute 1, 1000 or even 10000 API calls. Further imporvement will include finding chemical and physical properties, biological activities, safety and toxicity information, patents, literature citations and more.

# Dependencies
This tool needs `requests` and `pandas`. After download this repository, please run the following command line:

```
pip install -r requierments.txt
```

# Tutorials
New users please check the tutorials in the [Notebook](./src/tutorials.ipynb).

# Usage


# Identifiers in PubChem
In PubChem, there are three main identifiers: CID (compound ID number), SID (substrate ID number), and AID (bioassay ID number). A detailed explainatiaon could be found [here](https://www.researchgate.net/publication/282153538_PubChem_Substance_and_Compound_databases/figures?lo=1). In short, CID is the formal identifier for a compound. SID is the identifier of substrates that are tested in a given bioassay. CID is always a pure chemical and SID could be a mixture. Therefore, CID to SID is a one-to-many matching.