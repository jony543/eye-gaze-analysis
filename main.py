from RawDataReader import RawDataReader
from DataFrameProcessors import StimSizeProcessor, DataEnrichmentProcessor, InOutStimProcessor, PolarCoordinatesProcessor, DominantEyePositionProcessor
from DataFramePipeline import DataFramePipeline
from TrialColorPlot import TrialColorPlot
from sys import platform
import os

screen_resolution = [1920, 1080]

reader = RawDataReader(os.getcwd() + '/raw_data', os.getcwd() + '/raw_data', os.getcwd() + '/processed', False)
pipeline = DataFramePipeline([
    DataEnrichmentProcessor(['screen_w', 'screen_h'], screen_resolution),
    DominantEyePositionProcessor('dominant_eye'),
    PolarCoordinatesProcessor('dominant_x', 'dominant_y'),
    StimSizeProcessor([
        {
            "name": "Snack",
            "id": 2,
            "size": [690, 520]
        },
        {
            "name": "Face",
            "id": 1,
            "size": [400, 500]
        }
    ]),
    InOutStimProcessor('dominant_x', 'dominant_y')
],
os.getcwd() + '/processed', False)

df = reader.readDir()
df = pipeline.process(df)

plotter = TrialColorPlot()
fig = plotter.xy(
    df[df['trial'] == 15],
    os.getcwd() + '/stim/1_1007.jpg',
    screen_resolution)

if 'linux' in platform:
    from gui import TrialPotGui
    gui = TrialPotGui()
    gui.show(fig)

