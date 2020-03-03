import pymqi
import uuid
from random import randint
import time

# Install Steps
# - Install IBM Toolkit https://developer.ibm.com/messaging/2019/02/05/ibm-mq-macos-toolkit-for-developers/
# - Set environment variables and path as instructed in above link before continuing to the next step
# - pip install pymqi

# pymqi API Reference
# https://dsuch.github.io/pymqi/examples.html

# Set connection configuration
host = 'mqgospel-f0f7.qm.eu-gb.mq.appdomain.cloud'
port = '30215'
user = 'gmqcrobin'
password = 'D8tepw7qi7rrvySw24cRtkxwijLfY-fvthzbeucsB31S'

# Set MQ configuration
queue_manager = 'MQGospel'
channel = 'CLOUD.APP.SVRCONN'
queue_name = 'DEV.QUEUE.1'
# Specify that we're sending a string even though it's binary encoded
md = pymqi.MD()
md.Format = pymqi.CMQC.MQFMT_STRING

# Connect to MQ
conn_info = '%s(%s)' % (host, port)
qmgr = pymqi.connect(queue_manager, channel, conn_info, user, password)
queue = pymqi.Queue(qmgr, queue_name)

# Send a batch of messages
for x in range(1000):
	id = "A" + str(uuid.uuid4()).upper()
	amount = str(randint (1, 100))
	orderid = str(randint (1, 10000))
	message = '{"payments": [{"id": "' + id + '", "accountfrom": "robin", "accountto": "trent", "amount": "' + amount + '", "description": "order' + orderid + '"}]}'
	# In python3 you must encode the message
	encodedMessage = bytes(message, 'utf-8')
	# Send the message!
	queue.put(encodedMessage, md, None)
	print("Sent message " + str(x) + " to MQ: " + message)
	time.sleep(0.2)

# Tidy up
queue.close()
qmgr.disconnect()