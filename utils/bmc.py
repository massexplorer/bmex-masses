import numpy as np
import pandas as pd
from pybmc.bmc import BayesianModelCombination
from pybmc.data import Dataset
from utils.dropdown_options import dataset_options



def BMC(quantity, data_source="db"):
    """
    Runs the full BMC workflow for a given quantity.

    Parameters:
    - quantity (str): Property to predict ('BE', 'ChRad', etc.)
    - even_even (bool): Filter only even-even nuclei
    - data_source (str): HDF5 file containing model data

    Returns:
    - DataFrame with columns ['N', 'Z', 'Predicted_Median'] + uncertainty bounds
    """
    print("BMC CALLED")
    # Step 1: Get valid model names for this quantity
    model_options = dataset_options(quantity)
    models = [
        entry['value'] for entry in model_options
        if not entry.get('disabled', False) and entry['value'] not in ['BayesianModelCombination']
    ]

    # Step 2: Load data
    dataset = Dataset(data_source=data_source)
    data_dict = dataset.load_data(models=models, keys=[quantity],domain_keys=["Z", "N"])

    # Step 5: Split data for training
    train_data, _, _ = dataset.split_data(
    data_dict=data_dict,
    property_name=quantity,
    splitting_algorithm="random",
    train_size=0.7,
    val_size=0.15,
    test_size=0.15,
)

    # Step 6: Create BMC instance
    bmc = BayesianModelCombination(
        models_list=models,
        data_dict=data_dict,
        truth_column_name="AME2020"
    )
    clean_train = train_data.dropna(subset=models, how="any") # From train_data, remove any row where at least one of the listed models has a NaN value.    

    # Step 7: Orthogonalize and Train
    bmc.orthogonalize(quantity, train_df=clean_train, components_kept = 3)
    bmc.train()

    # Step 8: Predict
    _, lower_df, median_df, upper_df = bmc.predict2(quantity)

    # Step 9: Merge outputs
    out = median_df.copy()
    out[quantity] = out["Predicted_Median"]
    out["Predicted_Lower"] = lower_df["Predicted_Lower"]
    out["Predicted_Upper"] = upper_df["Predicted_Upper"]
    out = out.drop(columns=["Predicted_Median"])
    # coverage_results = bmc.evaluate()
    with pd.HDFStore(data_source) as store:
        store.put("BayesianModelCombination", out, format="table", data_columns=True)
        store.put("BayesianModelCombination_models", pd.Series(models))
        # store.put("BayesianModelCombination_coverage", pd.Series(coverage_results))

    return out, models#, coverage_results



