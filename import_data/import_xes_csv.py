import pm4py
import pandas


def import_xes(filename):
    log = pm4py.read_xes(filename)
    start_activities = pm4py.get_start_activities(log)
    end_activities = pm4py.get_end_activities(log)
    print(f'start_activities: {start_activities}, end_activities: {end_activities}')


def import_csv(filename):
    log = pandas.read_csv(filename, sep=';')
    log = pm4py.format_dataframe(log, case_id='case_id', activity_key='activity', timestamp_key='timestamp',
                                 timest_format='%Y-%m-%d %H:%M:%S%z')
    start_activities = pm4py.get_start_activities(log)
    end_activities = pm4py.get_end_activities(log)
    print("start_activities: {}, end_activities: {}".format(start_activities, end_activities))


def import_xes_2(filename):
    log = pm4py.read_xes(filename)  # DataFrame
    print(log.info())

    # convert dataframe to list and do filtering
    log_list: list = log.values.tolist()  # log.values is a ndarray
    print("log list:")
    for i in log_list:
        print(i)
    trace_list = list(filter(lambda x: len(x) > 5, log_list))
    print("trace list:")
    print(trace_list)

    # use pm4py to do filtering
    trace_log = pm4py.filter_log(lambda t: len(t) > 2, log)
    print("trace log:")
    print(trace_log)


if __name__ == '__main__':
    print("reading data from xes file")
    import_xes("../data/running-example.xes")
    print("reading data from csv file")
    import_csv("../data/running-example.csv")
    print("reading data from xes file with filter")
    import_xes_2("../data/running-example.xes")
