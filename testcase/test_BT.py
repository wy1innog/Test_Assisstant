import pytest


@pytest.fixture(scope='function')
def open_BT():
    print("open BT")


def test_BT_onoff():
    BT = 'on'
    assert BT == 'on'


def test_BT_connect(open_BT, BT_name=123):
    assert BT_name == "hello"

    def _bt_status(self):
        # 1:open  0:close

        flag = subprocess_getoutput('adb -s %s shell settings get global bluetooth_on' % dev()).strip()
        self.log.debug("Bluetooth status: %s" % flag)
        if '1' in flag:
            return True
        elif '0' in flag:
            return False
        else:
            self.TextBrowser_AP_recv.append("Bluetooth status error")
            self.log.warning("Bluetooth status error, flag=%s" % flag)

    def bt_status(self):
        """
        AP 打印蓝牙开关状态
        :return: None
        """
        self.log.info("######>>> Bluetooth status")
        if dev() != 0:
            if self._bt_status():
                self.TextBrowser_AP_recv.append("蓝牙状态: 开启\n")
            else:
                self.TextBrowser_AP_recv.append("蓝牙状态: 关闭\n")
        else:
            self.TextBrowser_AP_recv.append("无设备连接")


if __name__ == '__main__':
    pytest.main(['-v -s', 'test_BT.py'])
