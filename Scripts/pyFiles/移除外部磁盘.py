#!/usr/bin/env python3

import os
import time
import subprocess
import platform

def get_external_drives_macos():
    """获取 macOS 系统中的所有外部磁盘设备"""
    drives = []
    
    # 首先尝试直接使用 diskutil list external 命令
    result = subprocess.run(['diskutil', 'list', 'external'], capture_output=True, text=True)
    
    if result.returncode == 0 and result.stdout.strip():
        lines = result.stdout.strip().split('\n')
        for line in lines:
            if line.startswith('/dev/disk'):
                disk_id = line.split()[0]
                drives.append(disk_id)
    
    # 如果上面方法没找到外部设备，尝试检查所有非系统磁盘
    if not drives:
        list_result = subprocess.run(['diskutil', 'list'], capture_output=True, text=True)
        if list_result.returncode == 0:
            lines = list_result.stdout.strip().split('\n')
            for line in lines:
                if line.startswith('/dev/disk'):
                    disk_id = line.split()[0]
                    # 排除系统磁盘
                    if disk_id == '/dev/disk0':
                        continue
                    
                    info_result = subprocess.run(['diskutil', 'info', disk_id], capture_output=True, text=True)
                    if info_result.returncode == 0:
                        info_text = info_result.stdout.lower()
                        
                        # 检查是否为外部设备的各种特征
                        is_external = 'internal: no' in info_text
                        has_external_protocol = any(proto in info_text for proto in ['protocol: usb', 'protocol: thunderbolt', 'protocol: firewire', 'protocol: sdcard'])
                        is_ejectable = 'ejectable: yes' in info_text
                        
                        if is_external or has_external_protocol or is_ejectable:
                            drives.append(disk_id)
    
    # 最后检查是否还有遗漏的已挂载外部卷
    mount_result = subprocess.run(['mount'], capture_output=True, text=True)
    if mount_result.returncode == 0:
        for line in mount_result.stdout.strip().split('\n'):
            if '/dev/disk' in line and '/dev/disk0' not in line:
                parts = line.split()
                for part in parts:
                    if part.startswith('/dev/disk'):
                        # 如果这个设备还没在列表中，检查是否为外部设备
                        if part not in drives:
                            info_result = subprocess.run(['diskutil', 'info', part], capture_output=True, text=True)
                            if info_result.returncode == 0:
                                info_text = info_result.stdout.lower()
                                if 'internal: no' in info_text or 'protocol: usb' in info_text:
                                    drives.append(part)
    
    return drives

def get_drive_info_macos(drive_path):
    """获取 macOS 驱动器的信息"""
    result = subprocess.run(['diskutil', 'info', drive_path], capture_output=True, text=True)
    
    info = {'path': drive_path, 'name': 'Unknown', 'size': 'Unknown', 'type': 'Unknown', 'volume_name': None}
    
    if result.returncode == 0:
        output_text = result.stdout
        
        # 查找分区卷名
        found_volume_name = False
        
        # 首先检查这个驱动器是否有分区
        partition_info = subprocess.run(['diskutil', 'list', drive_path], capture_output=True, text=True)
        if partition_info.returncode == 0:
            partition_lines = partition_info.stdout.strip().split('\n')
            for line in partition_lines:
                if 'NAME' in line and 'TYPE' in line:  # 找到标题行
                    continue
                parts = line.strip().split()
                if len(parts) >= 3 and ':' not in parts[0]:  # 避开标题行和设备行
                    # 在分区信息后面查找名称
                    name_start_idx = line.find('NAME')
                    if name_start_idx != -1:
                        name_part = line[name_start_idx:].split()[1:]
                        if name_part:
                            # 组合可能的多词名称
                            volume_name = ' '.join(name_part)
                            if volume_name and volume_name != '':
                                info['volume_name'] = volume_name
                                info['name'] = volume_name
                                found_volume_name = True
                                break
                    elif len(parts) >= 3:
                        # 尝试查找名称（不同格式）
                        possible_name = parts[-1]
                        if possible_name and possible_name != '-':
                            info['volume_name'] = possible_name
                            info['name'] = possible_name
                            found_volume_name = True
                            break
        
        # 如果分区没有找到名称，尝试从disk info中查找
        if not found_volume_name:
            for line in output_text.split('\n'):
                # 尝试获取卷名
                if 'Volume Name:' in line:
                    name = line.split(':', 1)[1].strip()
                    if name and name != '':
                        info['name'] = name
                        info['volume_name'] = name
                        found_volume_name = True
                        break
                        
            if not found_volume_name:
                # 如果没有卷名，尝试获取媒体名称
                for line in output_text.split('\n'):
                    if 'Media Name:' in line:
                        name = line.split(':', 1)[1].strip()
                        if name and name != '':
                            info['name'] = name
                            break
                    # 或者使用设备名
                    elif 'Device / Media Name:' in line:
                        name = line.split(':', 1)[1].strip()
                        if name and name != '':
                            info['name'] = name
                            break
        
        # 获取磁盘大小
        for line in output_text.split('\n'):
            if 'Disk Size:' in line:
                info['size'] = line.split(':', 1)[1].strip()
                break
                
        # 获取设备类型
        for line in output_text.split('\n'):
            if 'Protocol:' in line:
                info['type'] = line.split(':', 1)[1].strip()
                break
            
        # 如果仍然没有名称，使用磁盘ID作为名称
        if info['name'] == 'Unknown':
            info['name'] = drive_path
            
    return info

