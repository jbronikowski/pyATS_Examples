import re
import pprint

import json

# Dst-Site-Prefix: 10.225.76.164/32    DSCP: default [0] Traffic class id:59827542
dst_site_prefix_re = re.compile(r'Dst-Site-Prefix:\s*(?P<dst_site_prefix>\S+)\s*DSCP:\s*(?P<dscp>\S*)')

#  Clock Time:                 14:16:10 (CDT) 08/05/2019
clock_time_re = re.compile(r'\S*Clock\s*Time:\s*(?P<clock_time>.*)')

#  TC Learned:                 4w2d ago
tc_learned_re = re.compile(r'\S*TC\s*Learned:\s*(?P<tc_learned>.*)')

#  Present State:              CONTROLLED
present_state_re = re.compile(r'\S*Present\s*State:\s*(?P<present_state>.*)')

#  Current Performance Status: in-policy
current_performance_status_re = re.compile(r'\S*Current\s*Performance\s*Status:\s*(?P<current_performance_status>.*)')

#  Current Service Provider:   ISP2 since 09:39:28
current_service_provider_re =   re.compile(r'\S*Current\s*Service\s*Provider:\s*(?P<current_service_provider>.*)')

#  Previous Service Provider:  ISP1 pfr-label: 0:0 | 0:0 [0x0] for 180 sec
previous_service_provider_re = re.compile(r'\S*Previous\s*Service\s*Provider:\s*(?P<previous_service_provider>.*)')

#  BW Used:                    0 Kbps
bw_used_re = re.compile(r'\S*BW\s*Used:\s*(?P<bw_used>.*)')

#  Present WAN interface:      Tunnel200 in Border 10.1.0.104
present_wan_interface_re = re.compile(r'\S*Present\s*WAN\s*interface:\s*(?P<present_wan_interface>\S*)\s*in\sBorder\s(?P<border>.*)')

#  Present Channel (primary):  12488652 ISP2 pfr-label:0:0 | 0:0 [0x0]
present_channel_re = re.compile(r'\S*Present\s*Channel\s*\(primary\):\s*(?P<present_channel>.*)')

#  Backup Channel:             12488653 ISP1 pfr-label:0:0 | 0:0 [0x0]
backup_channel_re = re.compile(r'\S*Backup\s*Channel:\s*(?P<backup_channel>.*)')

#  Destination Site ID bitmap: 0
dst_site_id_bit_re = re.compile(r'\S*Destination\s*Site\s*ID\s*bitmap:\s*(?P<dst_site_id_bit>.*)')

#  Destination Site ID:        10.50.0.84
dst_site_id_re = re.compile(r'\S*Destination\s*Site\s*ID:\s*(?P<dst_site_id>.*)')

#  Class-Sequence in use:      20
class_sequence_re = re.compile(r'\S*Class-Sequence\s*in\s*use:\s*(?P<class_sequence_in_use>.*)')

#  Class Name:                 BEST_EFFORT using policy User-defined
class_name_re = re.compile(r'\S*Class\s*Name:\s*(?P<class_name>\S*)')
    #priority 2 packet-loss-rate threshold 40.0 percent
    #priority 2 byte-loss-rate threshold 40.0 percent
priority_re = re.compile(r'(?P<priority>priority\s[1-9])\s*(?P<detail>\S*)\s*(?P<type>\S*)\s*(?P<value>.*)')

#  BW Updated:                 00:00:26 ago
bw_updated_re = re.compile(r'\S*BW\s*Updated:\s*(?P<bw_updated>.*)')

#  Reason for Latest Route Change:    Backup to Primary path preference transition

#  Route Change History:
route_change_indicator_re = re.compile(r'Date and Time')


#  1:  04:36:42 (CDT) 08/05/19   ISP1(0:0|0:0)/10.1.0.101/Tu100 (Ch:12488653)       ISP2(0:0|0:0)/10.1.0.104/Tu200 (Ch:12488652)       Backup to Primary path preference transition
#  2:  04:33:42 (CDT) 08/05/19   ISP2(0:0|0:0)/10.1.0.104/Tu200 (Ch:12488652)       ISP1(0:0|0:0)/10.1.0.101/Tu100 (Ch:12488653)       Unreachable
#  3:  02:23:41 (CDT) 08/05/19   ISP1(0:0|0:0)/10.1.0.101/Tu100 (Ch:12488653)       ISP2(0:0|0:0)/10.1.0.104/Tu200 (Ch:12488652)       Backup to Primary path preference transition
#  4:  02:20:39 (CDT) 08/05/19   ISP2(0:0|0:0)/10.1.0.104/Tu200 (Ch:12488652)       ISP1(0:0|0:0)/10.1.0.101/Tu100 (Ch:12488653)       Unreachable
#  5:  02:10:21 (CDT) 08/03/19   ISP1(0:0|0:0)/10.1.0.101/Tu100 (Ch:12488653)       ISP2(0:0|0:0)/10.1.0.104/Tu200 (Ch:12488652)       Backup to Primary path preference transition
route_change_re = re.compile(r'\s*(\d:)\s*(?P<date>\S*\s*\S*\s*\S*)\s*(?P<previous_exit>\S*\s*\S*)\s*(?P<current_exit>\S*\s*\S*)\s*(?P<reason>.*)')


