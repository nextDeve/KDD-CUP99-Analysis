from django.shortcuts import render
import pickle
import numpy as np
from django.http import HttpResponse, JsonResponse
import json, re
import pandas as pd
import warnings

warnings.filterwarnings('ignore')
feature_list = ['duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes', 'land', 'wrong_fragment',
                'urgent', 'hot', 'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell', 'su_attempted',
                'num_root', 'num_file_creations', 'num_shells', 'num_access_files', 'num_outbound_cmds',
                'is_host_login', 'is_guest_login', 'count', 'srv_count', 'serror_rate', 'srv_serror_rate',
                'rerror_rate', 'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate', 'srv_diff_host_rate',
                'dst_host_count', 'dst_host_srv_count', 'dst_host_same_srv_rate', 'dst_host_diff_srv_rate',
                'dst_host_same_src_port_rate', 'dst_host_srv_diff_host_rate', 'dst_host_serror_rate',
                'dst_host_srv_serror_rate', 'dst_host_rerror_rate', 'dst_host_srv_rerror_rate']

symbolicFeature = ['protocol_type', 'service', 'flag']
with open('model/feature_maps.json') as f:
    feature_map = json.load(f)
label_dic = {
    "11": "normal.",
    "1": "buffer_overflow.",
    "7": "loadmodule.",
    "12": "perl.",
    "9": "neptune.",
    "18": "smurf.",
    "3": "guess_passwd.",
    "14": "pod.",
    "20": "teardrop.",
    "15": "portsweep.",
    "5": "ipsweep.",
    "6": "land.",
    "2": "ftp_write.",
    "0": "back.",
    "4": "imap.",
    "17": "satan.",
    "13": "phf.",
    "10": "nmap.",
    "8": "multihop.",
    "22": "warezmaster.",
    "21": "warezclient.",
    "19": "spy.",
    "16": "rootkit."
}


def index(request):
    return render(request, 'index.html')


def analyze(request):
    # 获取前端上传参数
    features = request.GET.getlist('features[]')
    ids, values = [], []
    for feature in features:
        ids.append(feature_list.index(feature))
        if feature in symbolicFeature:
            values.append(feature_map[feature][request.GET.get(feature)])
        else:
            values.append(float(request.GET.get(feature)))
    # 读取模型
    with open('model/clt.pickle', 'rb') as f:
        dlt = pickle.load(f)
    # 读取初始状态
    initState = np.load('model/initState.npy')
    # 参数赋值给初始状态
    for index, id in enumerate(ids):
        initState[id] = values[index]
    # 获取决策参数
    cofs = dlt.coef_
    coefficient = []
    for id in ids:
        coefficient.append(cofs[:, id])
    # 获取label
    label_by_order = []
    for i in range(23):
        label_by_order.append(label_dic[str(i)])
    # 构建决策参数矩阵
    index_with_cof = []
    for j in range(len(features)):
        for i in range(23):
            index_with_cof.append([i, j, round(coefficient[j][i], 2)])
    print(index_with_cof)
    predict_prob = list((dlt.predict_proba([initState])[0]))
    for i, v in enumerate(predict_prob):
        predict_prob[i] = round(v, 8)
    predict = int(dlt.predict([initState])[0])
    result = {'code': 200, "predict_prob": predict_prob, 'predict': predict, 'features': features,
              'label': label_by_order, 'cof': index_with_cof}
    response = HttpResponse(json.dumps(result, ensure_ascii=False),
                            content_type="application/json,charset=utf-8")
    return response


def mul_analyze(request):
    multiInput = request.FILES.get('multiInput')
    text_content = multiInput.read()
    text_content = text_content.decode(encoding='UTF-8', errors='strict')
    lines = text_content.split('\n')
    features = re.sub('\s|\t', '', lines[0]).split(',')
    values, ids = [], []
    for feature in features:
        ids.append(feature_list.index(feature))
    for i in range(1, len(lines)):
        input_ = re.sub('\s|\t', '', lines[i]).split(',')
        value = []
        for index, feature in enumerate(features):
            if feature in symbolicFeature:
                value.append(feature_map[feature][input_[index]])
            else:
                value.append(float(input_[index]))
        values.append(value)
    # 读取初始状态
    initState = np.load('model/initState.npy')
    # 参数赋值给初始状态
    inputs = []
    for i in range(len(values)):
        line_input = list(initState.copy())
        for j, id in enumerate(ids):
            line_input[id] = values[i][j]
        inputs.append(line_input)
    # 读取模型
    with open('model/clt.pickle', 'rb') as f:
        dlt = pickle.load(f)
    predict_prob = list((dlt.predict_proba(inputs)))
    predict = list((dlt.predict(inputs)))
    for i in range(len(values)):
        predict_prob[i] = list(predict_prob[i].copy())
        for j, v in enumerate(predict_prob[i]):
            predict_prob[i][j] = round(v, 8)
    for i in range(len(predict)):
        predict[i] = int(predict[i])
    label_by_order = []
    for i in range(23):
        label_by_order.append(label_dic[str(i)])
    # 构建决策参数矩阵
    cofs = dlt.coef_
    coefficient = []
    for id in ids:
        coefficient.append(cofs[:, id])

    index_with_cof = []
    for j in range(len(features)):
        for i in range(23):
            index_with_cof.append([i, j, round(coefficient[j][i], 2)])

    result = {'code': 200, "predict_prob": predict_prob, 'predict': predict, 'features': features,
              'label': label_by_order, 'cof': index_with_cof}
    response = HttpResponse(json.dumps(result, ensure_ascii=False),
                            content_type="application/json,charset=utf-8")
    return response
