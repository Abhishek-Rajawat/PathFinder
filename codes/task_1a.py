import cv2
import numpy as np
import os
import image_enhancer

CELL_SIZE = 40
initial_point=(0,0)




def readImage(img_file_path):

	binary_img = None
	img=cv2.imread(img_file_path,2)
	ret,binary_img=cv2.threshold(img,127,255,cv2.THRESH_BINARY)

	return binary_img


def solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width):

	rre=CELL_SIZE
	
	shortestPath = []
	end=(int(final_point[0]))*no_cells_height+int(no_cells_width-1)
	img=original_binary_img
	h,w=original_binary_img.shape
	no_ro=no_cells_height
	no_ro=int(no_ro)
	no_co=no_cells_width;
	no_co=int(no_co)
	pr=0
	pc=0
	k=0
	num=""
	s=""
	fs=""
	ans=""
	imgc=[[-1]*4 for i in range(no_co*no_ro)]
	while pr<no_ro:
		while pc<no_co:
			irb=(pr*rre)+1
			ire=(pr+1)*rre
			icb=(pc*rre)+1
			ice=(pc+1)*rre
			t=int((irb+ire)/2)
			l=int((ice+icb)/2)
			if t>(h-1):
				t=h-1
			if l>(w-1):
				l=w-1
			if irb>(h-1):
				irb=h-1
			if ire>(h-1):
				ire=h-1
			if icb>(w-1):
				icb=w-1
			if ice>(w-1):
				ice=w-1
			li=-1
			ri=-1
			ti=-1
			bi=-1
			o=0
			if(CELL_SIZE==20):
				it=icb-10;
				if(it<0):
					it=-1;
				pt=ice+10;
				if(pt>=w):
					pt=-1;
				yt=irb-10;
				if(yt<0):
					yt=-1;
				rt=ire+10;
				if(it>h):
					it=-1;
				if (img[t,icb].all()!=0):
					if(it!=-1):
						if(img[t,it].all()!=0):
							li=(pr)*no_ro+pc-1
					else:
						li=(pr)*no_ro+pc-1
				if img[t,ice].all()!=0:
					if(pt!=-1):
						if(img[t,pt].all()!=0):
							ri=(pr)*no_ro+pc+1
					else:
						ri=(pr)*no_ro+pc+1
				if img[irb,l].all()!=0:
					if(yt!=-1):
						if(img[yt,l].all()!=0):
							ti=(pr)*no_ro+pc
							ti=ti-no_ro
					else:
						ti=(pr)*no_ro+pc
						ti=ti-no_ro
				if img[ire,l].all()!=0:
					if(rt!=-1):
						if(img[rt,l].all()!=0):
							bi=(pr)*no_ro+pc
							bi=bi+no_ro
					else:
						bi=(pr)*no_ro+pc
						bi=bi+no_ro

				if(li>=0):
					imgc[k][o]=li
					o=o+1
				if(ri>=0):
					imgc[k][o]=ri
					o=o+1
				if(ti>=0):
					imgc[k][o]=ti
					o=o+1
				if(bi>=0):
					imgc[k][o]=bi
					o=o+12
			else:
				if img[t,icb].all()!=0:
					li=(pr)*no_ro+pc-1
				if img[t,ice].all()!=0:
					ri=(pr)*no_ro+pc+1
				if img[irb,l].all()!=0:
					ti=(pr)*no_ro+pc
					ti=ti-no_ro
				if img[ire,l].all()!=0:
					bi=(pr)*no_ro+pc
					bi=bi+no_ro
				if(li>=0):
					imgc[k][o]=li
					o=o+1
				if(ri>=0):
					imgc[k][o]=ri
					o=o+1
				if(ti>=0):
					imgc[k][o]=ti
					o=o+1
				if(bi>=0):
					imgc[k][o]=bi
					o=o+12
			k=k+1
			pc=pc+1
		pc=0
		pr=pr+1
	flag=0
	k=0
	k1=0
	fla=0
	ar=[]
	tem=[]
	#for j in range(0,(no_cells_width*no_cells_height)):
		#for h in range(0,4):
			#print(imgc[j][h]+" ",end=' ')
		#print()
	li=(initial_point[0])*no_ro+initial_point[1]
	ar.append("_"+str(li))
	tem.append(str(li))
	k1=k1+1
	k=k+1
	while flag!=1:
		ui=0
		for j in range (0,k):
			ine=ar[j].rindex("_")
			l=len(ar[j])
			num=""
			for h in range (ine+1,l):
				num=num+ar[j][h]
			nu=int(num)
			cou=0
			for h in range (0,4):
				if imgc[nu][h]!=-1:
					fla=0
					s=str(imgc[nu][h])
					for u in range (0,k1):
						if tem[u]==s:
							fla=1
					if fla==0:
						cou=cou+1
			if cou==1:
				for h in range (0,4):
					if imgc[nu][h]!=-1:
						fla=0
						s=str(imgc[nu][h])
						for u in range (0,k1):
							if tem[u]==s:
								fla=1
						if fla==0:
							ar[j]=ar[j]+"_"+s
							tem.append(s);
							k1=k1+1
			elif cou>1:
				con=0
				for h in range(0,4):
					if imgc[nu][h]!=-1:
						fla=0
						s=str(imgc[nu][h])
						for u in range (0,k1):
							if tem[u]==s:
								fla=1
						if fla==0:
							if con==0:
								fs=s
								tem.append(s)
								k1=k1+1
							else:
								ar.append(str(ar[j])+"_"+s)
								tem.append(s)
								k1=k1+1
								ui=ui+1
							con=con+1
				ar[j]=ar[j]+"_"+fs
		if ui>0:
			k=k+ui
		for j in range (0,k):
			ine=ar[j].rindex("_")
			l=len(ar[j])
			s=""
			for h in range (ine+1,l):
				s=s+ar[j][h]
			if(s==str(end)):
				flag=1
				ans=ar[j]
				break
	ans=ans+"_"
	s=""
	l=len(ans)
	for j in range(1,l):
		ch=ans[j]
		if ch!='_':
			s=s+ch
		else:
			nu=int(s)
			s=""
			x1=int(nu/no_cells_height)
			y1=int(nu%no_cells_height)
			ex=(x1,y1)
			shortestPath.append(ex)












	
	
	return shortestPath


