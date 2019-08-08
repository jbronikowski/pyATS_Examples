import re
import json

file = 'class.txt'

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
    if len(line.strip()) == 0: continue

    line = line.strip()

    # Dst-Site-Prefix: 10.225.76.164/32    DSCP: default [0] Traffic class id:59827542
    m = p1.match(line)
    if m:
        dst_site_prefix = m.group('dst_site_prefix')
        dst_site_dscp = m.group('dscp')

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

    #  Clock Time:                 14:16:10 (CDT) 08/05/2019
    m = p2.match(line)
    if m:
        traffic_classes_dict['clock_time'] = m.group('clock_time')
        continue

    #  TC Learned:                 4w2d ago
    m = p3.match(line)
    if m:
        traffic_classes_dict['tc_learned'] = m.group('tc_learned')
        continue
    #  Present State:              CONTROLLED
    m = p4.match(line)

    if m:
        traffic_classes_dict['present_state'] = m.group('present_state')
        continue
    #  Current Performance Status: in-policy
    m = p5.match(line)

    if m:
        traffic_classes_dict['current_performance_status'] = m.group('current_performance_status')
        continue
    #  Current Service Provider:   ISP2 since 09:39:28
    m = p6.match(line)

    if m:
        traffic_classes_dict['current_service_provider'] = m.group('current_service_provider')
        continue
    #  Previous Service Provider:  ISP1 pfr-label: 0:0 | 0:0 [0x0] for 180 sec
    m = p7.match(line)

    if m:
        traffic_classes_dict['previous_service_provider'] = m.group('previous_service_provider')
        continue
    #  BW Used:                    0 Kbps
    m = p8.match(line)

    if m:
        traffic_classes_dict['bandwidth']['used'] = m.group('bw_used')
        continue

    #  BW Updated:                 00:00:26 ago
    m = p17.match(line)
    if m:
        traffic_classes_dict['bandwidth']['updated'] = m.group('bw_updated')
        continue

    #  Present WAN interface:      Tunnel200 in Border 10.1.0.104
    m = p9.match(line)
    if m:
        traffic_classes_dict['present_wan_interface']['tunnel'] = m.group('present_wan_interface')
        traffic_classes_dict['present_wan_interface']['border'] = m.group('border')
        continue

    #  Present Channel (primary):  12488652 ISP2 pfr-label:0:0 | 0:0 [0x0]
    m = p10.match(line)
    if m:
        traffic_classes_dict['channel']['present'] = m.group('present_channel')
        #traffic_classes_dict['channel']['present'] = channel_data[m.group('present_channel')]
        continue

    #  Backup Channel:             12488653 ISP1 pfr-label:0:0 | 0:0 [0x0]
    m = p11.match(line)
    if m:
        traffic_classes_dict['channel']['backup'] = m.group('backup_channel')
        #  traffic_classes_dict['channel']['backup'] = channel_data[m.group('backup_channel')]
        continue

    #  Destination Site ID bitmap: 0
    m = p12.match(line)
    if m:
        traffic_classes_dict['dst_site_id_bit'] = m.group('dst_site_id_bit')
        continue

    #  Destination Site ID:        10.50.0.84
    m = p13.match(line)
    if m:
        traffic_classes_dict['dst_site_id'] = m.group('dst_site_id')
        continue

    #  Class-Sequence in use:      20
    m = p14.match(line)
    if m:
        traffic_classes_dict['class_sequence_in_use'] = m.group('class_sequence_in_use')
        continue

    #  Class Name:                 BEST_EFFORT using policy User-defined
    m = p15.match(line)
    if m:
        class_name = m.group('class_name')
        traffic_classes_dict['class_name'][class_name] = {}
        continue
    #  priority 2 packet-loss-rate threshold 40.0 percent
    m = p16.match(line)
    if m:
        traffic_classes_dict['class_name'][class_name]['priority'] = m.group('priority')
        traffic_classes_dict['class_name'][class_name]['detail'] = m.group('detail')
        traffic_classes_dict['class_name'][class_name]['type'] = m.group('type')
        traffic_classes_dict['class_name'][class_name]['value'] = m.group('value')
        continue

    #  Route Change History:
    m = p18.match(line)
    if m:
        route_change_flag = 1
        continue

    if route_change_flag:
        #  1:  04:36:42 (CDT) 08/05/19   ISP1(0:0|0:0)/10.1.0.101/Tu100 (Ch:12488653)       ISP2(0:0|0:0)/10.1.0.104/Tu200 (Ch:12488652)       Backup to Primary path preference transition
        m = p19.match(line)
        if m:
            route_change_dict = {}
            route_change_dict['date'] = m.group('date')
            route_change_dict['previous_exit'] = m.group('previous_exit')
            route_change_dict['current_exit'] = m.group('current_exit')
            route_change_dict['reason'] = m.group('reason')
            traffic_classes_dict['route_change_history'].append(route_change_dict)
            continue


print(json.dumps(parsed_dict))
