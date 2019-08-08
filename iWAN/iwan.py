import re
import pprint

import json

channel_file = 'channel.txt'
class_file = 'class.txt'

def iwanclass (file, channel_data):
    # Dst-Site-Prefix: 10.225.76.164/32    DSCP: default [0] Traffic class id:59827542
    p1 = re.compile(r'Dst-Site-Prefix:\s*(?P<dst_site_prefix>\S+)\s*DSCP:\s*(?P<dscp>\S*)')

    #  Clock Time:                 14:16:10 (CDT) 08/05/2019
    p2 = re.compile(r'\S*Clock\s*Time:\s*(?P<clock_time>.*)')

    #  TC Learned:                 4w2d ago
    p3 = re.compile(r'\S*TC\s*Learned:\s*(?P<tc_learned>.*)')

    #  Present State:              CONTROLLED
    p4 = re.compile(r'\S*Present\s*State:\s*(?P<present_state>.*)')

    #  Current Performance Status: in-policy
    p5 = re.compile(r'\S*Current\s*Performance\s*Status:\s*(?P<current_performance_status>.*)')

    #  Current Service Provider:   ISP2 since 09:39:28
    p6 =   re.compile(r'\S*Current\s*Service\s*Provider:\s*(?P<current_service_provider>.*)')

    #  Previous Service Provider:  ISP1 pfr-label: 0:0 | 0:0 [0x0] for 180 sec
    p7 = re.compile(r'\S*Previous\s*Service\s*Provider:\s*(?P<previous_service_provider>.*)')

    #  BW Used:                    0 Kbps
    p8 = re.compile(r'\S*BW\s*Used:\s*(?P<bw_used>.*)')

    #  Present WAN interface:      Tunnel200 in Border 10.1.0.104
    p9 = re.compile(r'\S*Present\s*WAN\s*interface:\s*(?P<present_wan_interface>\S*)\s*in\sBorder\s(?P<border>.*)')

    #  Present Channel (primary):  12488652 ISP2 pfr-label:0:0 | 0:0 [0x0]
    p10 = re.compile(r'\S*Present\s*Channel\s*\(primary\):\s*(?P<present_channel>\d+)')

    #  Backup Channel:             12488653 ISP1 pfr-label:0:0 | 0:0 [0x0]
    p11 = re.compile(r'\S*Backup\s*Channel:\s*(?P<backup_channel>\d+)')

    #  Destination Site ID bitmap: 0
    p12 = re.compile(r'\S*Destination\s*Site\s*ID\s*bitmap:\s*(?P<dst_site_id_bit>.*)')

    #  Destination Site ID:        10.50.0.84
    p13 = re.compile(r'\S*Destination\s*Site\s*ID:\s*(?P<dst_site_id>.*)')

    #  Class-Sequence in use:      20
    p14 = re.compile(r'\S*Class-Sequence\s*in\s*use:\s*(?P<class_sequence_in_use>.*)')

    #  Class Name:                 BEST_EFFORT using policy User-defined
    p15 = re.compile(r'.*\S*Class\s*Name:\s*(?P<class_name>\S*)')
        #priority 2 packet-loss-rate threshold 40.0 percent
        #priority 2 byte-loss-rate threshold 40.0 percent
    p16 = re.compile(r'(?P<priority>priority\s[1-9])\s*(?P<detail>\S*)\s*(?P<type>\S*)\s*(?P<value>.*)')

    #  BW Updated:                 00:00:26 ago
    p17 = re.compile(r'\S*BW\s*Updated:\s*(?P<bw_updated>.*)')

    #  Reason for Latest Route Change:    Backup to Primary path preference transition

    #  Route Change History:
    p18 = re.compile(r'Date and Time')


    #  1:  04:36:42 (CDT) 08/05/19   ISP1(0:0|0:0)/10.1.0.101/Tu100 (Ch:12488653)       ISP2(0:0|0:0)/10.1.0.104/Tu200 (Ch:12488652)       Backup to Primary path preference transition
    #  2:  04:33:42 (CDT) 08/05/19   ISP2(0:0|0:0)/10.1.0.104/Tu200 (Ch:12488652)       ISP1(0:0|0:0)/10.1.0.101/Tu100 (Ch:12488653)       Unreachable
    #  3:  02:23:41 (CDT) 08/05/19   ISP1(0:0|0:0)/10.1.0.101/Tu100 (Ch:12488653)       ISP2(0:0|0:0)/10.1.0.104/Tu200 (Ch:12488652)       Backup to Primary path preference transition
    #  4:  02:20:39 (CDT) 08/05/19   ISP2(0:0|0:0)/10.1.0.104/Tu200 (Ch:12488652)       ISP1(0:0|0:0)/10.1.0.101/Tu100 (Ch:12488653)       Unreachable
    #  5:  02:10:21 (CDT) 08/03/19   ISP1(0:0|0:0)/10.1.0.101/Tu100 (Ch:12488653)       ISP2(0:0|0:0)/10.1.0.104/Tu200 (Ch:12488652)       Backup to Primary path preference transition
    p19 = re.compile(r'\s*(\d:)\s*(?P<date>\S*\s*\S*\s*\S*)\s*(?P<previous_exit>\S*\s*\S*)\s*(?P<current_exit>\S*\s*\S*)\s*(?P<reason>.*)')


    # 0 or 1 flags
    route_change_flag = 0

    # Init vars
    parsed_dict = {}
    class_name = ''


    out = open(file, "r")


    for line in out:
        #print(line)
        if len(line.strip()) == 0: continue

        line = line.strip()

        m = p1.match(line)

        if m:
            dst_site_prefix = m.group('dst_site_prefix')
            dst_site_dscp = m.group('dscp')

            #parsed_dict[dst_site_prefix] = {}

            if dst_site_prefix not in parsed_dict:
                parsed_dict[dst_site_prefix] = {}

            if dst_site_dscp not in parsed_dict[dst_site_prefix]:
                parsed_dict[dst_site_prefix][dst_site_dscp] = {}
                traffic_classes_dict = parsed_dict[dst_site_prefix][dst_site_dscp]

            # Init keys
            traffic_classes_dict['clock_time'] = ''
            traffic_classes_dict['tc_learned'] = ''
            traffic_classes_dict['present_state'] = ''
            traffic_classes_dict['current_performance_status'] = ''
            traffic_classes_dict['current_service_provider'] = ''
            traffic_classes_dict['previous_service_provider'] = ''
            traffic_classes_dict['bandwidth'] = {}
            traffic_classes_dict['present_wan_interface'] = {}
            traffic_classes_dict['channel'] = {}
            traffic_classes_dict['dst_site_id_bit'] = ''
            traffic_classes_dict['dst_site_id'] = ''
            traffic_classes_dict['class_sequence_in_use'] = ''
            traffic_classes_dict['class_name'] = {}
            traffic_classes_dict['route_change_history'] = []
            route_change_flag = 0
            class_name = ''
            continue

        m = p2.match(line)

        if m:
            traffic_classes_dict['clock_time'] = m.group('clock_time')
            continue

        m = p3.match(line)

        if m:
            traffic_classes_dict['tc_learned'] = m.group('tc_learned')
            continue

        m = p4.match(line)

        if m:
            traffic_classes_dict['present_state'] = m.group('present_state')
            continue

        m = p5.match(line)

        if m:
            traffic_classes_dict['current_performance_status'] = m.group('current_performance_status')
            continue

        m = p6.match(line)

        if m:
            traffic_classes_dict['current_service_provider'] = m.group('current_service_provider')
            continue

        m = p7.match(line)

        if m:
            traffic_classes_dict['previous_service_provider'] = m.group('previous_service_provider')
            continue

        m = p8.match(line)

        if m:
            traffic_classes_dict['bandwidth']['used'] = m.group('bw_used')
            continue

        m = p17.match(line)

        if m:
            traffic_classes_dict['bandwidth']['updated'] = m.group('bw_updated')
            continue

        m = p9.match(line)

        if m:
            traffic_classes_dict['present_wan_interface']['tunnel'] = m.group('present_wan_interface')
            traffic_classes_dict['present_wan_interface']['border'] = m.group('border')
            continue

        m = p10.match(line)

        if m:
            #traffic_classes_dict['channel']['present'] = m.group('present_channel')

            traffic_classes_dict['channel']['present'] = channel_data[m.group('present_channel')]
            continue

        m = p11.match(line)

        if m:
            traffic_classes_dict['channel']['backup'] = channel_data[m.group('backup_channel')]
            continue

        m = p12.match(line)

        if m:
            traffic_classes_dict['dst_site_id_bit'] = m.group('dst_site_id_bit')
            continue

        m = p13.match(line)

        if m:
            traffic_classes_dict['dst_site_id'] = m.group('dst_site_id')
            continue

        m = p14.match(line)

        if m:
            traffic_classes_dict['class_sequence_in_use'] = m.group('class_sequence_in_use')
            continue

        m = p15.match(line)

        if m:
            class_name = m.group('class_name')
            traffic_classes_dict['class_name'][class_name] = {}
            continue

        m = p16.match(line)

        if m:
            traffic_classes_dict['class_name'][class_name]['priority'] = m.group('priority')
            traffic_classes_dict['class_name'][class_name]['detail'] = m.group('detail')
            traffic_classes_dict['class_name'][class_name]['type'] = m.group('type')
            traffic_classes_dict['class_name'][class_name]['value'] = m.group('value')
            continue


        m = p18.match(line)

        if m:
            route_change_flag = 1
            continue

        if route_change_flag:
            m = p19.match(line)

            if m:
                route_change_dict = {}
                route_change_dict['date'] = m.group('date')
                route_change_dict['previous_exit'] = m.group('previous_exit')
                route_change_dict['current_exit'] = m.group('current_exit')
                route_change_dict['reason'] = m.group('reason')
                traffic_classes_dict['route_change_history'].append(route_change_dict)
                continue


    return parsed_dict

