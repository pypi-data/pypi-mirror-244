from __future__ import annotations

from typing import Any, Literal, Optional

import pandas as pd

from retentioneering.backend.tracker import collect_data_performance, time_performance
from retentioneering.data_processor import DataProcessor
from retentioneering.eventstream.types import EventstreamSchemaType
from retentioneering.params_model import ParamsModel
from retentioneering.utils.doc_substitution import docstrings
from retentioneering.utils.hash_object import hash_dataframe


class TruncatePathsParams(ParamsModel):
    """
    A class with parameters for :py:class:`.TruncatePath` class.
    """

    drop_before: Optional[str]
    drop_after: Optional[str]
    occurrence_before: Literal["first", "last"] = "first"
    occurrence_after: Literal["first", "last"] = "first"
    shift_before: int = 0
    shift_after: int = 0


@docstrings.get_sections(base="TruncatePath")  # type: ignore
class TruncatePaths(DataProcessor):
    """
    Remove events that will be deleted from each user's path
    based on the specified event and selected parameters.

    Parameters
    ----------
    drop_before : str, optional
        Event name before which part of the user's path is dropped. The specified event remains in the data.
    drop_after : str, optional
        Event name after which part of the user's path is dropped. The specified event remains in the data.
    occurrence_before : {"first", "last"}, default "first"
        This parameter is necessary when the specified event occurs more than once in one user's path.

        - when set to ``first``, the part of the user path before the first event occurrence is dropped;
        - when set to ``last``, the part of the user path before the last event occurrence is dropped;
    occurrence_after : {"first", "last"}, default "first"
        The same behavior as in the 'occurrence_before', but for the other part of the user path.
    shift_before : int,  default 0
        Sets the number of steps by which the truncate point is shifted from the selected event.
        If the value is negative, then the offset occurs to the left along the timeline.
        If positive, then it occurs to the right.
    shift_after : int,  default 0
        The same behavior as in the ``shift_before``, but for the other part of the user path.

    Returns
    -------
    Eventstream
        ``Eventstream`` with events that should be deleted from input ``eventstream``.


    Notes
    -----
    ``Step`` - is the group of events in the user path with the same timestamp.
    If the user path doesn't contain events from ``drop_before`` and ``drop_after`` parameters, then its
    path does not change.

    See :doc:`Data processors user guide</user_guides/dataprocessors>` for the details.
    """

    params: TruncatePathsParams

    @time_performance(
        scope="truncate_paths",
        event_name="init",
    )
    def __init__(self, params: TruncatePathsParams):
        super().__init__(params=params)

    @time_performance(
        scope="truncate_paths",
        event_name="apply",
    )
    def apply(self, df: pd.DataFrame, schema: EventstreamSchemaType) -> pd.DataFrame:
        source = df.copy()

        user_col = schema.user_id
        time_col = schema.event_timestamp
        event_col = schema.event_name
        event_id = schema.event_id

        drop_before = self.params.drop_before
        drop_after = self.params.drop_after
        occurrence_before = self.params.occurrence_before
        occurrence_after = self.params.occurrence_after
        shift_before = self.params.shift_before
        shift_after = self.params.shift_after

        params_data: list[Any] = []

        if not drop_after and not drop_before:
            raise Exception("Either drop_before or drop_after must be specified!")

        if drop_before:
            before: list[str | list[str | int | None]] | None = [
                drop_before,
                ["before", occurrence_before, shift_before],
            ]
            params_data.append(before)

        if drop_after:
            after: list[str | list[str | int | None]] | None = [drop_after, ["after", occurrence_after, shift_after]]
            params_data.append(after)

        for truncate_type in params_data:
            col_mark, occurrence, shift = truncate_type[1]

            if truncate_type[0]:
                mask_events = df[event_col] == truncate_type[0]
                df[f"{col_mark}_mark_target"] = mask_events.astype(int)
                df[f"{col_mark}_mark_target"] = df.groupby([user_col, time_col])[f"{col_mark}_mark_target"].transform(
                    max
                )
                if occurrence == "last":
                    df[f"{col_mark}_cumsum"] = df.iloc[::-1].groupby([user_col])[f"{col_mark}_mark_target"].cumsum()
                if occurrence == "first":
                    df[f"{col_mark}_cumsum"] = df.groupby([user_col])[f"{col_mark}_mark_target"].cumsum()

                def count_groups(x: pd.DataFrame) -> int:
                    return x.to_frame(name=time_col).groupby(time_col).ngroup()  # type: ignore

                df[f"{col_mark}_group_num_in_user"] = df.groupby([user_col], group_keys=False)[time_col].transform(
                    count_groups
                )

                if occurrence == "last":
                    df_groups = (
                        df[df[f"{col_mark}_cumsum"] == 1]
                        .groupby([user_col])[f"{col_mark}_group_num_in_user"]
                        .max()
                        .rename(f"{col_mark}_group_centered")
                        .reset_index()
                    )
                else:
                    df_groups = (
                        df[df[f"{col_mark}_cumsum"] == 1]
                        .groupby([user_col])[f"{col_mark}_group_num_in_user"]
                        .min()
                        .rename(f"{col_mark}_group_centered")
                        .reset_index()
                    )

                df = df.merge(df_groups)
                df[f"{col_mark}_group_centered"] = (
                    df[f"{col_mark}_group_num_in_user"] - df[f"{col_mark}_group_centered"] - shift
                )

        if all(col in df.columns for col in ["before_group_centered", "after_group_centered"]):
            df = df[(df["before_group_centered"] < 0) | (df["after_group_centered"] > 0)]
        elif df.columns[-1] == "before_group_centered":
            df = df[df["before_group_centered"] < 0]
        elif df.columns[-1] == "after_group_centered":
            df = df[df["after_group_centered"] > 0]

        df = df.reset_index()

        updated = source
        if not df.empty:
            updated = source[~source[event_id].isin(df[event_id])]

        collect_data_performance(
            scope="truncate_paths",
            event_name="metadata",
            called_params=self.to_dict()["values"],
            not_hash_values=["occurrence_before", "occurrence_after"],
            performance_data={
                "parent": {
                    "shape": source.shape,
                    "hash": hash_dataframe(source),
                },
                "child": {
                    "shape": updated.shape,
                    "hash": hash_dataframe(updated),
                },
            },
        )

        return updated
