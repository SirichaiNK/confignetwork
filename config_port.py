from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException


cisco_device = {
    'device_type': 'cisco_ios',  
    'host': '192.168.11.1',       
    'username': 'admin',         
    'password': '040745', 
    'secret': '7538',     
}

port_list = ['eth1/0','eth1/1','eth1/2','eth1/3']
vlan_list = [11,12,13,14,15]

try:
    net_connect = ConnectHandler(**cisco_device)
    
    net_connect.enable()
    net_connect.config_mode()


    for port in port_list:
        vlan = 1
        commands = [
            f'ip dhcp pool {vlan_list[vlan]}',
            f'network 192.168.{vlan_list[vlan]}.0 255.255.255.0'
            f'default-router 192.168.{vlan_list[vlan]}.1'
            'dns-server 8.88.8',
            f'int {port}',
            'switchport mode access',
            f'switchport access vlan {vlan_list[vlan]}',
            f'ip addr 192.168.{vlan_list[vlan]}.1 255.255.255.0',
            'no sh',
        ]
        vlan += 1
        output = net_connect.send_config_set(commands)
        print(output)
    net_connect.disconnect()

except NetMikoTimeoutException:
    print("Timeout occurred while trying to connect to the device.")
except NetMikoAuthenticationException:
    print("Authentication failed. Please check your username/password.")
except Exception as e:
    print(f"An unexpected error occurred: {str(e)}")
