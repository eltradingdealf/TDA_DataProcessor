import numpy as np

theShape = (1,70)
a = np.zeros(theShape)

b = np.zeros(theShape)

c = np.concatenate((a, b), axis=0)

c[0,1] = 98
c[0, 1] = 5
c[1,2] = 34

print(c)

x = np.zeros((1,1), dtype=int)
print(x)

x = a

x[0,0] = 3
x[0,1]=4
print(x)

x = np.concatenate((x, c), axis=0)
print('----')
print(x)

ss = 0
for a in x:
    ss += len(a)
#
print(ss)

ss = 0
ticks_array = [[2,3,4], [5,6,7]]
for a in ticks_array:
    ss += len(a)
#
print(ss)

volume_ndArray_tmp = np.zeros((3, 1), dtype=int)
ss = 0
for a in volume_ndArray_tmp:
    ss += len(a)
#
print (volume_ndArray_tmp)
print(ss)

print('----')
d = np.zeros((3,1), dtype=int)
#volume_ndArray_tmp = np.concatenate(volume_ndArray_tmp, d, axis=1)
volume_ndArray_tmp = np.hstack((volume_ndArray_tmp, d))
print (volume_ndArray_tmp)

volume_ndArray_tmp[1,1] = 33
volume_ndArray_tmp[1,0] = 33
volume_ndArray_tmp[0,1] = 33
volume_ndArray_tmp[0,0] = 33
print (volume_ndArray_tmp)

print('---')
zp = np.array([4,6,3,4,5,0,0,0])
i = np.mean(zp[:5])
print('i='+str(i))


arrg = np.zeros((1, 20), dtype=int)
arrg[0,0] = 7
arrg[0,1] = 5
arrg[0,2] = 6
arrg[0,3] = 5
arrg[0,4] = 6
iig = np.mean(arrg[0, :2])
print('iig='+str(iig))

