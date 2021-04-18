import pandas as pd
import os
import glob
import time
import datetime


class RawDataReader:
    def __init__(self, eyeTrackerDir, trialDataDir, outDir, forceReread):
        self.eyeTrackerDir = self.makedir(eyeTrackerDir)
        self.trialDataDir = self.makedir(trialDataDir)
        self.outDir = self.makedir(outDir)
        self.forceReread = forceReread

    def makedir(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)
        return dir

    def timestamp(self):
        return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    def readDir(self):
        dfs = []

        for ascFile in glob.glob(self.eyeTrackerDir + '//*asc'):
            ascFileName = os.path.basename(ascFile)

            subjectId = int(ascFileName.split('_')[0])
            print('{}: Reading subject {} data'.format(self.timestamp(), subjectId))

            txtFileName = glob.glob(self.trialDataDir + '//*' + str(subjectId) + '_Scale' + '*txt')[0]
            txtFilePersonalDataName = \
            glob.glob(self.trialDataDir + '//*' + str(subjectId) + '_personalDetails' + '*txt')[0]

            outFile = self.outDir + "/{}_data.csv".format(subjectId)

            dfs.append(self.readSubject(ascFile, txtFileName, txtFilePersonalDataName, outFile))

            print('{}: Finished reading subject {} data'.format(self.timestamp(), subjectId))

        return pd.concat(dfs)

    def readSubject(self, eyeTrackerFile, trialsFile, personalDataFile, outfile):
        if os.path.isfile(outfile) and (not self.forceReread):
           return pd.read_csv(outfile) #, dtype={"timestamp": "int", "rx": "float", "ry": "float", "lx": "float", "ly": "float"})

        txtData = pd.read_table(trialsFile)

        df = pd.read_csv(eyeTrackerFile, sep='\t', names=[0, 1, 2, 3, 4, 5, 6], skip_blank_lines=False)
        trialStartPoints = df[df[1].str.contains('TrialStart') & ~df[1].isna()]
        trialEndPoints = df[df[1].str.contains('ScaleStart') & ~df[1].isna()]

        df.columns = ['timestamp', 'lx', 'ly', 'l_pupil', 'rx', 'ry', 'r_pupil']

        i = 0
        for startIndex, row in trialStartPoints.iterrows():
            endIndex = trialEndPoints[i:(i + 1)].index[0]
            df.loc[(startIndex + 1):(endIndex - 1), 'trial'] = i + 1
            i += 1

        # convert all values from .asc file to numeric
        df = df.apply(pd.to_numeric, args=('coerce', 'float'))

        # remove rows that don't belong to any trial or that timestamp is illegal
        df.drop(df[df['trial'].isna() | df['timestamp'].isna()].index, inplace=True)

        mergeData = pd.merge(txtData, df, on='trial')

        txtpersonalData = pd.read_table(personalDataFile)
        dominant_eye = txtpersonalData['dominant eye (1-right, 2-left)'].values[0]
        if dominant_eye == 1:
            mergeData['dominant_eye'] = 'R'
        else:
            mergeData['dominant_eye'] = 'L'

        mergeData.to_csv(outfile, index=False)

        return mergeData