# 0 or 1 flags
class_priority_flag = 0
route_change_flag = 0

# Init vars
parsed_dict = {}
class_index = 0
class_name = ''


out = open("testfile.txt", "r")


for line in out:
    if len(line.strip()) == 0: continue

    line = line.strip()

    result = dst_site_prefix_re.match(line)

    if result:
        dst_site_prefix = result.group('dst_site_prefix')
        dst_site_dscp = result.group('dscp')

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

    result = clock_time_re.match(line)

    if result:
        traffic_classes_dict['clock_time'] = result.group('clock_time')
        continue

    result = tc_learned_re.match(line)

    if result:
        traffic_classes_dict['tc_learned'] = result.group('tc_learned')
        continue

    result = present_state_re.match(line)

    if result:
        traffic_classes_dict['present_state'] = result.group('present_state')
        continue

    result = current_performance_status_re.match(line)

    if result:
        traffic_classes_dict['current_performance_status'] = result.group('current_performance_status')
        continue

    result = current_service_provider_re.match(line)

    if result:
        traffic_classes_dict['current_service_provider'] = result.group('current_service_provider')
        continue

    result = previous_service_provider_re.match(line)

    if result:
        traffic_classes_dict['previous_service_provider'] = result.group('previous_service_provider')
        continue

    result = bw_used_re.match(line)

    if result:
        traffic_classes_dict['bandwidth']['used'] = result.group('bw_used')
        continue

    result = bw_updated_re.match(line)

    if result:
        traffic_classes_dict['bandwidth']['updated'] = result.group('bw_updated')
        continue

    result = present_wan_interface_re.match(line)

    if result:
        traffic_classes_dict['present_wan_interface']['tunnel'] = result.group('present_wan_interface')
        traffic_classes_dict['present_wan_interface']['border'] = result.group('border')
        continue

    result = present_channel_re.match(line)

    if result:
        traffic_classes_dict['channel']['present'] = result.group('present_channel')
        continue

    result = backup_channel_re.match(line)

    if result:
        traffic_classes_dict['channel']['backup'] = result.group('backup_channel')
        continue

    result = dst_site_id_bit_re.match(line)

    if result:
        traffic_classes_dict['dst_site_id_bit'] = result.group('dst_site_id_bit')
        continue

    result = dst_site_id_re.match(line)

    if result:
        traffic_classes_dict['dst_site_id'] = result.group('dst_site_id')
        continue

    result = class_sequence_re.match(line)

    if result:
        traffic_classes_dict['class_sequence_in_use'] = result.group('class_sequence_in_use')
        continue

    result = class_name_re.match(line)

    if result:
        class_name = result.group('class_name')
        traffic_classes_dict['class_name'][class_name] = {}
        continue

    result = priority_re.match(line)

    if result:
        traffic_classes_dict['class_name'][class_name]['priority'] = result.group('priority')
        traffic_classes_dict['class_name'][class_name]['detail'] = result.group('detail')
        traffic_classes_dict['class_name'][class_name]['type'] = result.group('type')
        traffic_classes_dict['class_name'][class_name]['value'] = result.group('value')
        continue


    result = route_change_indicator_re.match(line)

    if result:
        route_change_flag = 1
        continue

    if route_change_flag:
        result = route_change_re.match(line)

        if result:
            route_change_dict = {}
            route_change_dict['date'] = result.group('date')
            route_change_dict['previous_exit'] = result.group('previous_exit')
            route_change_dict['current_exit'] = result.group('current_exit')
            route_change_dict['reason'] = result.group('reason')
            traffic_classes_dict['route_change_history'].append(route_change_dict)
            continue





r = json.dumps(parsed_dict)

print(r)

pp = pprint.PrettyPrinter(width=75
 , compact=True)
#pp.pprint(parsed_dict)
