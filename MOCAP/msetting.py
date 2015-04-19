# coding = utf-8

from MOCAP.mreader import HumanoidUkr
from instruments import Training


if __name__ == "__main__":
    trainInstruments = Training(HumanoidUkr)
    trainInstruments.compute_between_variance(10)
