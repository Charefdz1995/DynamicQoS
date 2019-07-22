import json

from QoSmonitor.models import application


def output_references_device(device):

    device_dct = json.loads(device.to_json(indent=2))
    del(device_dct['_id'])
    device_dct["interfaces"] = [
    json.loads(interface.to_json(indent=2)) for interface in device.interfaces]
    for interf in device_dct["interfaces"]:
        del(interf['_id'])

    return json.dumps(device_dct,indent=4)
    



def output_references_link(link):
        link_dct = json.loads(link.to_json(indent=2))
        del (link_dct['_id'])
        link_dct["from_device"] = json.loads(output_references_device_brief(link.from_device))
        link_dct["to_interface"] = json.loads(link.to_interface.to_json(indent=2))
        del (link_dct["to_interface"]['_id'])
        link_dct["from_interface"] = json.loads(link.from_interface.to_json(indent=2))
        del (link_dct["from_interface"]['_id'])
        link_dct["to_device"] = json.loads(output_references_device_brief(link.to_device))

        return json.dumps(link_dct, indent=4)


def output_references_topology(topology):
    topology_dct = json.loads(topology.to_json(indent=2))
    del (topology_dct['_id'])
    topology_dct["devices"] = [
        json.loads(output_references_device(device)) for device in topology.devices
    ]
    topology_dct["links"] = [
        json.loads(output_references_link(link)) for link in topology.links
    ]

    return json.dumps(topology_dct, indent=4)

def output_references_topology_brief(topology):
    topology_dct = json.loads(topology.to_json(indent=2))
    del (topology_dct['_id'])
    del (topology_dct['devices'])
    del (topology_dct['links'])

    return json.dumps(topology_dct, indent=4)

def output_references_device_brief(device):

    device_dct = json.loads(device.to_json(indent=2))
    del(device_dct['_id'])
    device_dct["interfaces"] = [
    json.loads(interface.to_json(indent=2)) for interface in device.interfaces]
    del(device_dct['interfaces'])

    return json.dumps(device_dct,indent=4)

def output_references_ip_sla_info(ip_sla_info):
        ip_sla_info_dct = json.loads(ip_sla_info.to_json(indent=2))
        del (ip_sla_info_dct['_id'])
        del (ip_sla_info_dct['ip_sla_ref'])

        return json.dumps(ip_sla_info_dct, indent=4)


def output_references_ip_sla(ip_sla):
    ip_sla_dct = json.loads(ip_sla.to_json(indent=2))
    ip_sla_dct["sender_device_ref"] = json.loads(output_references_device_brief(ip_sla.sender_device_ref))
    ip_sla_dct["responder_device_ref"] = json.loads(output_references_device_brief(ip_sla.responder_device_ref))
    del (ip_sla_dct['_id'])

    return json.dumps(ip_sla_dct, indent=4)


def get_application_by_id(app_id):
    try:
        return application.objects.get(application_ID=app_id).application_NAME
    except:
        return str(app_id)


def output_references_flow_field(flow_field):
    flow_field_dct = json.loads(flow_field.to_json(indent=2))
    flow_field_dct["device"] = json.loads(output_references_device_brief(flow_field.device))
    flow_field_dct["input_int"] = str(flow_field.input_int.interface_name)
    flow_field_dct["output_int"] = str(flow_field.output_int.interface_name)
    del (flow_field_dct['_id'])
    del (flow_field_dct['flow'])
    return json.dumps(flow_field_dct, indent=4)


def output_references_flow(flow, flow_fields):
    flow_dct = json.loads(flow.to_json(indent=2))
    flow_dct["ip_sla_ref"] = json.loads(output_references_ip_sla(flow.ip_sla_ref))
    flow_dct["application_ID"] = str(get_application_by_id(flow.application_ID))
    del (flow_dct['_id'])
    del (flow_dct['ip_sla_ref'])
    flow_dct["flow_fields"] = [
        json.loads(output_references_flow_field(fl_feild)) for fl_feild in flow_fields
    ]

    return json.dumps(flow_dct, indent=4)


def ouput_topology_id(topology):
    topology_dct = json.loads(topology.to_json(indent=2))

    topology_dct['id']=topology_dct['_id']['$oid']
    del (topology_dct['_id'])
    del (topology_dct['devices'])
    del (topology_dct['links'])
    del (topology_dct['topology_desc'])

    return json.dumps(topology_dct, indent=4)


def ouput_device_id(device):
    device_dct = json.loads(device.to_json(indent=2))
    device_dct['id'] = device_dct['_id']['$oid']
    del (device_dct['_id'])
    del (device_dct['interfaces'])
    del (device_dct['management'])
    del (device_dct['is_responder'])


    return json.dumps(device_dct, indent=4)

def ouput_interface_id(interface):
    interface_dct = json.loads(interface.to_json(indent=2))
    interface_dct['id'] = interface_dct['_id']['$oid']
    del (interface_dct['_id'])
    del (interface_dct['interface_index'])
    del (interface_dct['interface_address'])
    del (interface_dct['interface_speed'])
    del (interface_dct['interface_prefixlen'])
    del (interface_dct['ingress'])



    return json.dumps(interface_dct, indent=4)

def output_flow_table_print(nt_field, ip_sla_i):
        rslt = []
        rslt.append(nt_field.flow.flow_id)
        rslt.append(nt_field.device.hostname)
        rslt.append(nt_field.input_int.interface_name)
        rslt.append(nt_field.output_int.interface_name)
        rslt.append(get_application_by_id(nt_field.flow.application_ID))
        rslt.append(nt_field.flow.ipv4_src_addr)
        rslt.append(nt_field.flow.transport_src_port)
        rslt.append(nt_field.flow.ipv4_dst_addr)
        rslt.append(nt_field.flow.transport_dst_port)
        rslt.append(nt_field.flow.type_of_service)
        rslt.append(nt_field.flow.ipv4_protocol)
        rslt.append(nt_field.counter_bytes)
        rslt.append(nt_field.counter_pkts)
        rslt.append(nt_field.bandwidth)

        try:
            rslt.append(ip_sla_i.avg_delay)
        except:
            rslt.append('Not Available')
        try:
            rslt.append(ip_sla_i.avg_jitter)
        except:
            rslt.append('Not Available')
        try:
            rslt.append(ip_sla_i.packet_loss)
        except:
            rslt.append('Not Available')

        return json.dumps(rslt, indent=4)





