import numpy as np
import json

# IMPORTANT: x, refs, signals have similar structure [{'raw': [-1 to 1 *], 'label': string}, {...}, ...]

# sample rate for xcorr
rate = 48000
# sampled chirp signal object
x = None
# memoized references(acoustic fingerprint) data, not stored in DB or file for faster execution
refs = []

# sampled chirp signal memoized when script is executed
with open('./data/chirp_sampled.json', 'r') as chirp_sampled_file:
    x = json.load(chirp_sampled_file)


def overwriteFingerprints(labeledDataList):
    global refs

    for labeledData in labeledDataList:
        refs.append({"raw": labeledData.raw, "label": labeledData.label})

    return refs


def addFingerprint(labeledData):
    global refs

    refs.append({"raw": labeledData.raw, "label": labeledData.label})

    return refs


def removeFingerprint(label):
    global refs

    for i in range(len(refs)):
        if refs[i].label == label:
            refs.pop(i)
            break


def label(unlabeledData):
    global refs

    ans = None
    signal = {"raw": unlabeledData.raw}

    # Step 1: Reference creation
    for i in range(len(refs)):
        refs[i]['xcorr'] = np.correlate(refs[i]['raw'], x, mode='full')

        idx = np.argmax(np.abs(refs[i]['xcorr']))
        refs[i]['xcorr'] = refs[i]['xcorr'][idx +
                                            np.arange(-10, int(rate * 0.001))]

        refs[i]['spectrum'] = np.abs(np.fft.fft(refs[i]['raw']))

    # Step 2-1: Feature extraction for test data
    signal['xcorr'] = np.correlate(signal['raw'], x, mode='full')

    idx = np.argmax(np.abs(signal['xcorr']))
    signal['xcorr'] = signal['xcorr'][idx +
                                      np.arange(-10, int(rate * 0.001))]

    signal['spectrum'] = np.abs(np.fft.fft(signal['raw']))

    # Step 2-2: Classification
    max_corr = 0
    signal['label'] = 'None'
    for j in range(len(refs)):
        cur_corr = np.corrcoef(
            signal['spectrum'], refs[j]['spectrum'])[0, 1]

        if cur_corr > max_corr:
            max_corr = cur_corr
            signal['label'] = refs[j]['label']
            ans = {'label': refs[j]['label'], 'corr': max_corr}

    return ans
