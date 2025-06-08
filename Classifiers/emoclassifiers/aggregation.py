from math import comb
from typing import Any

from Classifiers.emoclassifiers.classification import YesNoUnsureEnum



class Aggregator:

    @classmethod
    def aggregate(cls, results: dict[str, YesNoUnsureEnum]) -> Any:
        """
        Aggregate classification results for a conversation.
        """
        raise NotImplementedError("Subclass must implement this method")



class RawAggregator(Aggregator):

    @classmethod
    def aggregate(cls, results: dict[str, YesNoUnsureEnum]) -> bool:
        return {
            k: val == YesNoUnsureEnum.YES
            for k, val in results.items()
        }


class AnyAggregator(Aggregator):

    @classmethod
    def aggregate(cls, results: dict[str, YesNoUnsureEnum]) -> bool:
        return any(val == YesNoUnsureEnum.YES for val in results.values())


class AdjustedAggregator(Aggregator):

    @classmethod
    def aggregate(cls, results: dict[str, YesNoUnsureEnum], avg_num_chunks: int = 20) -> float:
        elems = results.values()
        num_elems = len(elems)
        if avg_num_chunks <= 0:
            raise ValueError(f"avg_num_chunks must be positive")

        # Calculate the number of True values in elems
        num_true = sum(elem == YesNoUnsureEnum.YES for elem in elems)
        num_false = num_elems - num_true

        # Handle the case where the sample size exceeds the total number of elements
        if avg_num_chunks > num_elems:
            # If there's at least one True in the entire list, any() will return True
            # since all elements are sampled. Otherwise, it returns False.
            return 1.0 if num_true > 0 else 0.0

        # Handle special cases
        if num_true == 0:
            return 0.0  # All elements are False

        # Calculate the probability that all sampled elements are False
        if num_false < avg_num_chunks:
            # Impossible to sample all False if there are fewer than k False
            prob_all_false = 0.0
        else:
            combinations_all_false = comb(num_false, avg_num_chunks)
            total_combinations = comb(num_elems, avg_num_chunks)
            prob_all_false = combinations_all_false / total_combinations

        # The expected value is the probability that at least one sampled element is True
        expected_value = 1.0 - prob_all_false
        return expected_value


AGGREGATOR_DICT = {
    "raw": RawAggregator,
    "any": AnyAggregator,
    "adjusted": AdjustedAggregator,
}
