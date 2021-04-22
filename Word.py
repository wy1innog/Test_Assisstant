import serial

# 待测用例
be_testcase = []
log = []
# tree下按钮对象存储
tree_btn_Dict = {}

# 串口
ser = serial.Serial(baudrate=115200)

# 测试，log接收状态
test_flag = False
recv_flag = True
pause_flag = False

# 配置
call_process = []
real_holdtime = 0
testing_caseName = ""
testcase_sum = 0
already_testcase = 0
waittest_testcase = testcase_sum - already_testcase
pass_case = 0
fail_case = 0

