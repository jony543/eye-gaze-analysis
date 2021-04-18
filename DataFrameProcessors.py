import numpy as np


class DataFrameProcessor:
    def __init__(self, name, columns):
        self.name = name
        self.columns = columns

    def process_df(self, df):
        raise NotImplementedError("Please Implement this method")


class DataEnrichmentProcessor(DataFrameProcessor):
    def __init__(self, col, val):
        super().__init__(type(self).__name__, [col])
        if isinstance(col, list):
            self.col = col
            self.val = val
        else:
            self.col = [col]
            self.val = [val]

    def process_df(self, df):
        for i, c in enumerate(self.col):
            df[c] = self.val[i]


class StimSizeProcessor(DataFrameProcessor):
    def __init__(self, stimArray):
        super().__init__(type(self).__name__, ['stim_h', 'stim_w'])
        self.stimuli = {s['id']: s for s in stimArray}

    def process_df(self, df):
        for stimId in self.stimuli:
            df.loc[df["StimTypeInd"] == stimId, "stim_h"] = self.stimuli[stimId]['size'][0]
            df.loc[df["StimTypeInd"] == stimId, "stim_w"] = self.stimuli[stimId]['size'][1]


class PolarCoordinatesProcessor(DataFrameProcessor):
    def __init__(self, x_col, y_col):
        super().__init__(type(self).__name__, ['alpha', 'radius'])
        self.x_col = x_col
        self.y_col = y_col

    def process_df(self, df):
        df["radius"] = np.sqrt(
            (df[self.x_col] - df['screen_w'] / 2) ** 2 + (df[self.y_col] - df['screen_h'] / 2) ** 2
        )
        df["alpha"] = np.arctan2(df[self.y_col] - df['screen_h'], df[self.x_col] - df['screen_w'])


class DominantEyePositionProcessor(DataFrameProcessor):
    def __init__(self, column):
        super().__init__(type(self).__name__, ['dominant_x', 'dominant_y'])
        self.column = column

    def process_df(self, df):
        df.loc[df[self.column] == 'R', 'dominant_x'] = df.loc[df[self.column] == 'R', 'rx']
        df.loc[df[self.column] == 'R', 'dominant_y'] = df.loc[df[self.column] == 'R', 'ry']

        df.loc[df[self.column] == 'L', 'dominant_x'] = df.loc[df[self.column] == 'L', 'lx']
        df.loc[df[self.column] == 'L', 'dominant_y'] = df.loc[df[self.column] == 'L', 'ly']


class InOutStimProcessor(DataFrameProcessor):
    def __init__(self, x_col, y_col):
        super().__init__(type(self).__name__, ['in_stim'])
        self.x_col = x_col
        self.y_col = y_col

    def process_df(self, df):
        x0 = (df['screen_w'] - df['stim_w']) / 2
        x1 = df['screen_w'] - x0

        y0 = (df['screen_h'] - df['stim_h']) / 2
        y1 = df['screen_h'] - y0

        df['in'] = 0

        df.loc[(df[self.x_col] > x0) & (df[self.x_col] < x1) &
               (df[self.y_col] > y0) & (df[self.y_col] < y1),
               'in'] = 1
