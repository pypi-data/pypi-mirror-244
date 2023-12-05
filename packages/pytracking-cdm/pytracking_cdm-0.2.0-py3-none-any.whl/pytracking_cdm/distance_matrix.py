"""Functions related to generating a distance matrix."""

from itertools import combinations
import pandas as pd
from weighted_levenshtein import lev
from Levenshtein import distance as fast_lev
from pytracking_cdm.cost_matrix import cost_matrix
import numpy as np
from tqdm import tqdm
from multiprocessing.pool import Pool

def calculate_distance(args):
    i, j, lst, insert_costs, delete_costs, substitute_costs, normalize = args
    if insert_costs is None and delete_costs is None and substitute_costs is None:
        distance =  fast_lev(lst[i], lst[j])
    else:
        distance = lev(lst[i], lst[j], insert_costs=insert_costs, delete_costs=delete_costs, 
                substitute_costs=substitute_costs) 
    if normalize:
        distance = distance / max(len(lst[i]), len(lst[j]))
    return i,j, distance

def distance_matrix(
    df: pd.DataFrame,
    processes: int,
    insert_costs_dct: dict = None,
    delete_costs_dct: dict = None,
    substitute_costs_dct: dict = None,
    code_dct: dict = None,
    normalize: bool = False,
) -> np.ndarray:
    """
    Generate a matrix of Levenshtein distances between sequences.

    Parameters:
    -----------
    df : pd.DataFrame
        pandas DataFrame containing one sequence per row
    processes : int
        Number of processes to use for parallel processing
    insert_costs_dct : dict, optional
        A dictionary specifying the insertion costs, by default None
    delete_costs_dct : dict, optional
        A dictionary specifying the deletion costs, by default None
    substitute_costs_dct : dict, optional
        A dictionary specifying the substitution costs, by default None
    code_dct : dict, optional
        A dictionary for encoding the cost matrix, by default None
    normalize : bool, optional
        Whether to normalize the Levenshtein distance, by default False

    Returns:
    --------
    np.ndarray
        A matrix of Levenshtein distances.
    """
    # Convert sequences to a list
    lst = df.seq.values.tolist()
    n = len(lst)

    # Generate cost matrices
    insert_costs = cost_matrix(1, insert_costs_dct, code_dct)
    delete_costs = cost_matrix(1, delete_costs_dct, code_dct)
    substitute_costs = cost_matrix(2, substitute_costs_dct, code_dct)

     # Create a pool of worker processes
    pool = Pool(processes=processes)
    
    # Prepare arguments for parallel processing. Calc of combinations doesnt include order.
    args_list = [(i, j, lst, insert_costs, delete_costs, substitute_costs, normalize) for (i, j) 
        in combinations(range(n), 2)]

    distances = np.zeros((n, n), dtype=np.float64)

    print("Processes: ", processes)

    # Calculate Levenshtein distances in parallel
    with tqdm(total=len(args_list)) as pbar:
        for i,j, distance in pool.imap(calculate_distance, args_list):
            distances[i, j] = distance
            distances[j, i] = distance
            pbar.update(1)

    pool.close()
    pool.join()

    return distances