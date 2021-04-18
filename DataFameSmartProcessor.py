import pandas as pd
import os


class DataFrameSmartProcessor:
    def processDf(self, func, args, inFile, outfile, forceRerun):
        if os.path.isfile(outfile) and (not forceRerun):
            return pd.read_csv(outfile)
        return None
