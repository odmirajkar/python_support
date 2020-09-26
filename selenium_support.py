"""
class to support selenium projects accepting the command line parameter
@Auther - OnkarM
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.remote_connection import RemoteConnection
import argparse
from os import environ
import sys
import os



class selenium_support():
    """
    Main class support selenium

    """
    def __init__(self):
        """
        Constructor for class. 
        add required arguments 
        """
        self.parser = argparse.ArgumentParser(description='CAP Selenium support library')
        self.parser.add_argument('--browser', type=str,default='Chrome', help='Browser valid values [Chrome,Firefox,Opera,Default is Chrome]')
        self.parser.add_argument('--driverpath', type=str,default='Syspath',required=False, help='Optional parameter,Driver path for browser, default is system path, if using remote driver mention remote driver path')
        self.parser.add_argument('--binarypath', type=str,default='Syspath', required=False, help='Optional parameter for browser binary path')
        self.parser.add_argument('--remote', type=bool,default=False, required=False,  help='Boolean parameter, optional parameter, use when for use of remote driver ')
        self.parser.add_argument('--awslambda', type=bool,default=False, required=False,  help='Boolean parameter, optional parameter,set it to convert program in AWS lambda. Warning other parameters will be ignore, only chrome driver is supported')


    def init(self):
        """
        initialize browser & driver
        """
        args=self.parser.parse_args()
        print(args)
        self.is_lambda=False
        try:
            os.mkdir('./screenshot')
        except:
            pass
        browser = args.browser
        if args.awslambda:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1280x1696')
            chrome_options.add_argument('--user-data-dir=/tmp/user-data')
            chrome_options.add_argument('--hide-scrollbars')
            chrome_options.add_argument('--enable-logging')
            chrome_options.add_argument('--log-level=0')
            chrome_options.add_argument('--v=99')
            chrome_options.add_argument('--single-process')
            chrome_options.add_argument('--data-path=/tmp/data-path')
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument('--homedir=/tmp')
            chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
            chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
            chrome_options.binary_location = "/tmp/headless-chromium"
            driver_path= '/tmp/chromedriver'	
            self.driver = webdriver.Chrome(executable_path=driver_path,chrome_options=chrome_options)
            try:
                os.mkdir('/tmp/screenshot')
            except:
                pass
            self.is_lambda=True

        elif browser.lower() == 'chrome':
            chrome_options = Options()
            if args.binarypath != 'Syspath':
                chrome_options.binary_location = args.binarypath

            if args.driverpath != 'Syspath' and args.remote == False:
                driver_path=args.driverpath
                print(driver_path)
                self.driver = webdriver.Chrome(executable_path=driver_path,chrome_options=chrome_options)
            elif args.remote:
                driver_path=args.driverpath
                capabilities = {
                'platform': 'ANY',
                'browserName': 'chrome',
                'version': '',
                'window-size':'Maximized'
                }
                self.driver =webdriver.Remote(driver_path,desired_capabilities=capabilities)    
            else:
                self.driver=webdriver.Chrome(chrome_options=chrome_options)
                
        elif browser.lower() == 'firefox':
            options = Options()
            if args.binarypath != 'Syspath':
                options.binary_location = args.binarypath

            if args.driverpath != 'Syspath' and args.remote == False:
                driver_path=args.driverpath
                self.driver = webdriver.Firefox(executable_path=driver_path,options=options)
            elif args.remote:
                driver_path=args.driverpath
                capabilities = {
                'platform': 'ANY',
                'browserName': 'Firefox',
                'version': '',
                'window-size':'Maximized'
                }
                self.driver =webdriver.Remote(driver_path,desired_capabilities=webdriver.DesiredCapabilities.FIREFOX)    
            else:
                self.driver=webdriver.Firefox(options=options)
                
        elif browser.lower() == 'opera':
            chrome_options = Options()
            if args.binarypath != 'Syspath':
                chrome_options.binary_location = args.binarypath

            if args.driverpath != 'Syspath' and args.remote == False:
                driver_path=args.driverpath
                self.driver = webdriver.Chrome(executable_path=driver_path,chrome_options=chrome_options)
            elif args.remote:
                driver_path=args.driverpath
                capabilities = {
                'platform': 'ANY',
                'browserName': 'Opera',
                'version': '',
                'window-size':'Maximized'
                }
                self.driver =webdriver.Remote(driver_path,desired_capabilities=webdriver.DesiredCapabilities.OPERA)
            else:
                self.driver=webdriver.Chrome(chrome_options=chrome_options) 
        


    def take_screenshot(self,name,path='./screenshot'):
        """
        function to take SS

        """
        if self.is_lambda  :
            filename ='/tmp/screenshot' +"/"+name
        else:
            filename=path+'/'+name
        self.driver.save_screenshot(filename)
