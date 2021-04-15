import serial

be_testcase = []
cp_case_func_dict = {
    '主叫主挂': 'test_calling_to_answer',
    '主叫被挂': 'test_caller_hangs_up',
    '主叫拒接': 'test_call_reject',
    '主叫未接': 'test_call_no_answer',
}
# 公用串口
ser = serial.Serial(baudrate=115200)
# 控制textbrowser是否接收AT
test_flag = False
# 配置
call_process = []
real_holdtime = 0
testing_caseName = ""
testcase_sum = 0
already_testcase = 0
waittest_testcase = testcase_sum - already_testcase
pass_case = 0
fail_case = 0
