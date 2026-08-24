#!/usr/bin/env python3
import os
os.environ["PATH"] = "/home/genxianghu/miniconda3/bin:/home/genxianghu/.local/bin:" + os.environ.get("PATH", "")
# -*- coding: utf-8 -*-
"""
通用单片机烧录工具
支持: STM32 / GD32 / TI / 51单片机 全系列
"""

import os
import sys
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

# ========== 默认固件路径（可修改）==========
DEFAULT_HEX_PATH = ""

# ========== 芯片数据库（全系列）==========
CHIPS = {
    # ========== STM32 系列 ==========
    "STM32F030C8": {"target": "stm32f030rc", "type": "arm", "pack": None},
    "STM32F051C8": {"target": "stm32f051rc", "type": "arm", "pack": None},
    "STM32F072RB": {"target": "stm32f072rb", "type": "arm", "pack": None},
    "STM32F103C8": {"target": "stm32f103rc", "type": "arm", "pack": None},
    "STM32F103RB": {"target": "stm32f103rc", "type": "arm", "pack": None},
    "STM32F103VE": {"target": "stm32f103rc", "type": "arm", "pack": None},
    "STM32F107VC": {"target": "stm32f107vc", "type": "arm", "pack": None},
    "STM32F205RC": {"target": "stm32f205rc", "type": "arm", "pack": None},
    "STM32F207VC": {"target": "stm32f207vc", "type": "arm", "pack": None},
    "STM32F303CC": {"target": "stm32f303rc", "type": "arm", "pack": None},
    "STM32F303RE": {"target": "stm32f303rc", "type": "arm", "pack": None},
    "STM32F334C8": {"target": "stm32f334rc", "type": "arm", "pack": None},
    "STM32F401CC": {"target": "stm32f401rc", "type": "arm", "pack": None},
    "STM32F407VE": {"target": "stm32f407ve", "type": "arm", "pack": "Keil.STM32F4xx_DFP"},
    "STM32F407VG": {"target": "stm32f407vg", "type": "arm", "pack": "Keil.STM32F4xx_DFP"},
    "STM32F407ZG": {"target": "stm32f407zg", "type": "arm", "pack": "Keil.STM32F4xx_DFP"},
    "STM32F429ZI": {"target": "stm32f429zi", "type": "arm", "pack": None},
    "STM32F446RE": {"target": "stm32f446rc", "type": "arm", "pack": None},
    "STM32F746ZG": {"target": "stm32f746zg", "type": "arm", "pack": None},
    "STM32F767ZI": {"target": "stm32f767zi", "type": "arm", "pack": None},
    "STM32G071RB": {"target": "stm32g071rb", "type": "arm", "pack": None},
    "STM32G0B1RE": {"target": "stm32g0b1re", "type": "arm", "pack": None},
    "STM32G431RB": {"target": "stm32g431rb", "type": "arm", "pack": None},
    "STM32G474RE": {"target": "stm32g474re", "type": "arm", "pack": None},
    "STM32H743ZI": {"target": "stm32h743zi", "type": "arm", "pack": None},
    "STM32H750VB": {"target": "stm32h750vb", "type": "arm", "pack": None},
    "STM32H7A3ZI": {"target": "stm32h7a3zi", "type": "arm", "pack": None},
    "STM32L072RB": {"target": "stm32l072rb", "type": "arm", "pack": None},
    "STM32L073RZ": {"target": "stm32l073rz", "type": "arm", "pack": None},
    "STM32L152RE": {"target": "stm32l152re", "type": "arm", "pack": None},
    "STM32L476RG": {"target": "stm32l476rg", "type": "arm", "pack": None},
    "STM32L496ZG": {"target": "stm32l496zg", "type": "arm", "pack": None},
    "STM32L552ZE": {"target": "stm32l552ze", "type": "arm", "pack": None},
    "STM32U575ZI": {"target": "stm32u575zi", "type": "arm", "pack": None},
    "STM32WB55RG": {"target": "stm32wb55rg", "type": "arm", "pack": None},
    "STM32WL55JC": {"target": "stm32wl55jc", "type": "arm", "pack": None},
    "STM32MP157C": {"target": "stm32mp157c", "type": "arm", "pack": None},

    # ========== GD32 系列 ==========
    "GD32F103C8": {"target": "gd32f103c8", "type": "arm", "pack": "GigaDevice.GD32F1xx_DFP"},
    "GD32F103RB": {"target": "gd32f103rb", "type": "arm", "pack": "GigaDevice.GD32F1xx_DFP"},
    "GD32F103VB": {"target": "gd32f103vb", "type": "arm", "pack": "GigaDevice.GD32F1xx_DFP"},
    "GD32F107VC": {"target": "gd32f107vc", "type": "arm", "pack": "GigaDevice.GD32F1xx_DFP"},
    "GD32F130C8": {"target": "gd32f130c8", "type": "arm", "pack": "GigaDevice.GD32F1x0_DFP"},
    "GD32F150G8": {"target": "gd32f150g8", "type": "arm", "pack": "GigaDevice.GD32F1x0_DFP"},
    "GD32F205RC": {"target": "gd32f205rc", "type": "arm", "pack": "GigaDevice.GD32F2xx_DFP"},
    "GD32F207VC": {"target": "gd32f207vc", "type": "arm", "pack": "GigaDevice.GD32F2xx_DFP"},
    "GD32F303CC": {"target": "gd32f303cc", "type": "arm", "pack": "GigaDevice.GD32F3x0_DFP"},
    "GD32F305RC": {"target": "gd32f305rc", "type": "arm", "pack": "GigaDevice.GD32F30x_DFP"},
    "GD32F307VC": {"target": "gd32f307vc", "type": "arm", "pack": "GigaDevice.GD32F30x_DFP"},
    "GD32F330C8": {"target": "gd32f330c8", "type": "arm", "pack": "GigaDevice.GD32F3x0_DFP"},
    "GD32F350RB": {"target": "gd32f350rb", "type": "arm", "pack": "GigaDevice.GD32F3x0_DFP"},
    "GD32F405RG": {"target": "gd32f405rg", "type": "arm", "pack": "GigaDevice.GD32F4xx_DFP"},
    "GD32F407VE": {"target": "gd32f407ve", "type": "arm", "pack": "GigaDevice.GD32F4xx_DFP"},
    "GD32F407VG": {"target": "gd32f407vg", "type": "arm", "pack": "GigaDevice.GD32F4xx_DFP"},
    "GD32F450VI": {"target": "gd32f450vi", "type": "arm", "pack": "GigaDevice.GD32F4xx_DFP"},
    "GD32F470VE": {"target": "gd32f470ve", "type": "arm", "pack": "GigaDevice.GD32F4xx_DFP"},
    "GD32F470VG": {"target": "gd32f470vg", "type": "arm", "pack": "GigaDevice.GD32F4xx_DFP"},
    "GD32F470ZI": {"target": "gd32f470zi", "type": "arm", "pack": "GigaDevice.GD32F4xx_DFP"},
    "GD32E503RC": {"target": "gd32e503rc", "type": "arm", "pack": "GigaDevice.GD32E50x_DFP"},
    "GD32E507VE": {"target": "gd32e507ve", "type": "arm", "pack": "GigaDevice.GD32E50x_DFP"},
    "GD32E230C8": {"target": "gd32e230c8", "type": "arm", "pack": "GigaDevice.GD32E23x_DFP"},
    "GD32C113RB": {"target": "gd32c113rb", "type": "arm", "pack": "GigaDevice.GD32C11x_DFP"},
    "GD32VF103VBT6": {"target": "gd32vf103vbt6", "type": "arm", "pack": "GigaDevice.GD32VF103_DFP"},

    # ========== TI 系列 ==========
    "MSP432P401R": {"target": "msp432p401r", "type": "arm", "pack": None},
    "MSP432P4111": {"target": "msp432p4111", "type": "arm", "pack": None},
    "MSPM0G3507": {"target": "mspm0g3507", "type": "arm", "pack": "TI.MSPM0_DFP"},
    "MSPM0G3519": {"target": "mspm0g3519", "type": "arm", "pack": "TI.MSPM0_DFP"},
    "MSPM0L1306": {"target": "mspm0l1306", "type": "arm", "pack": "TI.MSPM0_DFP"},
    "MSPM0L1346": {"target": "mspm0l1346", "type": "arm", "pack": "TI.MSPM0_DFP"},
    "MSPM0C1104": {"target": "mspm0c1104", "type": "arm", "pack": "TI.MSPM0_DFP"},
    "MSPM0G1107": {"target": "mspm0g1107", "type": "arm", "pack": "TI.MSPM0_DFP"},
    "TM4C123GH6PM": {"target": "tm4c123gh6pm", "type": "arm", "pack": None},
    "TM4C1294NCPDT": {"target": "tm4c1294ncpdt", "type": "arm", "pack": None},
    "CC1310F128": {"target": "cc1310f128", "type": "arm", "pack": None},
    "CC1312R1F3": {"target": "cc1312r1f3", "type": "arm", "pack": None},
    "CC1350F128": {"target": "cc1350f128", "type": "arm", "pack": None},
    "CC1352R1F3": {"target": "cc1352r1f3", "type": "arm", "pack": None},
    "CC2640R2F": {"target": "cc2640r2f", "type": "arm", "pack": None},
    "CC2650F128": {"target": "cc2650f128", "type": "arm", "pack": None},
    "CC2652R1F": {"target": "cc2652r1f", "type": "arm", "pack": None},
    "CC3220SF": {"target": "cc3220sf", "type": "arm", "pack": None},
    "CC3235SF": {"target": "cc3235sf", "type": "arm", "pack": None},

    # ========== 51 单片机 ==========
    "STC89C52RC": {"target": "stc89c52rc", "type": "51", "pack": None},
    "STC89C58RD+": {"target": "stc89c58rd", "type": "51", "pack": None},
    "STC15W408AS": {"target": "stc15w408as", "type": "51", "pack": None},
    "STC15F2K60S2": {"target": "stc15f2k60s2", "type": "51", "pack": None},
    "STC8H8K64U": {"target": "stc8h8k64u", "type": "51", "pack": None},
    "STC8H3K64S4": {"target": "stc8h3k64s4", "type": "51", "pack": None},
    "STC12C5A60S2": {"target": "stc12c5a60s2", "type": "51", "pack": None},
    "STC32G12K128": {"target": "stc32g12k128", "type": "51", "pack": None},
}

