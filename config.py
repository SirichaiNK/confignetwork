from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException


SW1 = {
    'device_type': 'cisco_ios',  
    'host': '192.168.99.1',       
    'username': 'admin',         
    'password': '6410110503', 
    'secret': '12345',     
}

SW2 = {
    'device_type': 'cisco_ios',  
    'host': '192.168.100.1',       
    'username': 'admin',         
    'password': '6410110503', 
    'secret': '12345',     
}

config_data = {
    "SW1_vlan_list" : [20,30,40],
    "SW1_ports" : ['eth0/1','eth0/2', 'eth0/3'],
    "SW2_vlan_list" : [12,13,14,15],
    "SW2_ports" : ['eth1/0','eth1/1','eth1/2', 'eth1/3']
}
Switch_list = [SW1, SW2]

for i in range(len(Switch_list)):
    n = 0
    try:
        net_connect = ConnectHandler(**Switch_list[i])
        
        net_connect.enable()
        net_connect.config_mode()


        for vlan in config_data[f'SW{i+1}_vlan_list']:
            commands = [
                f'vlan {vlan}',
                f'int vlan {vlan}',
                f'ip addr 192.168.{vlan}.1 255.255.255.0',
                'no sh',
                'exit',
                f'int {f'SW{i+1}_port'[n]}',
                f'switchport mode access',
                f'switchport access vlan {vlan}',
                'no sh'
            ]
            n += 1
            output = net_connect.send_config_set(commands)
            print(output)
        net_connect.disconnect()

    except NetMikoTimeoutException:
        print("Timeout occurred while trying to connect to the device.")
    except NetMikoAuthenticationException:
        print("Authentication failed. Please check your username/password.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
