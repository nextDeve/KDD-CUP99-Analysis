import pandas as pd
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegressionCV
from sklearn import preprocessing
import json, pickle
import numpy as np


def Features():
    features = ['duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes', 'land', 'wrong_fragment',
                'urgent', 'hot', 'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell', 'su_attempted',
                'num_root', 'num_file_creations', 'num_shells', 'num_access_files', 'num_outbound_cmds',
                'is_host_login',
                'is_guest_login', 'count', 'srv_count', 'serror_rate', 'srv_serror_rate', 'rerror_rate',
                'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate', 'srv_diff_host_rate', 'dst_host_count',
                'dst_host_srv_count', 'dst_host_same_srv_rate', 'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
                'dst_host_srv_diff_host_rate', 'dst_host_serror_rate', 'dst_host_srv_serror_rate',
                'dst_host_rerror_rate', 'dst_host_srv_rerror_rate', 'label']
    symbolicFeature = ['protocol_type', 'service', 'flag']
    return features, symbolicFeature


class modeling:
    def __init__(self, data_path):
        self.model = OneVsRestClassifier(
            estimator=LogisticRegressionCV(Cs=10, fit_intercept=True, cv=None, dual=False, penalty='l2', scoring=None,
                                           solver='lbfgs', tol=0.0001, max_iter=10000, class_weight=None, n_jobs=None,
                                           verbose=2, refit=True, intercept_scaling=1.0, multi_class='auto',
                                           random_state=1225, l1_ratios=None))
        self.features, self.symbolic = Features()
        self.data = pd.read_csv(data_path, header=None)
        self.data.columns = self.features
        self.label = None
        self.labelMap = None

    def preprocess(self):
        feature_maps = dict()
        # 将符号特征编码
        for feature in self.symbolic:
            feature_map = dict()
            le = preprocessing.LabelEncoder()
            le.fit(self.data[feature])
            uqi = self.data[feature].unique()
            self.data[feature] = le.transform(self.data[feature])
            reverse = le.transform(uqi)
            for i, v in enumerate(uqi):
                feature_map[v] = str(reverse[i])
            feature_maps[feature] = feature_map
        # 将标签编码
        le = preprocessing.LabelEncoder()
        le.fit(self.data['label'].to_numpy())
        uniq = self.data['label'].unique()
        self.label = le.transform(self.data['label'].to_numpy())
        self.data['label'] = self.label
        reverse = le.transform(uniq)
        feature_map = dict()
        for i, v in enumerate(uniq):
            feature_map[v] = str(reverse[i])
        feature_maps['label'] = feature_map
        self.labelMap = feature_map
        # 保存特征映射信息
        with open("feature_maps.json", 'w', encoding='utf-8') as f:
            json.dump(feature_maps, f, ensure_ascii=False)

    def saveInitState(self):
        normal = self.data[self.data['label'] == int(self.labelMap['normal.'])]
        initState = []
        for feature in self.features[:-1]:
            initState.append(normal[feature].mean())
        np.save('initState', np.array(initState))

    def train(self):
        # 去掉label列
        self.data.drop('label', axis=1, inplace=True)
        # 训练并保存模型
        clt = self.model.fit(self.data.to_numpy(), self.label)
        with open('clt.pickle', 'wb') as f:
            pickle.dump(clt, f)


if __name__ == '__main__':
    data_path = 'kddcup.data_10_percent_corrected'
    modelingObj = modeling(data_path)
    modelingObj.preprocess()
    modelingObj.saveInitState()
    # 训练模型
    modelingObj.train()
