"""Main module of this package containing the definition of the SeqAnaObj Class."""

from pytracking_cdm.sequencer import sequencer
from pytracking_cdm.distance_matrix import distance_matrix
import pandas as pd
import multiprocessing
import numpy as np


class SeqAnaObj:
    """Main class of this package whose init executes the processing pipeline.

    Transforms a folder containing fixation data to sequences and then to a matrix of levenshtein distances.

    Args:
        folder: Input folder containing files of rowise fixations as csv per individual or trial.
        id_col: Name of the column containing the unique id of the individual or trial.
        aoi_col: Name of the column containing the AOI labels.
        off_aoi_str: Exclude the AOIs with this label when generating the sequences. This is usually the label for a 
            fixation that's not on an area of interest.
        sep_col: A column that contains some category (for example trials) that should be treated as separate sequences.
        merge: Merge contiguous identical strings.
        normalize: Optionally normalize the levenshtein distance by dividing the distance between two strings by the 
            length of the longer string
        insert_costs_dct: A dictionary like this: {'label_one': 2}. A string as key and a insertion cost as value.
        delete_costs_dct: A dictionary like this: {'label_one': 2}. A string as key and a deletion cost as value.
        substitute_costs_dct: A dictionary like this: {'label_one': {"label_two": 1.25}}. The top level dictionary 
            should contain the AOI labels as keys and dictionaries as values. The nested dictionaries should contain the
            aoi label to substitute as their keys and the cost of substitution as their values.
        threads: Number of threads to use for multiprocessing. Multiprocessing is use for computing the distance
            matrix. By default, the number of threads is set to the number of CPUs.
    """
    def __init__(
        self,
        folder: str,
        id_col: str,
        aoi_col: str,
        off_aoi_str: str = None,
        sep_col: str = None,
        merge: bool = False,
        normalize: bool = False,
        insert_costs_dct: dict = None,
        delete_costs_dct: dict = None,
        substitute_costs_dct: dict = None,
        processes: int = None,
    ):
        print("\n Converting files to sequences... \n")
        temp = sequencer(
            folder=folder, id_col=id_col, aoi_col=aoi_col, off_aoi_str=off_aoi_str, sep_col=sep_col, merge=merge
        )

        self._seq_df: pd.DataFrame = temp[0]
        self._code_dct: dict = temp[1]
        print("\n Generating distance matrix... \n")
        if processes is None:
            processes = multiprocessing.cpu_count()
        self._distance_matrix: np.ndarray = distance_matrix(
            self._seq_df,   
            processes=processes,
            insert_costs_dct=insert_costs_dct,
            delete_costs_dct=delete_costs_dct,
            substitute_costs_dct=substitute_costs_dct,
            code_dct=self.code_dct,
            normalize=normalize,
        )
    
    @property
    def seq_df(self) -> pd.DataFrame:
        """Dataframe of one sequence per row per individual or trial, depending on params."""
        return self._seq_df
    
    @property
    def code_dct(self) -> dict:
        """Dictionary with the AOI labels as keys and their encoded sequence chars as values."""
        return self._code_dct
    
    @property
    def distance_matrix(self) -> np.ndarray:
        """A matrix of levenshtein distances.."""
        return self._distance_matrix
