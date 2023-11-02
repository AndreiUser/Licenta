import cv2 as cv
import argparse
import numpy as np

ap = argparse.ArgumentParser()

#python line.py --Ax 361 --Ay 135 --Bx 1355 --By 123 --Cx 389 --Cy 1093 --Dx 1333 --Dy 1093 --image images/drept.jpg
#python line.py --Ax 269 --Ay 125 --Bx 1211 --By 113 --Cx 269 --Cy 1072 --Dx 1233 --Dy 1071 --image images/LuminaNaturala.jpg
ap.add_argument("-a", "--Ax", required=False, help="")
ap.add_argument("-b", "--Ay", required=False, help="")
ap.add_argument("-c", "--Bx", required=False, help="")
ap.add_argument("-d", "--By", required=False, help="")
ap.add_argument("-e", "--Cx", required=False, help="")
ap.add_argument("-f", "--Cy", required=False, help="")
ap.add_argument("-m", "--Dx", required=False, help="")
ap.add_argument("-n", "--Dy", required=False, help="")

ap.add_argument("-g", "--image", required=False, help="path to input image")
args = vars(ap.parse_args())

def MakePointList(A,B):
    pasX=(B[0]-A[0])/8
    pasY=(B[1]-A[1])/8
    AB=[]
    for i in range(9):
        AB.append((A[0]+int(i*pasX),A[1]+int(i*pasY)))
    return AB

def GetPas(A,B):
    pasX=(B[0]-A[0])/8
    pasY=(B[1]-A[1])/8
    return (pasX,pasY)


def DrawKernel(A,B,C,D,img):     
    color=(200,200,200)
    font=cv.FONT_HERSHEY_SIMPLEX
    size=3
    resize=(1080,720)
    AB=MakePointList(A,B)
    CD=MakePointList(C,D)
    AC=MakePointList(A,C)
    BD=MakePointList(B,D)





    #img=GetSquareCordinates(AB,AC)

    squares=GetSquareCordinates(AB,AC)
    
    averageVector=[]
    for sq in squares:
        averageVector.append(average(sq))

    img2=colorTheSquares(squares)
    
    img2=cv.resize(img2,resize)
    cv.imshow("Chenar",img2)
    cv.waitKey(0)
    
    ALBGOL=[]
    ALBGOLVALUE=[]

    NEGRUGOL=[]
    NEGRUGOLVALUE=[]
    
    
    for av in averageVector:
        H3=averageVector[3]
        if(specialDiff(av,H3,255)):
            print(averageVector.index(av))
            ALBGOL.append(averageVector.index(av))
            ALBGOLVALUE.append(av)
        ALBGOLVALUE.append(0)

    for av in averageVector:
        E5=averageVector[4]
        if(specialDiffBlack(av,E5,50)):
            print(averageVector.index(av))
            NEGRUGOL.append(averageVector.index(av))
            NEGRUGOLVALUE.append(av)

            
    for i in range(64):
        if(np.isin(i,ALBGOL)):
            print("CAMPUL"+str(i)+"\n")
            print(ALBGOLVALUE[i])
            img = cv.putText(img,"campGol",(squares[i][0][0],squares[i][1][1]+60),cv.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2,cv.LINE_AA)
    
 
    img=cv.resize(img,resize)
    cv.imshow("Albe",img)
    cv.waitKey(0)

    img3=cv.imread(args["image"])

    j=0
    for i in range(64):
        if(np.isin(i,NEGRUGOL)):
            
            print("CAMPUL"+str(i)+"\n")
            red=int(NEGRUGOLVALUE[j][0])
            green=int(NEGRUGOLVALUE[j][1])
            blue=int(NEGRUGOLVALUE[j][2])
            img3 = cv.putText(img3,"negru.gol",(squares[i][0][0],squares[i][1][1]+50),cv.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2,cv.LINE_AA)
            j=j+1
    img3=cv.resize(img3,resize)
    cv.imshow("Negre",img3)
    cv.waitKey(0)





def specialDiff(av1,av2,value):
    print(av1,av2)
    compound=abs(av1[0]-av2[0]) + abs(av1[1]-av2[1]) + abs(av1[2]-av2[2])
    if(compound>value):
        return True
    
def specialDiffBlack(av1,av2,value):
    print(av1,av2)
    if(abs(av1[0]-av2[0])>value or abs(av1[1]-av2[1])>value or abs(av1[2]-av2[2])>value):
        return True

    

def GetSquareCordinates(AB,AC):
    squares=[]
    for i in range(8):
        for j in range(8):
            E=(AB[0+i][0],AC[0+j][1])
            F=(AB[0+1+i][0],AC[0+j][1])
            G=(AB[0+i][0],AC[0+1+j][1])
            H=(AB[0+1+i][0],AC[0+1+j][1])
            sq=(E,F,G,H)
            squares.append(sq)
    return squares

def colorTheSquares(squares):
    img=cv.imread(args["image"])

    for i in range(64):
        if(i%2==1):
            color=(0,0,200)
        else:
            color=(90,80,200)
        E=squares[i][0]
        F=squares[i][1]
        G=squares[i][2]
        H=squares[i][3]
        cv.line(img, E,G, color, 5)
        cv.line(img, F,H  , color, 5)
        cv.line(img, E,F  , color, 5)
        cv.line(img, G,H  , color, 5)
        #img=average(squares[i],img)
    return img

def average(sq):
    img=cv.imread(args["image"])

    m0=sq[0][0]
    n0=sq[0][1]
    m=sq[3][0]
    n=sq[3][1]

    R,G,B =0,0,0
    iterator=0

    for i in range(m0,m):
        for j in range(n0,n):
            iterator=iterator+1
            R=R+img[j][i][0]
            G=G+img[j][i][1]
            B=B+img[j][i][2]
            

   
    #cv.imshow("8 lini trase",img)
    cv.waitKey(0)
    return (R/iterator,G/iterator,B/iterator)

def averageGray(sq):
    img=cv.imread(args["image"])
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    m0=sq[0][0]
    n0=sq[0][1]
    m=sq[3][0]
    n=sq[3][1]

    R =0
    iterator=0
    print(img.shape)
    for i in range(m0,m):
        for j in range(n0,n):
            iterator=iterator+1
            R=R+img[j][i]
            
   
    #cv.imshow("8 lini trase",img)
    cv.waitKey(0)
    return (R/iterator)


    



def GetState(A):
    print("hello")




#cv.putText(img, (str(x)+" "+str(y)),  (x,y) , font, 0.6,color,2,cv.LINE_AA)
#((x+length*W),(y+i*length))

img=cv.imread("images/lumina.1.jpg")
#cv.line(img, (100,100), (200,100), (256,256,0), 1) 






Ax=int(args["Ax"])
Ay=int(args["Ay"])
Bx=int(args["Bx"])
By=int(args["By"])
Cx=int(args["Cx"])
Cy=int(args["Cy"])
Dx=int(args["Dx"])
Dy=int(args["Dy"])
img=cv.imread(args["image"])

#print("Am primit lungime="+str(length)+" x="+str(X)+" y="+str(Y)+" img="+args["image"])
DrawKernel((Ax,Ay),(Bx,By),(Cx,Cy),(Dx,Dy),img)

#python line.py --Xo 540 --Yo 135 --Xf 1490 --Yf 963 --imageimages/lumina.1.jpg

cv.imwrite("Produse/hello.jpg",img)
#cv.imshow("linie",img)
#cv.waitKey(0)




