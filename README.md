# mini_ximi

##概述
	整体架构写在http://hiroguo.me/?p=264文章中。
	
	本项目的代码提取出实际代码中的跟业务逻辑关系不大的公共的部分，做了少量重构。
	
##运行环境
	
	运行环境python 2.7.x
	
	项目的依赖库放置在pypi_requirements.txt文件中
	
	rabbitmq-server  本项目使用的guest用户  生产环境请自行更换用户
	
##代码结构


##服务端的tcp长连接层
	
	对客户端的tcp连接进行维护和管理，向客户端发送心跳包，对没有按时回复心跳包的连接断开连接。
	
	对客户端发送过来的tcp数据包进行解包，根据数据包的消息指令，携带路由key（表示这一指令由哪个后端业务逻辑服务处理），然后发送给rabbitmq。
	
	接收来自后端业务逻辑服务发送给rabbitmq的消息，tcp长连接层会部署多个进程，rabbitmq会根据绑定的路由的key将消息转发给指定的长连接管的进程。
	
	这一层目前使用python的twisted框架构建的。
	
	运行：   python bin/main_tcp_server.py main_tcp_server_1
	
	
##rabbitmq的consumer woker  处理业务逻辑部分

	从rabbitmq接收数据，然后根据业务逻辑处理完毕之后，把需要给客户端发送的消息，发回到rabbitmq当中。
	
	运行： python bin/worker_consumer.py
	

##客户端
	这里写了一个简易的客户端,它会连接到tcp长连接层，连接上去之后，进行登陆操作，然后每隔10秒钟发送一个心跳包到服务生起
	
	运行： python  test/client.py
	