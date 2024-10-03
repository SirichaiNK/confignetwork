from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException


SW1 = {
    'device_type': 'cisco_ios',  
    'host': '192.168.1.1',       
    'username': 'admin',         
    'password': '040745', 
    'secret': '7538',     
}

SW2 = {
    'device_type': 'cisco_ios',  
    'host': '192.168.11.1',       
    'username': 'admin',         
    'password': '040745', 
    'secret': '7538',     
}

Switch_list = [SW1, SW2]

for Switch in Switch_list:
    try:
        net_connect = ConnectHandler(**Switch)
        
        net_connect.enable()
        output = net_connect.send_command('show run')
        print(output)
        net_connect.disconnect()

    except NetMikoTimeoutException:
        print("Timeout occurred while trying to connect to the device.")
    except NetMikoAuthenticationException:
        print("Authentication failed. Please check your username/password.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
