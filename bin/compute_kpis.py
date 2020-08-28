from __future__ import division
from __future__ import print_function

# =========================== adjust path =====================================

import os
import sys

import netaddr

if __name__ == '__main__':
    here = sys.path[0]
    sys.path.insert(0, os.path.join(here, '..'))

# ========================== imports ==========================================

import json
import glob
import numpy as np

from SimEngine import SimLog
import SimEngine.Mote.MoteDefines as d

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import copy
import argparse

# =========================== defines =========================================

subfolder = None

#DAGROOT_ID_0 = 0  # we assume first mote is DAGRoot
#DAGROOT_IP_0 = 'fd00::1:0'


#second dagroot

#DAGROOT_ID_1 = 1
#DAGROOT_IP_1 = 'fd00::1'

DAGROOT_IPs= ['fd00::1:0','fd00::1']


BATTERY_AA_CAPACITY_mAh = 2821.5

# =========================== decorators ======================================

def openfile(func):
    def inner(inputfile):
        with open(inputfile, 'r') as f:
            return func(f)
    return inner

# =========================== helpers =========================================


def plot_motes_app_tx_seconds(data,file_settings,window='regular'):
    global subfolder
    # print(data)
    for mote_id, times in list(data.items()):
        y=np.empty(len(times)); 
        y.fill(mote_id);
        s = np.empty(len(times))
        s.fill(10)
        # n_times = [i /60/60 for i in times]
        plt.scatter(times,y,s = s)
        # plt.plot(times,np.arange(0,len(times)))
    if window != 'regular': 
        # window = 'backoff'
        plt.axis([1500,2600,0,10])
    plt.xlabel('time(s)')
    plt.ylabel('mote ID')
    plt.title('Packet creation time - {} '.format(file_settings['band']))
    # plt.show()
    plt.savefig(os.path.join(subfolder, 'tx_times.png'),dpi=300)
    plt.close()


def plot_avg_hops(data,file_settings):
    global subfolder
    plt.bar(data.keys(),data.values())
    plt.ylabel('Average Hops')
    plt.xlabel('mote ID')
    plt.title('Average Hops by mote - {} '.format(file_settings['band']))
    plt.savefig(os.path.join(subfolder, 'avg_hops.png'),dpi=300)
    plt.close()



def plot_deploy(allstatsData,file_settings):
    # moteData = {k: v for k, v in allstatsData.items() }
    global subfolder
    coordinates = {}
    labels = {}
    for k, v in allstatsData.items():
        if isinstance(k, int):
            # coordinates[k] = {}
            # labels[k] = {}
            for new_k, new_v in v.items():
                if new_k.startswith('coordinates'):
                    # coordinates[k][new_k] = new_v
                    coordinates[k] = new_v
                elif new_k.startswith('dodagRoot'):
                    # labels[k][new_k] = new_v
                    labels[k] = 'DODAG{} - Mote'.format(DAGROOT_IPs.index(new_v))
                if 'dodagRoot' not in v:
                    #either this mote is a root or it was not connected
                    if k in file_settings['roots']:
                        labels[k] = 'DODAG{} - Root'.format(k)
                    else:
                        labels[k] = 'NOT CONNECTED'

   

    x_o, y_o = zip(*coordinates.values())
    x = [i * 1000 for i in x_o]
    y = [i * 1000 for i in y_o]

    df = pd.DataFrame(dict(x=x, y=y, DODAG=list(labels.values())))

    groups = df.groupby('DODAG')


    plt.axis('equal')
    # plt.axis([0,100,-20,10])
    for name, group in groups:
        plt.plot(group["x"], group["y"], marker="o", linestyle="", label=name)

    # if file_settings['exec_numMotes'] > 20:
        # txt_x_offset = 2.0
        # txt_y_offset = 2.0
        # fontsize = 4

    # else:
        txt_x_offset = 0.15
        txt_y_offset = 0.4
        fontsize = 4

    for key in coordinates.keys():
        txt = 'id:{}'.format(key)
        # plt.annotate(txt, xy=(x[key],y[key]), xytext=(x[key]-txt_x_offset,y[key]-txt_y_offset))
        plt.text(x[key]-txt_x_offset, y[key]-txt_y_offset, 'id:{}'.format(key), fontsize=fontsize)


    plt.xlabel('x (m)')
    plt.ylabel('y (m)')

    plt.title('Deploy area and network distribution - {} '.format(file_settings['band']))

    handles, labels = plt.gca().get_legend_handles_labels()

    # sort both labels and handles by labels

    labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
    plt.legend(handles, labels)

    plt.savefig(os.path.join(subfolder, 'deploy.png'),dpi=300)
    plt.close()

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

