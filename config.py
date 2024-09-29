from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException


cisco_device = {
    'device_type': 'cisco_ios',  
    'host': '192.168.1.1',       
    'username': 'admin',         
    'password': '040745', 
    'secret': '7538',     
}

vlan_list = [11,12,13,14,15]

try:
    # เชื่อมต่อกับอุปกรณ์
    net_connect = ConnectHandler(**cisco_device)
    
    # เข้าสู่ enable mode
    net_connect.enable()
    net_connect.config_mode()

    # คำสั่งหลายคำสั่งในรูปแบบลิสต์
    for vlan in vlan_list:
        commands = [
            f'vlan {vlan}',
            #f'vlan {input('vlan name :')}',
            f'int vlan {vlan}',
            f'ip addr 192.168.{vlan}.1 255.255.255.0',
            'no sh',
            'end'
        ]

    # ส่งคำสั่งทั้งหมดทีเดียว
    output = net_connect.send_config_set(commands)

    # ปิดการเชื่อมต่อ
    net_connect.disconnect()

    # แสดงผลลัพธ์การสั่งการ
    print(output)

except NetMikoTimeoutException:
    print("Timeout occurred while trying to connect to the device.")
except NetMikoAuthenticationException:
    print("Authentication failed. Please check your username/password.")
except Exception as e:
    print(f"An unexpected error occurred: {str(e)}")
