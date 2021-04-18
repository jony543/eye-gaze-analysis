import pandas as pd
import os


class DataFramePipeline:
    def __init__(self, processors, outDir, forceRecalculate, resultFormat="csv"):
        self.processors = processors
        self.outDir = outDir
        self.forceRecalculate = forceRecalculate
        self.resultFormat = resultFormat

    def process(self, df):
        outFile = self.outDir + "/processed." + self.resultFormat
        print('starting DF pipeline to file: ' + outFile)

        if os.path.isfile(outFile) and (not self.forceRecalculate):
            print('reusing existing file')
            df = pd.read_csv(outFile)

        for p in self.processors:
            print('processing ' + p.name)
            if not all((c in df.columns.values) for c in p.columns):
                p.process_df(df)
            print('finished processing ' + p.name)

        df.to_csv(outFile, index=False)

        print('finished DF pipeline')

        return df