if __name__=='__main__':

	curr_dir_path = os.getcwd()
	img_dir_path = curr_dir_path + '/../task_1a_images/'				# path to directory of 'task_1a_images'
	
	file_num = 0
	img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'		# path to 'maze00.jpg' image file

	##print('\n============================================')

	#print('\nFor maze0' + str(file_num) + '.jpg')

	try:
		
		original_binary_img = readImage(img_file_path)
		height, width = original_binary_img.shape

	except AttributeError as attr_error:
		
		#print('\n[ERROR] readImage function is not returning binary form of original image in expected format !\n')
		exit()
	
	no_cells_height = int(height/CELL_SIZE)							# number of cells in height of maze image
	no_cells_width = int(width/CELL_SIZE)							# number of cells in width of maze image
	#initial_point = (0, 7)										# start point coordinates of maze
	final_point = ((no_cells_height-1),(no_cells_width-1))			# end point coordinates of maze

	try:

		shortestPath = solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width)
		if len(shortestPath) > 2:

			img = image_enhancer.highlightPath(original_binary_img, initial_point, final_point, shortestPath)
			
		else:

			#print('\n[ERROR] shortestPath returned by solveMaze function is not complete !\n')
			exit()
	
	except TypeError as type_err:
		
		#print('\n[ERROR] solveMaze function is not returning shortest path in maze image in expected format !\n')
		exit()

	#print('\nShortest Path = %s \n\nLength of Path = %d' % (shortestPath, len(shortestPath)))
	
	#print('\n============================================')
	
	cv2.imshow('canvas0' + str(file_num), img)
	#cv2.imwrite('canvas0' + str(file_num)+'.jpg', img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	exit()

	"""choice = input('\nWant to run your script on all maze images ? ==>> "y" or "n": ')

	if choice == 'y':

		file_count = len(os.listdir(img_dir_path))

		for file_num in range(file_count):

			img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'

			print('\n============================================')

			print('\nFor maze0' + str(file_num) + '.jpg')

			try:
				
				original_binary_img = readImage(img_file_path)
				height, width = original_binary_img.shape

			except AttributeError as attr_error:
				
				print('\n[ERROR] readImage function is not returning binary form of original image in expected format !\n')
				exit()
			
			no_cells_height = int(height/CELL_SIZE)							# number of cells in height of maze image
			no_cells_width = int(width/CELL_SIZE)							# number of cells in width of maze image
			initial_point = (0, 0)											# start point coordinates of maze
			final_point = ((no_cells_height-1),(no_cells_width-1))			# end point coordinates of maze

			try:

				shortestPath = solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width)

				if len(shortestPath) > 2:

					img = image_enhancer.highlightPath(original_binary_img, initial_point, final_point, shortestPath)
					
				else:

					print('\n[ERROR] shortestPath returned by solveMaze function is not complete !\n')
					exit()
			
			except TypeError as type_err:
				
				print('\n[ERROR] solveMaze function is not returning shortest path in maze image in expected format !\n')
				exit()

			print('\nShortest Path = %s \n\nLength of Path = %d' % (shortestPath, len(shortestPath)))
			
			print('\n============================================')

			cv2.imshow('canvas0' + str(file_num), img)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
	
	else:

		print('')"""


