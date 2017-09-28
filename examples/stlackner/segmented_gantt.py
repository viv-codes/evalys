# coding: utf-8

import functools

from evalys.utils import bulksetattr
from evalys.visu import core
from evalys.visu import gantt


class SegmentedGanttVisualization(gantt.GanttVisualization):
    def __init__(self, ax, *, title='Gantt chart'):
        super().__init__(ax, title=title)
        self.labeler = functools.partial(self.merge_labeler, labeler=self.labeler)

    @staticmethod
    def adapt_uniq_num(df):
        unique_numbers = []
        do_annotate = [False] * len(df)

        next_idx = 0
        rows_same_job_map = {}

        # Set the unique id for each job
        for _, row in df.iterrows():
            try:
                cur_idx = int(row['jobID'])
            except KeyError:
                cur_idx = next_idx

            next_idx = cur_idx + 1
            unique_numbers.append(cur_idx)
            rows_same_job_map.setdefault(cur_idx, []).append(row)

        # Annotate the element in the middle of a job series
        for rows in rows_same_job_map.values():
            mid_row = rows[len(rows) // 2]
            do_annotate[mid_row.name] = True

        df['uniq_num'] = unique_numbers
        df['do_annotate'] = do_annotate

    @staticmethod
    def merge_labeler(job, labeler):
        return labeler(job) if job['do_annotate'] else ''


def plot_segmented_gantt(jobset, *, title='Gantt chart', **kwargs):
    layout = core.SimpleLayout(wtitle=title)
    gantt = layout.register(SegmentedGanttVisualization, axkey='all', title=title)
    bulksetattr(gantt, **kwargs)
    gantt.build(jobset)
    layout.show()
