#python

def subscriber_speed_callback(msg):
    print (msg.keys()) # for debug (to get the keys of the python dict associated to the topic)
    sim.addLog(sim.verbosity_scriptinfos,'subscriber received speed = '+str(msg['data']))
    speed = msg['data']
    # and apply speed to front wheel motor joint in CoppeliaSim (/FrontMotor)
    sim.setJointTargetVelocity(sim.getObject("/FrontMotor"),speed)

def subscriber_steering_callback(msg):
    print (msg.keys()) # for debug (to get the keys of the python dict associated to the topic)
    sim.addLog(sim.verbosity_scriptinfos,'subscriber received steering = '+str(msg['data']))
    steering = msg['data']
    # and apply steering to handlebar joint in CoppeliaSim (/Steering)
    sim.setJointTargetPosition(sim.getObject("/Steering"),steering)    

def sysCall_init():
    sim = require('sim')
    simROS2 = require('simROS2')
    # Prepare the float32 publisher and subscribers 
    self.publisher_front_sonar=simROS2.createPublisher('/front_sonar','std_msgs/msg/Float32')
    self.subscriber_steering=simROS2.createSubscription('/steering','std_msgs/msg/Float32','subscriber_steering_callback')
    self.subscriber_speed=simROS2.createSubscription('/speed','std_msgs/msg/Float32','subscriber_speed_callback')

def sysCall_actuation():
     # Send an updated distance for the front obstacle
    front_sonar = sim.getObject("/FrontSonar")  
    result, distance, detected_point, detected_object_handle, detected_object_normal = sim.handleProximitySensor (front_sonar)
    simROS2.publish(self.publisher_front_sonar, {'data': distance})
    # simROS2.sendTransform(getTransformStamped(self.objectHandle, self.objectAlias, -1, 'world'))
    # # To send several transforms at once, use simROS2.sendTransforms instead

def sysCall_cleanup():
    # Following not really needed in a simulation script (i.e. automatically shut down at simulation end):
    simROS2.shutdownPublisher(self.publisher_front_sonar)
    simROS2.shutdownSubscription(self.subscriber_steering)   
    simROS2.shutdownSubscription(self.subscriber_speed)   

