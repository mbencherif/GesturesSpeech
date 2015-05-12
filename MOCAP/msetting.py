# coding=utf-8

from MOCAP.mreader import HumanoidUkr
from tools.instruments import Training


def plot_ratio_vs_fps(hand_mode="bothHands", beta=None):
    """
     Plots discriminant ratio VS fps.
    """
    Training(HumanoidUkr).ratio_vs_fps(hand_mode, beta, 1, 120, 2)


def upd_ratio(hand_mode="bothHands", beta=None, fps=None):
    """
     Updates discriminant ratio, w.r.t. hand mode, beta and fps params.
    """
    Training(HumanoidUkr).update_ratio(hand_mode, beta, fps, verbose=True)


def choose_beta(hand_mode="bothHands", fps=None):
    """
     Chooses the best beta (which yields the biggest discriminant ratio R),
     w.r.t. hand mode and fps params.
    """
    Training(HumanoidUkr).choose_beta(hand_mode, fps)


if __name__ == "__main__":
    plot_ratio_vs_fps()
    # FIXME repair fps.png
