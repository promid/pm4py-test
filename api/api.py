import pandas
import pm4py
from flask import Flask, request, jsonify
from flask_cors import CORS
from pm4py.algo.conformance.alignments.process_tree import algorithm as alignments_pt

app = Flask(__name__)
CORS(app)


@app.route('/process_alignments', methods=['POST'])
def process_alignments():
    data = request.json
    process_tree_str = data.get('process_tree_str')
    log_csv_file_path = data.get('log_csv_file_path')
    process_tree = pm4py.parse_process_tree(process_tree_str)
    csv_log = pandas.read_csv(log_csv_file_path, sep=';')
    log = pm4py.format_dataframe(csv_log, case_id='case_id', activity_key='activity', timestamp_key='timestamp',
                                 timest_format='%Y-%m-%d %H:%M:%S%z')
    alignments_res = alignments_pt.apply(log, process_tree)
    items = []
    for res in alignments_res:
        item = {"cost": res['cost'], "alignment": []}
        for t in res['alignment']:
            key = t[0]
            # 判断t[1]是否是str
            if isinstance(t[1], str):
                value = t[1]
            elif hasattr(t[1], 'label'):
                value = t[1].label
            else:
                value = "unknown"
            kv = {'model': key, 'log': value}
            item["alignment"].append(kv)
        item['fitness'] = res['fitness']
        items.append(item)
    ret = {"result": items}
    print(ret)
    return jsonify(ret)


def alignments_res_to_serializable(alignments_res):
    serializable_alignments = []
    for alignment in alignments_res:
        # 为了简化，这里我们只转换了部分字段
        serializable_alignment = {
            'cost': alignment['cost'],
            'alignment': alignment['alignment'],
            'optimal': alignment['optimal'],
            'fitness': alignment['fitness']
        }
        serializable_alignments.append(serializable_alignment)
    return serializable_alignments


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
