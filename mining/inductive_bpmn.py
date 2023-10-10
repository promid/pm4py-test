import pm4py

if __name__ == "__main__":
    log = pm4py.read_xes('../data/running-example.xes')
    process_model = pm4py.discover_bpmn_inductive(log, 0.8)  # 0.8 is the noise threshold
    pm4py.view_bpmn(process_model, format="jpeg")
