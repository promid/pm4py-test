import pm4py
import pandas

from pm4py.algo.conformance.alignments.process_tree import algorithm as alignments_pt

if __name__ == '__main__':
    process_tree_str = "->('Scheduled','Pulling','Pulled','Created','Started')"
    process_tree = pm4py.parse_process_tree(process_tree_str)
    print(process_tree)
    petri_net, initial_marking, final_marking = pm4py.convert_to_petri_net(process_tree)
    log_csv_file = '../data/create-pod.csv'
    csv_log = pandas.read_csv(log_csv_file, sep=';')
    log = pm4py.format_dataframe(csv_log, case_id='case_id', activity_key='activity', timestamp_key='timestamp',
                                 timest_format='%Y-%m-%d %H:%M:%S%z')
    alignments = pm4py.fitness_alignments(log, petri_net, initial_marking, final_marking)
    print(alignments)

    alignments_res = alignments_pt.apply(log, process_tree)
    print(alignments_res)

    # num = 1
    # for alignment in alignments_res:
    #     print("num", num)
    #     print("fitness:", alignment['fitness'])
    #     print("对齐:", alignment['alignment'])
    #     print("偏差成本:", alignment['cost'])
    #     num += 1