def init_mote():
    return {
        'upstream_num_tx': 0,
        'upstream_num_rx': 0,
        'upstream_num_lost': 0,
        'join_asn': None,
        'join_time_s': None,
        'sync_asn': None,
        'sync_time_s': None,
        'charge_asn': None,
        'upstream_pkts': {},
        'latencies': [],
        'hops': [],
        'charge': None,
        'lifetime_AA_years': None,
        'avg_current_uA': None,
        'tx_seconds': [],

    }

def createSingleStats(stats,mote_id,motestats):
    # return {
    if mote_id not in stats['network']:
        stats['network'].append(mote_id)
        stats['network_size'] += 1
   
    stats['app_packets_sent'] += motestats['upstream_num_tx']
    stats['app_packets_received'] += motestats['upstream_num_rx']
    stats['app_packets_lost'] += motestats['upstream_num_lost']

    # joining times

    if motestats['join_asn'] is not None:
        stats['joining_times'].append(motestats['join_asn'])

    # latency

    stats['us_latencies'] += motestats['latencies']


    # current consumed

    stats['current_consumed'].append(motestats['charge'])
    if motestats['lifetime_AA_years'] is not None:
        stats['lifetimes'].append(motestats['lifetime_AA_years'])
    stats['current_consumed'] = [
        value for value in stats['current_consumed'] if value is not None
    ]

    #hops
    if 'avg_hops' in motestats.keys():
        stats['avg_hops'][mote_id] = motestats['avg_hops']

    #tx packets
    if 'tx_seconds' in motestats.keys():
        stats['tx_seconds'][mote_id] = motestats['tx_seconds']

    # }
