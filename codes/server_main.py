import socket
import task_1a
import cv2
import numpy as np
import os
import _thread

ServerSocket = socket.socket()
host = '10.42.0.1'
port =  2301
ThreadCount = 0

a=[]
a = [[0 for c in range(10)] for r in range(10)]
curr_dir_path = os.getcwd()
img_dir_path = curr_dir_path + '/../task_1a_images/'				
global updated_image
img_file_path = img_dir_path + 'Floor1.jpg'		
original_binary_img = task_1a.readImage(img_file_path)
updated_image=original_binary_img
height, width = original_binary_img.shape


no_cells_height = int(height/40)							
no_cells_width = int(width/40)							
final_point = ((no_cells_height-1),(no_cells_width-1))

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(5)
def threaded_client(connection):
    #print('ThreadCount')
   
    global updated_image
    msg = connection.recv(2048)
    str=msg.decode('utf-8')
    print(str)
    
    str=str+""
    ab=(int(str[1]),int(str[3]))
    initial_point=ab
    a[int(str[1])][int(str[3])]+=1

        

    try:

        shortestPath = task_1a.solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width)
        if len(shortestPath) > 2:
            img = task_1a.image_enhancer.highlightPath(updated_image, initial_point, final_point, shortestPath)
            c1=int(str[1])
            c2=int(str[3])
            for i in range (0,10):
                for j in range (0,10):
                    flag=0
                    val=a[i][j]
                    if val==1:
                        img_1 = task_1a.readImage(curr_dir_path + '/../task_1a_images/One.jpg')
                    elif val==2:
                        img_1 = task_1a.readImage(curr_dir_path + '/../task_1a_images/Two.jpg')
                    elif val==3:
                        img_1 = task_1a.readImage(curr_dir_path + '/../task_1a_images/Three.jpg')
                    else:
                        flag=1
                    
                    if flag==0:
                        co1=i*40
                        co1=co1+6
                        co2=co1+28
                        
                        to1=j*40
                        to1=to1+6
                        to2=to1+28
                        
                        img[co1:co2,to1:to2]=255
                        img[co1:co2,to1:to2]=img_1
                    
                        
                        
                    
            updated_image=img
            
        
        else:

            #print('\n[ERROR] shortestPath returned by solveMaze function is not complete !\n')
            exit()
        
        

    except TypeError as type_err:
    
        
        #print('\n[ERROR] solveMaze function is not returning shortest path in maze image in expected format !\n')
        exit()

    cv2.imshow('don', img)
    cv2.imwrite('Exxitplan.jpg', img)
    cv2.waitKey(7000)
    cv2.destroyAllWindows()



       
while True:

    Client, address = ServerSocket.accept()
    
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    
    threaded_client(Client)
    
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSocket.close()