def channel(file):
    # Channel Id: 13383058  Dst Site-Id: 10.50.3.60  Link Name: ISP2  DSCP: default [0] pfr-label: 0:0 | 0:0 [0x0] TCs: 5  BackupTCs: 0
    p1 = re.compile(r'.*Channel Id:\s(?P<channel_id>[0-9]+)\s*Dst Site-Id:\s*(?P<dst_site_id>\S*)\s*Link Name:\s*(?P<link_name>\S*)\s*DSCP:\s*(?P<dscp>\S*)')

    #  Channel Created: 4w1d ago
    p2 = re.compile(r'.*Channel Created: (?P<value>.*)')

    #  Provisional State: Initiated and open
    p3 = re.compile(r'.*Provisional State: (?P<value>.*)')

    #  Operational state: Available
    p4 = re.compile(r'.*Operational state: (?P<value>.*)')

    #  Channel to hub: FALSE
    p5 = re.compile(r'.*Channel to hub: (?P<value>.*)')

    #  Interface Id: 17
    p6 = re.compile(r'.*Interface Id: (?P<value>.*)')

    #  Supports Zero-SLA: Yes
    p7 = re.compile(r'.*Supports Zero-SLA: (?P<value>.*)')

    #  Muted by Zero-SLA: No
    p8 = re.compile(r'.*Muted by Zero-SLA: (?P<value>.*)')

    #  Estimated Channel Egress Bandwidth: 983 Kbps
    p9 = re.compile(r'.*Estimated Channel Egress Bandwidth: (?P<value>.*)')

    #  Immitigable Events Summary:
    p10 = re.compile(r'.*Immitigable Events Summary:')

    #  Total Performance Count: 0, Total BW Count: 0
    p11 = re.compile(r'.*Total Performance Count: (?P<performance_count>\d+).*Total BW Count: (?P<bw_count>\d+)')

    #  ODE Statistics:
    p12 = re.compile(r'.*ODE Statistics:')

    #  Received: 73
    p13 = re.compile(r'.*Received: (?P<value>\S*$)')

    #  ODE Stats Bucket Number: 1
    p14 = re.compile(r'.*ODE Stats Bucket Number: (?P<value>.*)')

    #  Latest TCA Bucket
    p15 = re.compile(r'.*Latest TCA Bucket')

    #  Last Updated  : 19:46:23 ago
    p16 = re.compile(r'.*Last Updated\s*:\s*(?P<value>.*)')

    #  Packet Count  : 561
    p17 = re.compile(r'.*Packet Count\s*:\s*(?P<value>.*)')

    #  Byte Count    : 45009
    p18 = re.compile(r'.*Byte Count\s*:\s*(?P<value>.*)')

    #  One Way Delay : 250 msec*
    p19 = re.compile(r'.*One Way Delay\s*:\s*(?P<value>.*)')

    #  Loss Rate Pkts: 7.13 %
    p20 = re.compile(r'.*Loss Rate Pkts\s*:\s*(?P<value>.*)')

    #  Loss Rate Byte: 0.0 %
    p21 = re.compile(r'.*Loss Rate Byte\s*:\s*(?P<value>.*)')

    #  Jitter Mean   : 21306 usec
    p22 = re.compile(r'.*Jitter Mean\s*:\s*(?P<value>.*)')

    #  Unreachable   : FALSE
    p23 = re.compile(r'.*Unreachable\s*:\s*(?P<value>.*)')

    #  Unreachability: FALSE
    p23_1 = re.compile(r'.*Unreachability\s*:\s*(?P<value>.*)')

    #  TCA Statistics:
    p24 = re.compile(r'.*TCA Statistics:')

    #  Received: 148 ; Processed: 75 ; Unreach_rcvd: 148 ; Local Unreach_rcvd: 21
    p25 = re.compile(r'.*Received: (?P<received>\d+).*Processed: (?P<processed>\d+).*Unreach_rcvd: (?P<unreach_rcvd>\d+).*Local Unreach_rcvd: (?P<local_unreach_rvcd>\d+)')

    #  TCA lost byte rate: 0
    p26 = re.compile(r'.*TCA lost byte rate: (?P<value>.*)')

    #  TCA lost packet rate: 0
    p27 = re.compile(r'.*TCA lost packet rate: (?P<value>.*)')

    #  TCA one-way-delay: 0
    p28 = re.compile(r'.*TCA one-way-delay: (?P<value>.*)')

    #  TCA network-delay: 0
    p29 = re.compile(r'.*TCA network-delay: (?P<value>.*)')

    #  TCA jitter mean: 0
    p30 = re.compile(r'.*TCA jitter mean: (?P<value>.*)')

    # 0 or 1 flags
    ode_stats_bucket_number_flag = 0
    tca_stats_flag = 0
    latest_tca_bucket_flag = 0

    # Init vars
    parsed_dict = {}


    out = open(file, "r")
    for line in out:
        #print(line)
        if len(line.strip()) == 0: continue

        line = line.strip()

        m = p1.match(line)

        if m:
            channel_id = m.group('channel_id')
            dst_site_dscp = m.group('dscp')
            dst_site_id = m.group('dst_site_id')
            link_name = m.group('link_name')

            #parsed_dict[dst_site_prefix] = {}

            if channel_id not in parsed_dict:
                parsed_dict[channel_id] = {}
                channel_dict = parsed_dict[channel_id]


            # Init keys
            channel_dict['dscp'] = dst_site_dscp
            channel_dict['dst_site_id'] = dst_site_id
            channel_dict['link_name'] = link_name
            channel_dict['channel_created'] = ''
            channel_dict['provisional_state'] = ''
            channel_dict['operational_state'] = ''
            channel_dict['channel_to_hub'] = ''
            channel_dict['interface_id'] = ''
            channel_dict['supports_zero_sla'] = ''
            channel_dict['muted_zero_sla'] = ''
            channel_dict['estimated_channel_egress_bandwidth'] = ''
            channel_dict['ode_stats_bucket_number'] = {}
            ode_stats_bucket_number_flag = 0
            latest_tca_bucket_flag = 0

            continue

        #  Channel Created: 4d07h ago
        m = p2.match(line)
        if m:
            channel_dict['channel_created'] = m.group('value')

        #  Provisional State: Initiated and open
        m = p3.match(line)
        if m:
            channel_dict['provisional_state'] = m.group('value')

        #  Operational state: Available
        m = p4.match(line)
        if m:
            channel_dict['operational_state'] = m.group('value')

        #  Channel to hub: FALSE
        m = p5.match(line)
        if m:
            channel_dict['channel_to_hub'] = m.group('value')

        #  Interface Id: 17
        m = p6.match(line)
        if m:
            channel_dict['interface_id'] = m.group('value')

        #  Supports Zero-SLA: Yes
        m = p7.match(line)
        if m:
            channel_dict['supports_zero_sla'] = m.group('value')

        #  Muted by Zero-SLA: No
        m = p8.match(line)
        if m:
            channel_dict['muted_zero_sla'] = m.group('value')

        #  Estimated Channel Egress Bandwidth: 0 Kbps
        m = p9.match(line)
        if m:
            channel_dict['estimated_channel_egress_bandwidth'] = m.group('value')

        #  Estimated Channel Egress Bandwidth: 0 Kbps
        m = p9.match(line)
        if m:
            channel_dict['estimated_channel_egress_bandwidth'] = m.group('value')

        #  Immitigable Events Summary:
        m = p10.match(line)
        if m:
            channel_dict['immitigable_events_summary'] = {}

        #  Total Performance Count: 0, Total BW Count: 0
        m = p11.match(line)
        if m:
            channel_dict['immitigable_events_summary']['total_perfomance_count'] = m.group('performance_count')
            channel_dict['immitigable_events_summary']['total_bw_count'] = m.group('bw_count')

        #  ODE Statistics
        m = p13.match(line)
        if m:
            channel_dict['ode_received_stats'] = m.group('value')

        #  ODE Stats Bucket Number: 1
        m = p14.match(line)
        if m:

            ode_stats_bucket_number_value = m.group('value')
            channel_dict['ode_stats_bucket_number'][ode_stats_bucket_number_value] = {}
            ode_stats_bucket_number_dict = channel_dict['ode_stats_bucket_number'][ode_stats_bucket_number_value]
            ode_stats_bucket_number_flag = 1


        if ode_stats_bucket_number_flag:
            #  Last Updated  : 19:46:23 ago
            m = p16.match(line)
            if m:
                ode_stats_bucket_number_dict['last_updated'] = m.group('value')

            #  Packet Count  : 561
            m = p17.match(line)
            if m:
                ode_stats_bucket_number_dict['packet_count'] = m.group('value')

            #  Byte Count    : 45009
            m = p18.match(line)
            if m:
                ode_stats_bucket_number_dict['byte_count'] = m.group('value')

            #  One Way Delay : 250 msec*
            m = p19.match(line)
            if m:
                ode_stats_bucket_number_dict['one_way_delay'] = m.group('value')

            #  Loss Rate Pkts: 7.13 %
            m = p20.match(line)
            if m:
                ode_stats_bucket_number_dict['loss_rate_pkts'] = m.group('value')

            #  Loss Rate Byte: 0.0 %
            m = p21.match(line)
            if m:
                ode_stats_bucket_number_dict['loss_rate_bytes'] = m.group('value')

            #  Jitter Mean   : 21306 usec
            m = p22.match(line)
            if m:
                ode_stats_bucket_number_dict['jitter_mean'] = m.group('value')

            #  Unreachable   : FALSE
            m = p23.match(line)
            if m:
                ode_stats_bucket_number_dict['unreachable'] = m.group('value')



        #  Latest TCA Bucket
        m = p15.match(line)
        if m:
            channel_dict['latest_tca_bucket'] = {}
            ode_stats_bucket_number_flag = 0
            latest_tca_bucket_flag = 1

        if latest_tca_bucket_flag:
            #  Last Updated  : 19:46:23 ago
            m = p16.match(line)
            if m and latest_tca_bucket_flag:
                channel_dict['latest_tca_bucket']['last_updated'] = m.group('value')

            #  One Way Delay : 250 msec*
            m = p19.match(line)
            if m:
                channel_dict['latest_tca_bucket']['one_way_delay'] = m.group('value')

            #  Loss Rate Pkts: 7.13 %
            m = p20.match(line)
            if m:
                channel_dict['latest_tca_bucket']['loss_rate_pkts'] = m.group('value')

            #  Loss Rate Byte: 0.0 %
            m = p21.match(line)
            if m:
                channel_dict['latest_tca_bucket']['loss_rate_bytes'] = m.group('value')

            #  Jitter Mean   : 21306 usec
            m = p22.match(line)
            if m:
                channel_dict['latest_tca_bucket']['jitter_mean'] = m.group('value')

            #  Unreachable   : FALSE
            m = p23_1.match(line)
            if m:
                channel_dict['latest_tca_bucket']['unreachability'] = m.group('value')

        #  TCA Statistics:
        m = p24.match(line)
        if m:
            channel_dict['tca_stats'] = {}

        #  Received: 148 ; Processed: 75 ; Unreach_rcvd: 148 ; Local Unreach_rcvd: 21
        m = p25.match(line)
        if m:
            channel_dict['tca_stats']['received'] = m.group('received')
            channel_dict['tca_stats']['processed'] = m.group('processed')
            channel_dict['tca_stats']['unreach_rcvd'] = m.group('unreach_rcvd')
            channel_dict['tca_stats']['local_unreach_rvcd'] = m.group('local_unreach_rvcd')

        #  TCA lost byte rate: 0
        m = p26.match(line)
        if m:
            channel_dict['tca_stats']['lost_byte_rate'] = m.group('value')

        #  TCA lost packet rate: 0
        m = p27.match(line)
        if m:
            channel_dict['tca_stats']['lost_packet_rate'] = m.group('value')

        #  TCA one-way-delay: 0
        m = p28.match(line)
        if m:
            channel_dict['tca_stats']['one-way-delay'] = m.group('value')

        #  TCA network-delay: 0
        m = p29.match(line)
        if m:
            channel_dict['tca_stats']['network-delay'] = m.group('value')

        #  TCA jitter mean: 0
        m = p30.match(line)
        if m:
            channel_dict['tca_stats']['jitter_mean'] = m.group('value')
    return parsed_dict


channel_data = channel(channel_file)
class_data = iwanclass(class_file, channel_data)

print(json.dumps(class_data))