PROBES = {
    "CMSIS-DAP (DAP-Link)": "daplink",
    "ST-Link": "stlink",
    "J-Link": "jlink",
    "51单片机-串口": "serial",
}

PACK_DIR = os.path.expanduser("~/.local/share/cmsis-pack-manager")


class FlasherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("通用单片机烧录工具")
        self.root.geometry("750x600")
        self.root.resizable(False, False)
        
        style = ttk.Style()
        style.configure("TButton", font=("Microsoft YaHei", 11))
        style.configure("TLabel", font=("Microsoft YaHei", 11))
        style.configure("TCombobox", font=("Microsoft YaHei", 10))
        
        # 厂商选择
        frame_vendor = ttk.Frame(root, padding=10)
        frame_vendor.pack(fill="x")
        ttk.Label(frame_vendor, text="厂商:").pack(side="left")
        self.vendor_var = tk.StringVar(value="全部")
        self.vendor_combo = ttk.Combobox(frame_vendor, textvariable=self.vendor_var,
                                          values=["全部", "STM32", "GD32", "TI", "51单片机"],
                                          width=12, state="readonly")
        self.vendor_combo.pack(side="left", padx=5)
        self.vendor_combo.bind("<<ComboboxSelected>>", self.on_vendor_change)
        
        # 固件文件选择
        frame1 = ttk.Frame(root, padding=10)
        frame1.pack(fill="x")
        ttk.Label(frame1, text="固件文件:").pack(side="left")
        self.file_var = tk.StringVar(value=DEFAULT_HEX_PATH)
        self.file_entry = ttk.Entry(frame1, textvariable=self.file_var, width=50)
        self.file_entry.pack(side="left", padx=5)
        ttk.Button(frame1, text="浏览...", command=self.browse_file).pack(side="left")
        
        # 芯片选择
        frame2 = ttk.Frame(root, padding=10)
        frame2.pack(fill="x")
        ttk.Label(frame2, text="目标芯片:").pack(side="left")
        self.chip_var = tk.StringVar()
        self.all_chips = list(CHIPS.keys())
        self.chip_combo = ttk.Combobox(frame2, textvariable=self.chip_var,
                                        values=self.all_chips, width=30, state="readonly")
        self.chip_combo.pack(side="left", padx=5)
        self.chip_combo.current(0)
        
        # 调试器选择
        ttk.Label(frame2, text="  调试器:").pack(side="left")
        self.probe_var = tk.StringVar()
        self.probe_combo = ttk.Combobox(frame2, textvariable=self.probe_var,
                                         values=list(PROBES.keys()), width=22, state="readonly")
        self.probe_combo.pack(side="left", padx=5)
        self.probe_combo.current(0)
        
        # 按钮区
        frame3 = ttk.Frame(root, padding=10)
        frame3.pack(fill="x")
        self.flash_btn = ttk.Button(frame3, text="开始烧录", command=self.start_flash, width=15)
        self.flash_btn.pack(side="left", padx=5)
        self.stop_btn = ttk.Button(frame3, text="停止", command=self.stop_flash, width=10, state="disabled")
        self.stop_btn.pack(side="left", padx=5)
        ttk.Button(frame3, text="清空日志", command=self.clear_log).pack(side="left", padx=5)
        
        # 日志输出
        frame4 = ttk.LabelFrame(root, text="烧录日志", padding=5)
        frame4.pack(fill="both", expand=True, padx=10, pady=5)
        self.log = scrolledtext.ScrolledText(frame4, wrap=tk.WORD, font=("Consolas", 10))
        self.log.pack(fill="both", expand=True)
        
        self.process = None
        self.log_message("通用单片机烧录工具已启动")
        self.log_message("支持: STM32 全系列 / GD32 全系列 / TI 全系列 / 51单片机")
        self.log_message("请选择固件文件、厂商、目标芯片和调试器，然后点击【开始烧录】")
        self.log_message("")
        
    def on_vendor_change(self, event=None):
        vendor = self.vendor_var.get()
        if vendor == "全部":
            chips = self.all_chips
        elif vendor == "TI":
            chips = [c for c in self.all_chips if c.startswith(("MSP", "TM4C", "CC"))]
        else:
            chips = [c for c in self.all_chips if c.startswith(vendor)]
        self.chip_combo.config(values=chips)
        if chips:
            self.chip_combo.current(0)
        else:
            self.chip_var.set("")
        
    def browse_file(self):
        path = filedialog.askopenfilename(
            title="选择固件文件",
            filetypes=[("HEX/BIN 文件", "*.hex *.bin"), ("所有文件", "*.*")]
        )
        if path:
            self.file_var.set(path)
    
    def log_message(self, msg):
        self.log.insert(tk.END, msg + "\n")
        self.log.see(tk.END)
        
    def clear_log(self):
        self.log.delete(1.0, tk.END)
        
    def start_flash(self):
        hex_path = self.file_var.get().strip()
        chip_name = self.chip_var.get()
        probe_name = self.probe_var.get()
        
        if not hex_path or not os.path.exists(hex_path):
            messagebox.showerror("错误", "请先选择有效的固件文件！")
            return
        if not chip_name:
            messagebox.showerror("错误", "请选择目标芯片！")
            return
            
        chip_info = CHIPS.get(chip_name)
        if not chip_info:
            messagebox.showerror("错误", f"未知芯片: {chip_name}")
            return
            
        probe_type = PROBES.get(probe_name, "daplink")
        
        self.flash_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.log_message(f"\n{'='*50}")
        self.log_message(f"目标芯片: {chip_name}")
        self.log_message(f"调试器: {probe_name}")
        self.log_message(f"固件: {hex_path}")
        self.log_message(f"{'='*50}\n")
        
        thread = threading.Thread(target=self._flash_thread, 
                                   args=(hex_path, chip_info, probe_type, chip_name))
        thread.daemon = True
        thread.start()
        
    def _flash_thread(self, hex_path, chip_info, probe_type, chip_name):
        try:
            if chip_info["type"] == "51":
                self._flash_51(hex_path, chip_info, chip_name)
            else:
                self._flash_arm(hex_path, chip_info, probe_type, chip_name)
        except Exception as e:
            self.log_message(f"错误: {str(e)}")
        finally:
            self.root.after(0, self._flash_done)
            
    def _flash_arm(self, hex_path, chip_info, probe_type, chip_name):
        result = subprocess.run(["which", "pyocd"], capture_output=True, text=True)
        if result.returncode != 0:
            self.log_message("错误: 未找到 pyocd，请先安装: pip install -U pyocd")
            return
            
        cmd = ["pyocd", "flash", "-t", chip_info["target"], "--connect", probe_type, "--frequency", "1000000", hex_path]
        
        if chip_info.get("pack"):
            pack_name = chip_info["pack"]
            pack_file = self._find_pack(pack_name)
            if pack_file:
                cmd = ["pyocd", "flash", "--pack", pack_file, "-t", chip_info["target"], 
                       "--connect", probe_type, "--frequency", "1000000", hex_path]
            else:
                self.log_message(f"未找到 {pack_name}，尝试自动下载...")
                self.log_message("执行: pyocd pack install " + pack_name)
                install = subprocess.run(["pyocd", "pack", "install", pack_name], 
                                         capture_output=True, text=True)
                self.log_message(install.stdout or install.stderr)
                pack_file = self._find_pack(pack_name)
                if pack_file:
                    cmd = ["pyocd", "flash", "--pack", pack_file, "-t", chip_info["target"],
                           "--connect", probe_type, "--frequency", "1000000", hex_path]
                else:
                    self.log_message("警告: Pack 下载失败，尝试无 Pack 烧录...")
        
        self.log_message(f"执行命令: {' '.join(cmd)}\n")
        
        self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                        text=True, bufsize=1)
        for line in self.process.stdout:
            self.root.after(0, lambda l=line.strip(): self.log_message(l))
        self.process.wait()
        
        if self.process.returncode == 0:
            self.log_message("\n烧录成功！")
        else:
            self.log_message(f"\n烧录失败 (返回码: {self.process.returncode})")
            
    def _flash_51(self, hex_path, chip_info, chip_name):
        result = subprocess.run(["which", "stcgal"], capture_output=True, text=True)
        if result.returncode != 0:
            self.log_message("错误: 51单片机需要 stcgal，请先安装:")
            self.log_message("   pip install stcgal")
            return
            
        try:
            import serial.tools.list_ports
            ports = [p.device for p in serial.tools.list_ports.comports() if p.device.startswith("/dev/tty")]
        except:
            ports = []
            
        if not ports:
            self.log_message("错误: 未找到串口，请连接 USB 转串口模块")
            return
            
        port = ports[0]
        self.log_message(f"检测到串口: {port}")
        
        proto = "stc89"
        if "STC15" in chip_name: proto = "stc15"
        elif "STC8" in chip_name: proto = "stc8"
        elif "STC12" in chip_name: proto = "stc12"
        elif "STC32" in chip_name: proto = "stc32"
        
        cmd = ["stcgal", "-P", proto, "-p", port, "-b", "115200", hex_path]
        
        self.log_message(f"执行命令: {' '.join(cmd)}\n")
        self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                        text=True, bufsize=1)
        for line in self.process.stdout:
            self.root.after(0, lambda l=line.strip(): self.log_message(l))
        self.process.wait()
        
        if self.process.returncode == 0:
            self.log_message("\n烧录成功！")
        else:
            self.log_message(f"\n烧录失败 (返回码: {self.process.returncode})")
            
    def _find_pack(self, pack_name):
        # 1. 先搜索 cmsis-pack-manager 的标准目录结构
        for root, dirs, files in os.walk(PACK_DIR):
            if pack_name.replace(".", "_") in root or pack_name in root:
                for f in files:
                    if f.endswith(".pack"):
                        return os.path.join(root, f)
        # 2. 再搜索 packs 目录下的直接存放的 .pack 文件
        packs_dir = os.path.join(PACK_DIR, "packs")
        if os.path.isdir(packs_dir):
            for f in os.listdir(packs_dir):
                if f.endswith(".pack") and pack_name.replace(".", "_") in f.replace(".", "_"):
                    return os.path.join(packs_dir, f)
        return None
        
    def _flash_done(self):
        self.flash_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.process = None
        
    def stop_flash(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.log_message("\n已停止烧录")
            self._flash_done()


def create_desktop_icon(script_path):
    desktop_dirs = [os.path.expanduser("~/桌面"), os.path.expanduser("~/Desktop")]
    icon_path = os.path.join(os.path.dirname(script_path), "hammer.png")
    
    try:
        from PIL import Image, ImageDraw
        img = Image.new('RGBA', (256, 256), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse([8, 8, 248, 248], fill=(255, 140, 0, 255), outline=(200, 90, 0, 255), width=5)
        draw.rectangle([68, 82, 192, 128], fill=(210, 210, 215, 255), outline=(160, 160, 165, 255), width=3)
        draw.rectangle([38, 88, 68, 122], fill=(210, 210, 215, 255), outline=(160, 160, 165, 255), width=2)
        draw.rectangle([192, 88, 222, 122], fill=(210, 210, 215, 255), outline=(160, 160, 165, 255), width=2)
        draw.rectangle([118, 128, 148, 215], fill=(170, 120, 70, 255), outline=(130, 90, 50, 255), width=3)
        img.save(icon_path)
    except ImportError:
        icon_path = "utilities-terminal"
    
    desktop_content = f"""[Desktop Entry]
Name=通用烧录工具
Comment=单片机固件烧录工具
Exec=python3 {script_path}
Icon={icon_path}
Type=Application
Terminal=false
Categories=Development;Electronics;
"""
    
    for d in desktop_dirs:
        if os.path.isdir(d):
            desktop_file = os.path.join(d, "universal-flasher.desktop")
            with open(desktop_file, 'w') as f:
                f.write(desktop_content)
            os.chmod(desktop_file, 0o755)
            print(f"桌面快捷方式已创建: {desktop_file}")
    
    app_dir = os.path.expanduser("~/.local/share/applications")
    os.makedirs(app_dir, exist_ok=True)
    app_file = os.path.join(app_dir, "universal-flasher.desktop")
    with open(app_file, 'w') as f:
        f.write(desktop_content)
    os.chmod(app_file, 0o755)
    print(f"应用菜单快捷方式已创建: {app_file}")
    
    subprocess.run(["update-desktop-database", app_dir], capture_output=True)
    print("全部完成！可以在桌面或开始菜单中找到【通用烧录工具】")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--install":
        create_desktop_icon(os.path.abspath(__file__))
        sys.exit(0)
        
    root = tk.Tk()
    app = FlasherGUI(root)
    root.mainloop()
