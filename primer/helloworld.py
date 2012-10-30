import cloud

def square(x):
	return x*x

jid = cloud.call(square, 9)
print 'Squaring 9 (9*) has been pushed to the cloud with job id %s' % jid

res = cloud.result(jid)
print 'Result is %s' % res
