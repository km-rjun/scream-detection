import numpy as np


def tetsting_unit(filename):
    tester = []
    import librosa
    test, ans = librosa.load(filename)  # provide path of  wave file
    mfccs = np.mean(librosa.feature.mfcc(test, ans, n_mfcc=40).T, axis=0)
    tester.append(mfccs)
    tester = np.array(tester)
    return tester #return Mfcss extracted arrray 

def svm_process(filename):
    import pickle  # importing pickle to load saved model

    load_model = pickle.load(open('svm_based_model/phase1_model.sav', 'rb'))  # loading phase_1 model (noise vs speech)
    result = load_model.predict(tetsting_unit(filename))  # predicting if result[0]==1 then noise else human sound
    load_model2 = pickle.load(open('svm_based_model/phase2_model.sav', 'rb'))  # loading phase2 model
    if result[0] == 2:  # checking sound noise or human
        print("Phase-1 clear")
        ok = load_model2.predict(tetsting_unit(filename))  # using second phase_model
        if ok[0] == 1:
            # print("Phase-2 clear")
            # print('Scream')
            return True
        else:
            # print('speech')
            return False
    else:
        # print("noise")
        return "Noise"


