import unittest
from selenium_support import selenium_support
import time
import sys
import HtmlTestRunner
from os import path

"""
This is actual testcase file for your selenium project.
it uses python unitTest framework to create testcases.

Best practicse 
1. copy this file instead of editing it, this will makesure you have blueprint of testcase design with you.
you can create mutiple python files representing multiple test suite. eg sanity suite,regression suite etc.

2. do not change below menthods 
    1. setupClass- required to set up browsers 
    2.TearDownClass- close the browsers
    3. main method- this is to set up html report and execute testcases in file

3. as per unittest framwork, you need to create testcase in a method which start with word test
   eg-test_signin_testcase(self) , these are dummy test cases you can edit as per your testcases.

4. since browser driver is managed by selenium_support class, which enables cross browser testing. refer to driver object as cls.support.driver or self.support.driver
5. for screenshot use take_screenshot from support library 

"""

class Test_ATT(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        #time.sleep(80)
        cls.support=selenium_support()
        retry =5
        while retry:
            
            
            url="https://www.att.com"
            try:
                cls.support.init()
                if cls.support.driver:
                    cls.support.driver.get(url)
                    cls.support.take_screenshot('att.png')
                    print(cls.support.driver.capabilities)
                    break
            except:    
                retry=retry -1
                print("connection failed retry pending ",retry)
                time.sleep(10) 
        if retry == 0:
            cls.assertEqual(1,2,"Failed to connect to browser")
        

    def test_signin_testcase(self):
        print(self.support.driver.capabilities)
        time.sleep(5)
        account=self.support.driver.find_element_by_xpath("//span[@id='z1-profile-text' and .='Account']")
        account.click()
        self.support.take_screenshot('login.png')
        print("Account clicked")

        time.sleep(15)

        signin=self.support.driver.find_element_by_xpath('//span[ .="Sign in"]')
        signin.click()

        time.sleep(10)
        print(self.support.driver.find_element_by_xpath('//h1[@id="signInHeaderText"]').text +" visible")

        userid=self.support.driver.find_element_by_xpath("//input[@id='userID']")
        userid.send_keys('sp634u')

        password=self.support.driver.find_element_by_xpath("//input[@id='password']")
        password.send_keys('sp634u')

        signin_button=self.support.driver.find_element_by_xpath("//button[@id='signin']")
        signin_button.click()
        time.sleep(10)

        sign_in_check=self.support.driver.find_element_by_xpath("//h1[@class='bad-request-header mb-0 mt-3']")
        print(sign_in_check.text)


    def test_click_Pay_without_signing_in(self):
        self.support.driver.get("https://www.att.com")

        time.sleep(1)
        account=self.support.driver.find_element_by_xpath("//span[@id='z1-profile-text' and .='Account']")
        account.click()
        print("Account clicked")
        self.support.take_screenshot('payment.png')
        time.sleep(12)
        Pay_without_signing_in=self.support.driver.find_element_by_xpath("//span[.='Pay without signing in']")
        Pay_without_signing_in.click()
        time.sleep(10)
        enter_ph_number=self.support.driver.find_element_by_xpath("//input[@name='Active AT&T phone number']")
        enter_ph_number.send_keys('12345678')
        print("phone number entered")
        cancel_button=self.support.driver.find_element_by_xpath("//button[@aria-label='Cancel']")
        cancel_button.click()
        print("Cancel button clicked")


    def test_Internet_order(self):
        # //span[@class='z1-tier1-text' and .='TV']
        self.support.driver.get("https://www.att.com")

        time.sleep(10)
        click_internet=self.support.driver.find_element_by_xpath("//span[@class='z1-tier1-text' and .='Internet']")
        click_internet.click()
        self.support.take_screenshot('internet.png')
        print("Internet clciked")
        time.sleep(15)
        click_Check_availability=self.support.driver.find_element_by_xpath('//a[@title="Check availability"]')
        click_Check_availability.click()
    

    @classmethod
    def tearDownClass(cls):
        cls.support.driver.quit()    

        
def main(out = sys.stderr, verbosity = 2): 
    loader = unittest.TestLoader() 
    #import os

    #module=os.path.splitext(os.path.basename(__file__))[0]
    #suite = loader.loadTestsFromName(module+'.TestCases.test_b')
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    print(suite)
    #unittest.TextTestRunner(out, verbosity = verbosity).run(suite) 
    #output_file = open("HTML_Test_Runner_ReportTest.txt", "w")
    if path.exists("/tmp"):
        report_filder='/tmp/report'
    else:
        report_filder='./report'

    html_runner = HtmlTestRunner.HTMLTestRunner(
        #    stream=output_file,
            report_title='HTML Reporting using PyUnit',
            descriptions='HTML Reporting using PyUnit & HTMLTestRunner',
            output=report_filder
        )
    #unittest.TestRunner()
    html_runner.run(suite)


if __name__ == "__main__":
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', action='store', dest='config_value',help='Store a simple value')
    results = parser.parse_args()
    print ('config_value     =', results.config_value)
    Test_Zypher.config=results.config_value
    #unittest.main(verbosity=2)
    """
    
    #time.sleep(30)
    main()
    #with open('testing.out', 'w') as f: 
    #    main(f)
