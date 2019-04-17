import sys
import cv2

if __name__ == '__main__':
    # 设置多线程
    cv2.setUseOptimized(True);
    cv2.setNumThreads(4);

    # read image
    im = cv2.imread(sys.argv[1])
    # resize image
    newHeight = 200
    newWidth = int(im.shape[1]*200/im.shape[0])
    im = cv2.resize(im, (newWidth, newHeight))    

    # 调用opencv
    ss = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()

    
    ss.setBaseImage(im)

    # 速度更快，但是数量少
    if (sys.argv[2] == 'f'):
        ss.switchToSelectiveSearchFast()

    #数量多，但速度慢
    elif (sys.argv[2] == 'q'):
        ss.switchToSelectiveSearchQuality()

   
    rects = ss.process()
    print('Total Number of Region Proposals: {}'.format(len(rects)))
    
    numShowRects = 100
    increment = 50

    while True:
        imOut = im.copy()    
        for i, rect in enumerate(rects):
            if (i < numShowRects):
                x, y, w, h = rect
                cv2.rectangle(imOut, (x, y), (x+w, y+h), (0, 255, 0), 1, cv2.LINE_AA)
            else:
                break
  
        cv2.imshow("Output", imOut)
        k = cv2.waitKey(0) & 0xFF

        if k == 109: 
            numShowRects += increment
        elif k == 108 and numShowRects > increment:
            numShowRects -= increment
        elif k == 113:
            break

    cv2.destroyAllWindows()
