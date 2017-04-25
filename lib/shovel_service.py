from lib.rackhd_service import RackHDClient
import lib.ironic_service as ironic_service
import json


def register(user_entry):
    info = extra = {}
    if user_entry.get('driver') == 'pxe_ipmitool':
        info = {
            'ipmi_address': user_entry.get('ipmihost'),
            'ipmi_username': user_entry.get('ipmiuser'),
            'ipmi_password': user_entry.get('ipmipass'),
            'deploy_kernel': user_entry.get('kernel'),
            'deploy_ramdisk': user_entry.get('ramdisk')
        }
    else:
        return {'err': 'driver not supported'}, 403

    # Fill in the extra meta data with some failover and event data
    extra = {
        'nodeid': user_entry.get('uuid'),
        'name': user_entry.get('name'),
        'lsevents': {'time': 0},
        'eventcnt': 0,
        'failover': user_entry.get('failovernode'),
        'eventre': user_entry.get('eventre'),
        'timer': {}
    }

    # Properties
    rackhd = RackHDClient()
    rackhd_node = user_entry.get('uuid')
    try:
        propreties = {
            'cpus': rackhd.get_node_cpu(rackhd_node),
            'memory_mb': rackhd.get_node_memory_size(rackhd_node),
            'local_gb': rackhd.get_node_disk_size(rackhd_node)
        }
    except Exception as err:
        return {'err': err.message}, 404

    # Finally setup the node info, properties and extra
    node = {'name': user_entry.get('uuid'),
            'driver': user_entry.get('driver'),
            'driver_info': info,
            'properties': propreties,
            'extra': extra}
    try:
        ironic_node = ironic_service.create_node(**node)
        # Set port
        port = {'address': user_entry.get('port'), 'node_uuid': ironic_node.uuid}
        ironic_service.create_port(**port)
    except Exception as err:
        return err

    return {'message': 'success'}, 201


def unregister(uuid):
    try:
        ironic_service.delete_node(uuid)
    except Exception as err:
        return err
    return '', 204
