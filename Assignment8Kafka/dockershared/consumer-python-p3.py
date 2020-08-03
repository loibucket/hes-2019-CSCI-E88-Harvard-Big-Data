# Using Kafka APIs, create a Problem3Consumer (single-threaded is OK), with the "p3consumer" consumer group.id,  that listens to the "problem3" topic - demonstrate that it receives events generated by the Problem3Producer
# For each event received, the Problem3Consumer should print out its offset, partition number, event key and event body

from kafka import KafkaConsumer

var = 1
while var == 1 :
    consumer = KafkaConsumer(bootstrap_servers='kafka:9092',group_id='p3consumer',auto_offset_reset='latest')
    #consumer = KafkaConsumer(bootstrap_servers='localhost:32787',client_id="2",group_id='consumer-1',auto_offset_reset='latest')
    consumer.subscribe(['problem3'])

    for message in consumer:
        #print (type(message)) #debug
        #print (message) #debug
        print ('offset:', end=' ')
        print (message.offset, end=' ')
        print ('partition:', end=' ')
        print (message.partition, end=' ')
        print ('event key:', end=' ')
        print (message.key.decode("utf-8"), end=' ')
        print ('event body:', end=' ')
        print (message.value.decode("utf-8"))