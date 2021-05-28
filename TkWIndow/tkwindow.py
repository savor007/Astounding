from tkinter import *
import time
from queue import Queue


LOG_LINE_NUM = 0
radar_queue=Queue()
lidar_queue=Queue()
can_queue=Queue()

class MY_GUI():
    def __init__(self,init_window, lidar_task_queue=None, radar_task_queue=None, can_task_queue=None):
        self.lidar_queue=lidar_task_queue
        self.radar_queue=radar_task_queue
        self.can_queue=can_task_queue
        self.init_window_name = init_window


    #设置窗口
    def set_init_window(self):
        self.init_window_name.title("ECU Simulator")           #窗口名
        #self.init_window_name.geometry('320x160+10+10')                         #290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name.geometry('1920x1080+10+10')
        #self.init_window_name["bg"] = "pink"                                    #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        #self.init_window_name.attributes("-alpha",0.9)                          #虚化，值越小虚化程度越高
        #标签
        self.lidar_data_label = Label(self.init_window_name, text="lidar")
        self.lidar_data_label.grid(row=0, column=0)
        self.radar_data_label = Label(self.init_window_name, text="radar")
        self.radar_data_label.grid(row=0, column=12)
        self.can_data_label = Label(self.init_window_name, text="CAN")
        self.can_data_label.grid(row=0, column=24)


        #文本框
        self.lidar_data_Text = Text(self.init_window_name, width=68, height=49)  #原始数据录入框
        self.lidar_data_Text.grid(row=1, column=0, rowspan=10, columnspan=10)
        self.radar_data_Text = Text(self.init_window_name, width=68, height=49)  #处理结果展示
        self.radar_data_Text.grid(row=1, column=12, rowspan=10, columnspan=10)
        self.can_data_Text = Text(self.init_window_name, width=68, height=49)  # 日志框
        self.can_data_Text.grid(row=1, column=24, columnspan=10)
  


    def clear_content(self):
        self.lidar_data_Text.delete(1.0,END)
        self.radar_data_Text.delete(1.0, END)
        self.can_data_Text.delete(1.0,END)



    def update(self):
        str=""
        print("--------------------queue size"+str(self.lidar_queue.qsize()+"-------"))
        if self.lidar_queue.qsize() > 0:
            str=self.lidar_queue.get_nowait()+"\n"
            self.lidar_data_Text.insert(END, str)
            self.lidar_queue.task_done()
        if self.radar_queue.qsize() > 0:
            str=self.radar_queue.get_nowait()+"\n"
            self.radar_data_Text.insert(END, str)
            self.radar_queue.task_done()
        if self.can_queue.qsize() > 0:
            str=self.can_queue.get_nowait()+"\n"
            self.can_data_Text.insert(END, str)
            self.can_queue.task_done()
        self.init_window_name.after(5, self.update)


    def print_lidar_data(self, lidar_str):
        #current_index=self.lidar_data_Text.index()
        self.lidar_data_Text.insert(END, lidar_str)



    def print_can_data(self, can_str):
        #current_index=self.can_data_Text.index()
        self.can_data_Text.insert(END, can_str)


    def print_radar_data(self, radar_str):
        #current_index=self.radar_data_Text.index()
        self.lidar_radar_Text.insert(END, radar_str)


#gui_start()
if __name__ == "__main__":
    init_window = Tk()              #实例化出一个父窗口
    ecu_simulator_ui = MY_GUI(init_window, lidar_queue,radar_queue,can_queue)
    # 设置根窗口默认属性
    ecu_simulator_ui.set_init_window()
    ecu_simulator_ui.clear_content()
    init_window.after(10, ecu_simulator_ui.update)
    ecu_simulator_ui.update()
    ######################################
    init_window.mainloop()
