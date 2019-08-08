import re
import json

file = 'channel.txt'

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

    if len(line.strip()) == 0: continue

    line = line.strip()

    # Channel Id: 13383058  Dst Site-Id: 10.50.3.60  Link Name: ISP2  DSCP: default [0] pfr-label: 0:0 | 0:0 [0x0] TCs: 5  BackupTCs: 0
    m = p1.match(line)

    if m:
        channel_id = m.group('channel_id')
        dst_site_dscp = m.group('dscp')
        dst_site_id = m.group('dst_site_id')
        link_name = m.group('link_name')

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


print(json.dumps(parsed_dict))
