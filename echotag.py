import numpy as np
import json

# IMPORTANT: x, refs, signals have similar structure [{'raw': [-1 to 1 *], 'label': string}, {...}, ...]

# sample rate for xcorr
rate = 48000
# sampled chirp signal object
x = None
# memoized references(acoustic fingerprint) data, not stored in DB or file for faster execution
g_refs = []

# sampled chirp signal memoized when script is executed
with open('./data/chirp_sampled.json', 'r') as chirp_sampled_file:
    x = json.load(chirp_sampled_file)


def overwriteFingerprints(labeledDataList):
    global g_refs

    g_refs = labeledDataList

    return g_refs


def addFingerprint(labeledData):
    global g_refs

    g_refs.append(labeledData)

    return g_refs


def label(unlabeledDataList):
    global g_refs

    ans = {}
    refs = []
    signals = []

    for ref in g_refs:
        refs.append({"raw": ref.raw, "label": ref.label})

    for unlabeledData in unlabeledDataList:
        signals.append({"raw": unlabeledData.raw})

    # Step 1: Reference creation
    for i in range(len(refs)):
        refs[i]['xcorr'] = np.correlate(refs[i]['raw'], x, mode='full')

        idx = np.argmax(np.abs(refs[i]['xcorr']))
        refs[i]['xcorr'] = refs[i]['xcorr'][idx +
                                            np.arange(-10, int(rate * 0.001))]

        refs[i]['spectrum'] = np.abs(np.fft.fft(refs[i]['raw']))

    # Step 2-1: Feature extraction for test data
    for i in range(len(signals)):
        signals[i]['xcorr'] = np.correlate(signals[i]['raw'], x, mode='full')

        idx = np.argmax(np.abs(signals[i]['xcorr']))
        signals[i]['xcorr'] = signals[i]['xcorr'][idx +
                                                  np.arange(-10, int(rate * 0.001))]

        signals[i]['spectrum'] = np.abs(np.fft.fft(signals[i]['raw']))

    # Step 2-2: Classification
    for i in range(len(signals)):
        max_corr = 0
        signals[i]['label'] = 'None'
        for j in range(len(refs)):
            cur_corr = np.corrcoef(
                signals[i]['spectrum'], refs[j]['spectrum'])[0, 1]
            # Alternatively, you can use the Euclidean distance
            # cur_corr = np.sqrt(np.sum((signals[i]['spectrum'] - ref[j]['spectrum'])**2))

            print(f"{i + 1}: {refs[j]['label']}({cur_corr})")

            if cur_corr > max_corr:
                max_corr = cur_corr
                signals[i]['label'] = refs[j]['label']
                ans[i+1] = {'label': refs[j]['label'], 'corr': max_corr}

    return list(ans.values())
