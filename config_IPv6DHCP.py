from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException


cisco_device = {
    'device_type': 'cisco_ios',  
    'host': '192.168.11.1',       
    'username': 'admin',         
    'password': '040745', 
    'secret': '7538',     
}

vlan_list = [12,13,14,15]

try:
    net_connect = ConnectHandler(**cisco_device)
    
    net_connect.enable()
    net_connect.config_mode()


    for vlan in vlan_list:
        commands = [
            f'ipv6 dhcp pool VLAN{vlan}_IPV6_POOL',
            f'address prefix 2001:db8:{vlan}::/64',
            f'dns-server 2001:4860:4860::8888',
            'domain-name testnet.com',
            f'interface vlan {vlan}'
            f'ipv6 dhcp server VLAN{vlan}_IPV6_POOL'
            'ipv6 nd managed-config-flag'
            'ipv6 nd other-config-flag'
        ]
        output = net_connect.send_config_set(commands)
        print(output)
    routing_output = net_connect.send_command('ipv6 unicast-routing')
    print(routing_output)
    net_connect.disconnect()

except NetMikoTimeoutException:
    print("Timeout occurred while trying to connect to the device.")
except NetMikoAuthenticationException:
    print("Authentication failed. Please check your username/password.")
except Exception as e:
    print(f"An unexpected error occurred: {str(e)}")
