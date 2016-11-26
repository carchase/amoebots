def handleInput(cmd, vel):
	if cmd == 1:
		print 'Moving forward'
		moveWheels(vel, vel, True)
		return
	if cmd == 2:
		print 'Moving backward'
		moveWheels(-vel, -vel, True)
		return
	if cmd == 3:
		print 'Turning left'
		moveWheels(0, vel, True)
		return
	if cmd == 4:
		print 'Turning right'
		moveWheels(vel, 0, True)
		return
	if cmd == 5:
		print 'Stopping'
		moveWheels(0, 0, False)
		return
	if cmd == 6:
		print 'Stopping arm'
		moveArm(0, False)
		return
	if cmd == 7:
		print 'Moving arm' # up?
		moveArm(vel, True)
		return
	if cmd == 8:
		print 'Moving arm' # down?
		moveArm(-vel, True)
		return
	if cmd == 11:
		print 'Moving forward'
		moveWheels(vel, vel, False)
		return
	if cmd == 12:
		print 'Moving backward'
		moveWheels(-vel, -vel, False)
		return
	if cmd == 13:
		print 'Turning left'
		moveWheels(0, vel, False)
		return
	if cmd == 14:
		print 'Turning right'
		moveWheels(vel, 0, False)
		return
	if cmd == 15:
		print 'Moving arm' # up?
		moveArm(vel, False)
		return
	if cmd == 16:
		print 'Moving arm' # down?
		moveArm(-vel, False)
		return
	print 'Unsupported command ' + str(cmd)

def moveWheels(left, right, delay):
	left_motor.setVelocity(left)
	right_motor.setVelocity(right)
	if delay:
		time.sleep(1)
		moveWheels(0, 0, False)

def moveArm(velocity, delay):
	top_motor.setVelocty(velocity)
	if delay:
		time.sleep(1)
		moveArm(0, False)