def createAllStats(stats):
    return {
            'network-connectivity-data':[
                    {
                        'name': 'List of connected mote IDs',
                        'value': stats['network']
                    },
                    {
                        'name': 'Network Size',
                        'value': stats['network_size']
                    },
                    {
                        'name': 'Average Hops By mote',
                        'value': stats['avg_hops']
                    },
                ],
            'e2e-upstream-delivery': [
                {
                    'name': 'E2E Upstream Delivery Ratio',
                    'unit': '%',
                    'value': (
                        1 - stats['app_packets_lost'] / stats['app_packets_sent']
                        if stats['app_packets_sent'] > 0 else 'N/A'
                    )
                },
                {
                    'name': 'E2E Upstream Loss Rate',
                    'unit': '%',
                    'value': (
                        stats['app_packets_lost'] / stats['app_packets_sent']
                        if stats['app_packets_sent'] > 0 else 'N/A'
                    )
                }
            ],
            'e2e-upstream-latency': [
                {
                    'name': 'E2E Upstream Latency',
                    'unit': 's',
                    'mean': (
                        mean(stats['us_latencies'])
                        if stats['us_latencies'] else 'N/A'
                    ),
                    'min': (
                        min(stats['us_latencies'])
                        if stats['us_latencies'] else 'N/A'
                    ),
                    'max': (
                        max(stats['us_latencies'])
                        if stats['us_latencies'] else 'N/A'
                    ),
                    '99%': (
                        np.percentile(stats['us_latencies'], 99)
                        if stats['us_latencies'] else 'N/A'
                    )
                },
                {
                    'name': 'E2E Upstream Latency',
                    'unit': 'slots',
                    'mean': (
                        mean(stats['us_latencies']) / stats['slot_duration']
                        if stats['us_latencies'] else 'N/A'
                    ),
                    'min': (
                        min(stats['us_latencies']) / stats['slot_duration']
                        if stats['us_latencies'] else 'N/A'
                    ),
                    'max': (
                        max(stats['us_latencies']) / stats['slot_duration']
                        if stats['us_latencies'] else 'N/A'
                    ),
                    '99%': (
                        np.percentile(stats['us_latencies'], 99) / stats['slot_duration']
                        if stats['us_latencies'] else 'N/A'
                    )
                }
            ],
            'current-consumed': [
                {
                    'name': 'Current Consumed',
                    'unit': 'mA',
                    'mean': (
                        mean(stats['current_consumed'])
                        if stats['current_consumed'] else 'N/A'
                    ),
                    '99%': (
                        np.percentile(stats['current_consumed'], 99)
                        if stats['current_consumed'] else 'N/A'
                    )
                }
            ],
            'network_lifetime':[
                {
                    'name': 'Network Lifetime',
                    'unit': 'years',
                    'min': (
                        min(stats['lifetimes'])
                        if stats['lifetimes'] else 'N/A'
                    ),
                    'total_capacity_mAh': BATTERY_AA_CAPACITY_mAh,
                }
            ],
            'joining-time': [
                {
                    'name': 'Joining Time',
                    'unit': 's',
                    'mean': (
                        mean(stats['joining_times'])*stats['slot_duration']
                        if stats['joining_times'] else 'N/A'
                    ),
                    'min': (
                        min(stats['joining_times'])*stats['slot_duration']
                        if stats['joining_times'] else 'N/A'
                    ),
                    'max': (
                        max(stats['joining_times'])*stats['slot_duration']
                        if stats['joining_times'] else 'N/A'
                    ),
                    '99%': (
                        np.percentile(stats['joining_times'], 99)*stats['slot_duration']
                        if stats['joining_times'] else 'N/A'
                    )
                },
                {
                    'name': 'Joining Time',
                    'unit': 'slots',
                    'min': (
                        min(stats['joining_times'])
                        if stats['joining_times'] else 'N/A'
                    ),
                    'max': (
                        max(stats['joining_times'])
                        if stats['joining_times'] else 'N/A'
                    ),
                    'mean': (
                        mean(stats['joining_times'])
                        if stats['joining_times'] else 'N/A'
                    ),
                    '99%': (
                        np.percentile(stats['joining_times'], 99)
                        if stats['joining_times'] else 'N/A'
                    )
                }
            ],
            'app-packets-sent': [
                {
                    'name': 'Number of application packets sent',
                    'total': stats['app_packets_sent']
                }
            ],
            'app_packets_received': [
                {
                    'name': 'Number of application packets received',
                    'total': stats['app_packets_received']
                }
            ],
            'app_packets_lost': [
                {
                    'name': 'Number of application packets lost',
                    'total': stats['app_packets_lost']
                }
            ]
    }  

def is_number(s):
    try:
        float(s)  
    except ValueError:
        return False
    return True

def createJoinStatsRuns(stats):
    #Initialize with first
    join_stats = {}
    join_stats = copy.deepcopy(stats[0]['global-stats'])

    totalRuns = len(list(stats.items()))
    for (run_id, per_mote_stats) in stats.items():
        #read global from each
        if run_id == 0:
            #skips first
            continue
        # print(list(per_mote_stats['global-stats'].items()))

        for (key, value) in per_mote_stats['global-stats'].items():
                for index in range(len(value)): 
                    for (inner_key,inner_value) in list(value[index].items()):
                        if not hasattr(inner_value, "__len__"):
                            #if is a number it will be added for later computation
                            join_stats[key][index][inner_key] = [join_stats[key][index][inner_key]]+[inner_value]
                            # else there is no need to do anything
                            if run_id == totalRuns - 1:
                                #calculate the average from both stats
                                # print('COMPUTE MEAN', key, index, inner_key,join_stats[key][index][inner_key])
                                join_stats[key][index][inner_key] = mean(join_stats[key][index][inner_key])

                        
                        else:
                            # if not string
                            if not isinstance(inner_value, str) and type(inner_value) is not list:
                            #iterate over the array   
                                for (obj_key,obj_value) in list(inner_value.items()): 
                                    # if not present, that mote did not connect    
                                    if obj_key in join_stats[key][index][inner_key]:
                                        join_stats[key][index][inner_key][obj_key] = [join_stats[key][index][inner_key][obj_key]]+[obj_value]
                                        if run_id == totalRuns - 1:
                                            #calculate the average from both stats
                                            # print('COMPUTE MEAN', key, index, inner_key,join_stats[key][index][inner_key])
                                            join_stats[key][index][inner_key][obj_key] = mean(join_stats[key][index][inner_key][obj_key])




    return join_stats

