"""
Tests the FloatList type.
"""

from floatlist import FloatList

if __name__ == "__main__":
	fl = FloatList([0, 1, 2, 3], True)
	print(fl.lerp)
	print("contents of fl: "+str(fl))
	print("fl[.75:2:1.0]: "+str(fl[.75:2:1.0]))
	print(0 in fl)
	for i in range(60):
		k = i/10
		print(str(k)+": "+str(k%len(fl))+": "+str(fl[k]))
