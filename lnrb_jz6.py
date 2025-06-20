# coding = utf-8  
from selenium import webdriver # pip install selenium
import time,os

#driver = webdriver.Firefox() # copy geckodriver.exe to python dir
#driver = webdriver.Ie()
driver = webdriver.Chrome() # copy driver.exe to python dir

#driver.maximize_window() # 浏览器最大化
#driver.minimize_window() # 浏览器最小化
#driver.implicitly_wait(6) # 隐性等待

y='2023'
m='03'
f = open('png/list' + m +'.txt','w')
for i in range(31,32): # 1-31（1-32）日
    for k in range(1,33): # 1-32（1-33）版
        d=str(i).zfill(2) # 日期格式化
        n=str(k).zfill(2) # 版面格式化
        nn=str(k+1).zfill(2) # 下一版面格式化
        print(d+ '日第' + n + '版')
        lnrb_url='http://epaper.lnd.com.cn/lnrbepaper/pc/layout/'+ y + m + '/' + d + '/node_' + n + '.html' # 当前版面地址
        lnrb_url_next='http://epaper.lnd.com.cn/lnrbepaper/pc/layout/'+ y + m + '/' + d + '/node_' + nn + '.html' # 下一版面地址
        driver.get(lnrb_url) # 打开页面
        time.sleep(1) # 强制等待
        try:
            #if driver.find_element_by_xpath('/html/body/center[1]/h1').text == '404 Not Found'or driver.find_element_by_xpath('/html/body/div/div[2]/h1').text == '您访问的页面暂时无法显示':# 发现页面不存在
            #if driver.find_element_by_xpath('/html/body/div/div[2]/h1').text == '您访问的页面暂时无法显示':# 发现页面不存在
            if driver.find_element_by_xpath('/html/body/center[1]/h1').text == '404 Not Found':# 发现页面不存在
                print ('今日报纸有可能结束，也可能是对开版')
                driver.get(lnrb_url_next) # 再打开下一版面看看
                if driver.find_element_by_xpath('/html/body/center[1]/h1').text == '404 Not Found':# 发现页面不存在，当天报纸真的结束了
                    print ('今日报纸结束，共' + str(k-1) + '版')
                    break # 跳出当天版面循环
        except:
            print('正常')
            #print(driver.find_element_by_xpath(".//*[@id='ScroLeft']/div[1]/em").text[5:9])
            
        #if driver.find_element_by_xpath(".//*[@id='ScroLeft']/div[1]/em").text[-2:] == '锦州': # 查找报头是否为锦州专版
        #print(driver.find_element_by_xpath(".//*[@id='ScroLeft']/div[1]/em").text[5:7])
        if driver.find_element_by_xpath(".//*[@id='ScroLeft']/div[1]/em").text[5:9] == '地方新闻': # 查找报头是否为锦州专版
            print('地方新闻专版')
            print(driver.find_element_by_xpath(".//*[@id='ScroLeft']/div[1]/em").text[10:12])
            png_name='png\\《辽宁日报》' + y + '年' + m + '月' + d + '日第' + n + '版' + '.png'
            driver.get_screenshot_as_file(png_name) # 当前窗口截图
        for j in driver.find_elements_by_partial_link_text('锦州') \
            or driver.find_elements_by_partial_link_text('锦绣') \
            or driver.find_elements_by_partial_link_text('辽沈') \
            or driver.find_elements_by_partial_link_text('陆海') \
            or driver.find_elements_by_partial_link_text('黑山') \
            or driver.find_elements_by_partial_link_text('北镇') \
            or driver.find_elements_by_partial_link_text('凌海') \
            or driver.find_elements_by_partial_link_text('义县'): # 查找所有包含锦州的元素
            bt=j.text # 取得元素全部内容
            print(bt)
            js="window.open('" + j.get_attribute('href') + "');" # 取得元素链接
            driver.execute_script(js) # 通过js方式在新标签页中打开
            handles = driver.window_handles # 取得标签页句柄集合
            driver.switch_to.window(handles[1]) #切换到第二个窗口        
            time.sleep(1) # 强制等待
            png_name='png\\《辽宁日报》' + y + '年' + m + '月' + d + '日第' + n + '版' + bt + '.png'
            driver.get_screenshot_as_file(png_name) # 第二个窗口截图
            #f.write( m + '月' + d + '日，《' + bt + '》\n') # 写入列表文件
            time.sleep(1) # 强制等待        
            driver.close() # 关闭第二个窗口
            driver.switch_to.window(handles[0]) #切换回第一个窗口
f.close()
driver.quit()