# =========================== KPIs ============================================

@openfile
def kpis_all(inputfile):

    allstats = {} # indexed by run_id, DODAG [many DODAGS defined by number of roots], mote_id.

    file_settings = json.loads(inputfile.readline())  # first line contains settings

    if 'roots' in file_settings.keys(): 
        assert len(DAGROOT_IPs) >= len(file_settings['roots'])

    # === gather raw stats
    

    for line in inputfile:
        logline = json.loads(line)

        # shorthands
        run_id = logline['_run_id']
        if '_asn' in logline: # TODO this should be enforced in each line
            asn = logline['_asn']
        if '_mote_id' in logline: # TODO this should be enforced in each line
            mote_id = logline['_mote_id']

        # populate
        if run_id not in allstats:
            allstats[run_id] = {}
        if (
                ('_mote_id' in logline)
                and
                (mote_id not in allstats[run_id])
               

            ):
            allstats[run_id][mote_id] = init_mote()


        if   logline['_type'] == SimLog.LOG_TSCH_SYNCED['type']:
            # sync'ed

            # shorthands
            mote_id    = logline['_mote_id']

            # only log non-dagRoot sync times
            if mote_id in file_settings['roots']:
                # break from loop skip this run.
                continue

            allstats[run_id][mote_id]['sync_asn']  = asn
            allstats[run_id][mote_id]['sync_time_s'] = asn*file_settings['tsch_slotDuration']

        elif logline['_type'] == SimLog.LOG_SECJOIN_JOINED['type']:
            # joined

            # shorthands
            mote_id    = logline['_mote_id']

            # only log non-dagRoot join times
            if mote_id in file_settings['roots']:
                continue
            if not allstats[run_id][mote_id]['join_asn']:
                print('first joined', mote_id, 'at ', asn)
            else:
                print('this mote was joined previously ->', mote_id, 'at ', allstats[run_id][mote_id]['join_asn'], 'now at ', asn)

            # populate
            assert allstats[run_id][mote_id]['sync_asn'] is not None
            allstats[run_id][mote_id]['join_asn']  = asn
            allstats[run_id][mote_id]['join_time_s'] = asn*file_settings['tsch_slotDuration']


        elif logline['_type'] == SimLog.LOG_APP_TX['type']:
            # packet transmission

            # shorthands
            mote_id    = logline['_mote_id']
            dstIp      = logline['packet']['net']['dstIp']
            appcounter = logline['packet']['app']['appcounter']
            seconds = logline['packet']['app']['seconds']
            
            # print(mote_id, dstIp)

            # only log upstream packets 
            # if dstIp != DAGROOT_IP_0 and dstIp != DAGROOT_IP_1:
            if dstIp not in DAGROOT_IPs:
                # skips this run
                # maybe they skip it because the last hop is not counted?
                continue

            # populate
            assert allstats[run_id][mote_id]['join_asn'] is not None
            if appcounter not in allstats[run_id][mote_id]['upstream_pkts']:
                # initiallize the first hop, the final hop count is stored in the received packet
                # hops are decremented on 6LowPAN and updated in the packet content
                allstats[run_id][mote_id]['upstream_pkts'][appcounter] = {
                    'hops': 0,
                }
           
            # check if the packet was already transmited previously to override it
            # if the package was sent o a different asn by another interface it means that the applications are not sync
            # or that the mote unjoined the DODAG. IN order to fix this, a margin is considered, and the Lowest ASN is considered.

            if 'tx_seconds' in allstats[run_id][mote_id]['upstream_pkts'][appcounter]:
                #consider a one period window max
                previous_tx_sec = allstats[run_id][mote_id]['upstream_pkts'][appcounter]['tx_seconds']
                if previous_tx_sec > seconds+file_settings["app_pkPeriod"]:
                    allstats[run_id][mote_id]['upstream_pkts'][appcounter]['online'] = True;

            #override data for the new interace ( on RX latency will be computed)
            allstats[run_id][mote_id]['upstream_pkts'][appcounter]['tx_asn'] = asn
            allstats[run_id][mote_id]['upstream_pkts'][appcounter]['tx_seconds'] = seconds

        elif logline['_type'] == SimLog.LOG_APP_RX['type']:
            # packet reception

            # shorthands
            mote_id    = netaddr.IPAddress(logline['packet']['net']['srcIp']).words[-1]
            dstIp      = logline['packet']['net']['dstIp']
            hop_limit  = logline['packet']['net']['hop_limit']
            appcounter = logline['packet']['app']['appcounter']

            #slot duration was added to packet to acctount for multiple slot durarions
            slot_duration = logline['config']['slot_duration']

            tx_asn = allstats[run_id][mote_id]['upstream_pkts'][appcounter]['tx_asn']


            # only log upstream packets 
            if dstIp not in DAGROOT_IPs:
                continue
            
            if 'latency' in allstats[run_id][mote_id]['upstream_pkts'][appcounter] and 'online' not in allstats[run_id][mote_id]['upstream_pkts'][appcounter]:
            # packet was already received by other radio interface 
            # online - represents the correct packet, as the other interface was offline (there is only this one to account for)
                # older packet tx_asn is replaced on the packet TX compute, hence tx_asn is related to the new packet.
                if allstats[run_id][mote_id]['upstream_pkts'][appcounter]['latency'] > (asn-tx_asn)*slot_duration:
                    # Substitute older latency if longer than the second one
                    allstats[run_id][mote_id]['upstream_pkts'][appcounter]['latency'] = (asn-tx_asn)*slot_duration

            else :
                #this packet was not received by the first interface, hence this is the correct latency to use
                allstats[run_id][mote_id]['upstream_pkts'][appcounter]['latency'] = (asn-tx_asn)*slot_duration


            allstats[run_id][mote_id]['upstream_pkts'][appcounter]['hops']   = (
                d.IPV6_DEFAULT_HOP_LIMIT - hop_limit + 1
            )
            allstats[run_id][mote_id]['upstream_pkts'][appcounter]['rx_asn'] = asn

            #add slot duration foir join compute ( two radio interface )
            allstats[run_id][mote_id]['upstream_pkts'][appcounter]['slot_duration'] = slot_duration

        elif logline['_type'] == SimLog.LOG_RADIO_STATS['type']:
            # shorthands
            mote_id    = logline['_mote_id']

            # only log non-dagRoot charge 
            if mote_id in file_settings['roots']:
                continue 

            # logline[slot_type] contains the amount of slots that the currently mote operated in.
            # Slots are multiplyed by their consumption in uC.
            # later this value is converted to uA considering the newtork lifetime and slot length.
            charge =  logline['idle_listen'] * d.CHARGE_IdleListen_uC
            charge += logline['tx_data_rx_ack'] * d.CHARGE_TxDataRxAck_uC
            charge += logline['rx_data_tx_ack'] * d.CHARGE_RxDataTxAck_uC
            charge += logline['tx_data'] * d.CHARGE_TxData_uC
            charge += logline['rx_data'] * d.CHARGE_RxData_uC
            charge += logline['sleep'] * d.CHARGE_Sleep_uC

            allstats[run_id][mote_id]['charge_asn'] = asn # network duration in slots. Last recorded
            allstats[run_id][mote_id]['charge']     = charge

        elif logline['_type'] == SimLog.LOG_RPL_JOIN_DAG['type']:

            allstats[run_id][mote_id]['dodagRoot'] = logline['_joined_dag']

          
        elif logline['_type'] == SimLog.LOG_DEPLOY_COORDINATES['type']:

            allstats[run_id][mote_id]['coordinates'] = logline['_coordinates']



    # === compute advanced motestats
    for (run_id, per_mote_stats) in list(allstats.items()):
        for (mote_id, motestats) in list(per_mote_stats.items()):
            if mote_id not in file_settings['roots']:

                if (motestats['sync_asn'] is not None) and (motestats['charge_asn'] is not None):
                    # avg_current, lifetime_AA
                    if (
                            (motestats['charge'] <= 0)
                            or
                            (motestats['charge_asn'] <= motestats['sync_asn'])
                        ):
                        motestats['lifetime_AA_years'] = 'N/A'
                    else:
                        # Motes count how many slots they operated in for each type of slot.
                        # charge asn is the last recoreded asn with a radio stat msg. (network life)
                        # the asns where the mote was not synced are ignored.
                        # the result is multiplied by the slot length in seconds.
                        # hence  uC * s = uA. Since uc = [A/S] giving uA/s * s = uA.
                        motestats['avg_current_uA'] = motestats['charge']/float((motestats['charge_asn']-motestats['sync_asn']) * file_settings['tsch_slotDuration'])
                        assert motestats['avg_current_uA'] > 0
                        motestats['lifetime_AA_years'] = (BATTERY_AA_CAPACITY_mAh*1000/float(motestats['avg_current_uA']))/(24.0*365)
                if motestats['join_asn'] is not None:
                    # latencies, upstream_num_tx, upstream_num_rx, upstream_num_lost
                    if len(list(allstats[run_id][mote_id]['upstream_pkts'].keys())) > 5:
                        treshold = max(list(allstats[run_id][mote_id]['upstream_pkts'].keys()))-5

                    for (appcounter, pktstats) in list(allstats[run_id][mote_id]['upstream_pkts'].items()):                    
                        #ignore last packets ( last 5 from each mote)
                        if appcounter <= treshold:
                            motestats['tx_seconds']+=[pktstats['tx_seconds']]
                            motestats['upstream_num_tx']      += 1
                            if 'rx_asn' in pktstats:
                                motestats['upstream_num_rx']  += 1
                                # thislatency = (pktstats['rx_asn']-pktstats['tx_asn'])*file_settings['tsch_slotDuration']
                                # thislatency = (pktstats['rx_asn']-pktstats['tx_asn'])*pktstats['slot_duration']
                                thislatency = pktstats['latency']
                                motestats['latencies']  += [thislatency]
                                motestats['hops']       += [pktstats['hops']]
                            else:
                                print('\n', mote_id, ' Lost packet -> ', appcounter, '\n')
                                motestats['upstream_num_lost'] += 1
                    if (motestats['upstream_num_rx'] > 0) and (motestats['upstream_num_tx'] > 0):
                        motestats['latency_min_s'] = min(motestats['latencies'])
                        motestats['latency_avg_s'] = sum(motestats['latencies'])/float(len(motestats['latencies']))
                        motestats['latency_max_s'] = max(motestats['latencies'])
                        motestats['upstream_reliability'] = motestats['upstream_num_rx']/float(motestats['upstream_num_tx'])
                        motestats['avg_hops'] = sum(motestats['hops'])/float(len(motestats['hops']))

    # === network stats

    stats = {}
    stats['global'] = {}
    # if there is only one root we do not need separeted statistics
    if len(file_settings['roots']) > 1:
        for root in file_settings['roots']:
            stats['DODAG_{}'.format(root)] = {}




    for (run_id, per_mote_stats) in list(allstats.items()):

        #-- define stats

        # reset for EACH RUN
        # global counters
        stats['global'] =  {
            'network':[],
            'network_size': 0,
            'avg_hops':{},
            'app_packets_sent': 0,
            'app_packets_received': 0,
            'app_packets_lost': 0,
            'joining_times': [],
            'us_latencies':[],
            'current_consumed':[],
            'lifetimes':[],
            'slot_duration':file_settings['tsch_slotDuration'],
            'tx_seconds':{}

        }

        # if there is only one root we do not need separeted statistics
        if len(file_settings['roots']) > 1:
            for root in file_settings['roots']:
                stats['DODAG_{}'.format(root)] = {
                    'network':[],
                    'network_size': 0,
                    'avg_hops': {},
                    'app_packets_sent': 0,
                    'app_packets_received': 0,
                    'app_packets_lost': 0,
                    'joining_times': [],
                    'us_latencies':[],
                    'current_consumed':[],
                    'lifetimes':[],
                    'slot_duration':file_settings['tsch_slotDuration'],
                    'tx_seconds':{}
                }

        #-- compute stats
        for (mote_id, motestats) in list(per_mote_stats.items()):
            if mote_id in file_settings['roots']:
                continue

            createSingleStats(stats['global'],mote_id,motestats)

            # Assert dodag log is present
            # if there is only one root we do not need separeted statistics
            if 'dodagRoot' in motestats and len(file_settings['roots']) > 1:
                createSingleStats(
                    stats['DODAG_{}'.format(DAGROOT_IPs.index(motestats['dodagRoot']))],
                    mote_id,
                    motestats)

        #plot avg hops
        plot_avg_hops(stats['global']['avg_hops'],file_settings)

         #plot tx packs seconds
    
        plot_motes_app_tx_seconds(stats['global']['tx_seconds'],file_settings)


        #-- save stats
        allstats[run_id]['global-stats'] = createAllStats(stats['global'])

        # if there is only one root we do not need separeted statistics
        if len(file_settings['roots']) > 1:
            for root in file_settings['roots']:
                allstats[run_id]['DODAG_{}-stats'.format(root)] = createAllStats(stats['DODAG_{}'.format(root)])

    # === remove unnecessary stats

    for (run_id, per_mote_stats) in list(allstats.items()):
        for (mote_id, motestats) in list(per_mote_stats.items()):
            if 'sync_asn' in motestats:
                del motestats['sync_asn']
            if 'charge_asn' in motestats:
                del motestats['charge_asn']
                del motestats['charge']
            if 'join_asn' in motestats:
                del motestats['upstream_pkts']
                del motestats['hops']
                del motestats['join_asn']
                # del motestats['tx_seconds']
                # del motestats['latencies']




    # Join KPIs from all runs

    # starting wiht simple average from global KPI s
    # numRuns are not sved in .data file, must check run ids in all stats
    if len(list(allstats.keys())) > 1:
        allstats['join-metrics'] = createJoinStatsRuns(allstats)

    # plot deploy of first run
    plot_deploy(allstats[0],file_settings)
    return allstats


def parse_args():
    # parse options
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--inputfolder',
        help       = 'The simulation result folder.',
        default    = None,
    )
    return parser.parse_args()

# =========================== main ============================================

def main(options):


    global subfolder
    # FIXME: This logic could be a helper method for other scripts
    # Identify simData having the latest results. That directory should have
    # the latest "mtime".

    if options.inputfolder:
        subfolder = options.inputfolder
    else:
        #defatult to simData
        subfolders = list([os.path.join('simData', x) for x in os.listdir('simData')])
        subfolder = max(subfolders, key=os.path.getmtime)
    print(subfolder)
    if len(glob.glob(os.path.join(subfolder, '*.dat'))):
        for infile in glob.glob(os.path.join(subfolder, '*.dat')):
            print('generating KPIs for {0}'.format(infile))

            # gather the kpis
            kpis = kpis_all(infile)

            # print on the terminal
            # print(json.dumps(kpis, indent=4))

            # add to the data folder
            outfile = '{0}.kpi'.format(infile)
            with open(outfile, 'w') as f:
                f.write(json.dumps(kpis, indent=4))
            print('KPIs saved in {0}'.format(outfile))
    else:

        print('Path does not contain ".dat" file')

if __name__ == '__main__':

    options = parse_args()

    main(options)