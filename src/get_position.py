
class TestApp(TestWrapper, TestClient):
    def __init__(self, ipaddress, portid, clientid):
        TestWrapper.__init__(self)
        TestClient.__init__(self, wrapper=self)

        self.connect(ipaddress, portid, clientid)

if __name__ == '__main__':
    ##    ## Check that the port is the same as on the Gateway    

    ### ipaddress is 127.0.0.1 if one same machine, clientid is arbitrary
    app = TestApp("127.0.0.1", 7496, 10)