def eject_drive_macos(drive_path):
    """在 macOS 上弹出外部磁盘"""
    result = subprocess.run(['diskutil', 'eject', drive_path], capture_output=True, text=True)
    return result.returncode == 0, result.stdout.strip()

def debug_disk_detection():
    """调试磁盘检测"""
    print("===== 调试信息 =====")
    print("所有磁盘列表:")
    all_disks = subprocess.run(['diskutil', 'list'], capture_output=True, text=True)
    print(all_disks.stdout)
    
    print("\n外部磁盘列表:")
    ext_disks = subprocess.run(['diskutil', 'list', 'external'], capture_output=True, text=True)
    print(ext_disks.stdout)
    
    print("\n检测到的外部驱动器:")
    external = get_external_drives_macos()
    print(external)
    
    if external:
        print("\n外部驱动器详细信息:")
        for drive in external:
            info = get_drive_info_macos(drive)
            print(f"- {drive}: {info['name']} ({info['size']}, {info['type']})")
    
    print("==================\n")

def get_display_name(info):
    """获取更好的显示名称"""
    # 如果有卷名，直接使用卷名
    if info['volume_name'] and info['volume_name'] != 'Unknown':
        return info['volume_name']
    # 否则使用设备名称
    return info['name']

def main():
    system = platform.system()
    
    if system != 'Darwin':
        print(f"此脚本当前仅支持 macOS 系统，检测到您的系统为: {system}")
        return
    
    print("正在检测外部磁盘...")
    
    # 运行一次调试检测
    debug_disk_detection()
    
    prev_drives = set()
    
    # 检查用户权限
    try:
        test_run = subprocess.run(['diskutil', 'list'], capture_output=True, text=True)
        if test_run.returncode != 0:
            print(f"执行diskutil命令失败，可能需要管理员权限，请尝试使用sudo运行此脚本: {test_run.stderr}")
            return
    except Exception as e:
        print(f"执行命令时出错: {str(e)}")
        return
    
    try:
        while True:
            try:
                current_drives = set(get_external_drives_macos())
                
                # 检测新插入的外部磁盘
                new_drives = current_drives - prev_drives
                for drive in new_drives:
                    info = get_drive_info_macos(drive)
                    display_name = get_display_name(info)
                    print(f"\n发现新外部磁盘: {display_name} ({info['size']})")
                    print(f"设备路径: {info['path']}")
                    print(f"设备类型: {info['type']}")
                
                # 检测移除的外部磁盘
                removed_drives = prev_drives - current_drives
                for drive in removed_drives:
                    print(f"\n外部磁盘 {drive} 已被移除")
                
                # 更新已知驱动器列表
                prev_drives = current_drives
                
                # 如果有外部磁盘连接，显示菜单
                if current_drives:
                    print("\n当前连接的外部磁盘:")
                    drive_list = list(current_drives)
                    for i, drive in enumerate(drive_list, 1):
                        info = get_drive_info_macos(drive)
                        display_name = get_display_name(info)
                        print(f"{i}. {display_name} ({info['size']}) - {info['path']}")
                    
                    print("\n选项:")
                    print("数字键 - 选择对应磁盘进行弹出")
                    print("e - 弹出所有外部磁盘并退出") # 新增选项
                    print("r - 刷新磁盘列表")
                    print("d - 运行调试检测")
                    print("q - 退出程序")
                    
                    choice = input("\n请选择: ")
                    
                    if choice == 'q':
                        print("程序已退出")
                        break
                    elif choice == 'r':
                        print("正在刷新磁盘列表...")
                        continue
                    elif choice == 'd':
                        debug_disk_detection()
                        continue
                    elif choice == 'e': # 新增处理逻辑
                        print("正在尝试弹出所有外部磁盘...")
                        all_ejected = True
                        failed_drives = []
                        for drive in drive_list:
                            info = get_drive_info_macos(drive)
                            display_name = get_display_name(info)
                            print(f"  正在弹出: {display_name} ({drive})...")
                            success, message = eject_drive_macos(drive)
                            if success:
                                print(f"  成功弹出: {display_name}")
                            else:
                                print(f"  弹出失败: {display_name} - {message}")
                                all_ejected = False
                                failed_drives.append(display_name)
                        
                        if all_ejected:
                            print("所有外部磁盘已成功弹出。程序退出。")
                        else:
                            print(f"部分磁盘未能弹出: {', '.join(failed_drives)}")
                            print("程序退出。")
                        break # 无论成功与否都退出

                    elif choice.isdigit() and 1 <= int(choice) <= len(drive_list):
                        selected_drive = drive_list[int(choice) - 1]
                        info = get_drive_info_macos(selected_drive)
                        display_name = get_display_name(info)
                        print(f"正在弹出: {display_name} ({selected_drive})...")
                        
                        success, message = eject_drive_macos(selected_drive)
                        if success:
                            print(f"成功弹出外部磁盘: {display_name}")
                            
                            # 检查是否弹出了最后一个磁盘
                            remaining_drives = set(get_external_drives_macos())
                            if not remaining_drives:
                                print("已弹出最后一个外部磁盘，程序将自动退出...")
                                time.sleep(1)
                                break
                        else:
                            print(f"弹出失败: {message}")
                    else:
                        print("无效的选择，请重试")
                else:
                    print("\r没有检测到外部磁盘，等待插入...", end="")
                
                time.sleep(2)
            except Exception as e:
                print(f"发生错误: {str(e)}")
                time.sleep(2)
    
    except KeyboardInterrupt:
        print("\n程序已退出")

if __name__ == "__main__":
    main()