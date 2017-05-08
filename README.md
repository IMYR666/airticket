# 抓取携程机票信息

## 1. 立项背景：
 去年过年回家时，订机票发现票价在每个网站上都有些出入，每次来回切换几个APP的操作挺繁琐的，然后又受启发于电影票比价，
 所以想着如果可以做一个机票比价的程序，自动筛选出最低价格的机票，就不用麻烦的来回切换APP了。
 在此之前，在公司也刚完成几个需要爬虫配合的任务，算是初识爬虫吧，然后就决定自己动手写一个机票比价的程序。
 由于携程不需要登录就可以查看到所有机票的信息，所以此爬虫没有涉及到模拟登陆的部分。主要技术点是构造请求头，AJAX数据的抓取，
 多线程抓取，数据存储等。  
## 2.构造请求头  
 * 设置用户代理  
 urllib2默认使用的是Pyhon-urllib/2.7作为用户代理下载网页内容，但是因为曾经历过质量不佳的Python网络爬虫造成的服务器过载，一些网站会禁封这个默认
 的用户代理，因此，为了更可靠的下载，需要控制用户代理的设定。一般常用的代理如下：  
 
 ```python
 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36'
 ```
 设置完后，使用`request.get()`请求，发现返回的还是`403`错误，这就说明还有携程还对爬虫做了某些限制。后经过查阅发现，请求头中还缺少`referer`关键字。
 * referer  
 Referer是header的一部分，当浏览器向web服务器发送请求的时候，一般会带上Referer，告诉服务器我是从哪个页面链接过来的，服务器基此可以获得一些信息用于处理。
 简而言之，HTTP Referer是header的一部分，当浏览器向web服务器发送请求的时候，一般会带上Referer，告诉服务器我是从哪个页面链接过来的，
 服务器藉此可以获得一些信息用于处理。比如从我主页上链接到一个朋友那里，他的服务器就能够从HTTP Referer中统计出每天有多少用户点击我主页
 上的链接访问他的网站。但注意这个关键字不是必须的，只有部分网站会检查这个，完整可用的请求头如下：
 ```python
 d_headr = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',
    'Referer': s_root_url # 请求rul
    }
 ```
## 3. AJAX数据的抓取  
  构造好以上的请求头后，使用`request.get()`请求返回的状态码`200`，说明伪装成功可以抓取数据了，但是接下来发现，抓下来的html网页中，没有一趟航班信息！
  也就是说，抓下来的html页面，和用浏览器打开的html页面时不一样的。后来几经查阅，发现是因为网站使用了AJAX技术，是一种异步加载方式，可以在不刷新整个页面
  的情况下，获取最新数据。了解这一点之后，使用chrome的开发者工具，找到加载机票信息的那个请求，然后直接构造请求url,用`request.get()`方法就可以直接获取到
  标准的json格式的数据，省去了解析网页的过程。主要代码如下：  
  
  ```python
  req = requests.get(s_real_url, headers=get_header(s_root_url))
  ```  
  
## 4. 多线程抓取  
  由于后面升级需求，找出所有热门城市之间的机票信息，而且要实时，所以对数据的更新频率要高而且数据量也打，所以需要多线程抓取。
  ```python
    for i in range(NUM_THREAD):
      thread_no = i + 1
      stop = start + num_per_thread
      thread = create_thread(get_flight_info, (thread_no, l_city_name[start:stop], s_start_date))
      threads.append(thread)
      start = stop

    for t in threads:
        t.setDaemon(True)
        t.start()

    for t in threads:
        t.join()
  ```
## 5. 数据存储  
  目前数据时存储在mysql中，python需要安装`MySQLdb`这个第三方库。然后我把有关数据库操作的方法封装成一个DBUtils类，这样就可以通用了。



