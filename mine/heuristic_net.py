import pm4py

if __name__ == "__main__":
    log = pm4py.read_xes('../data/running-example.xes')
    map = pm4py.discover_heuristics_net(log)
    pm4py.view_heuristics_net(map, format="jpeg")