import cv2
import copy
import numpy as np

class Segmentation(object):
    def start(self, file_name, target):
        # target {0:사과 , 1:체리 , 2:토마토}
        origin_img = cv2.imread(file_name)
        if origin_img is None:
            print('====================== Image not found ======================')
            print('====================== File name : ' + file_name)
            return

        gray_img = cv2.imread(file_name,0)
        bin_img = self.binarize(gray_img, 250)

        sg_img , count = self.segmentation(bin_img)
        result = self.segmentation_image_show(origin_img,sg_img, target)
        cv2.imshow('Test',result)
        cv2.waitKey(0)

    def binarize(self, img, threshold):
        # 이진화
        ret, bin_img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
        return bin_img

    # def segmentation(self, img):
    #     segmentation_img = copy.deepcopy(img)
    #     offset = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    #     count = 0
    #     start_point = []
    #
    #     for i in range(len(img)):
    #         for j in range(len(img[0])):
    #             if segmentation_img[i][j] == 255:
    #                 start_point.append([i, j])
    #                 count += 1
    #                 q = [[i, j]]
    #                 while q:
    #                     cur = q.pop(0)
    #                     x, y = cur[0], cur[1]
    #                     if x < 0 or y < 0:
    #                         pass
    #                     elif x > len(img) - 1 or y > len(img[0]) - 1:
    #                         pass
    #                     elif segmentation_img[x][y] != 255:
    #                         pass
    #                     else:
    #                         segmentation_img[x][y] = count
    #                         for i in range(4):
    #                             q.append([x + offset[i][0], y + offset[i][1]])
    #     return segmentation_img
    #
    # def segmentation_image_show(self, origin_img, segmentation_img, color, xy):
    #     color_img = copy.deepcopy(origin_img)
    #     color_count = segmentation_img[xy[0]][xy[1]]
    #
    #     for i in range(len(segmentation_img)):
    #         for j in range(len(segmentation_img[0])):
    #             if segmentation_img[i][j] != 0 and segmentation_img[i][j] != 255 and segmentation_img[i][j] == color_count:
    #                 color_img[i][j] = color
    #     self.natual_coloring(color_img,50)
    #     return color_img
    #
    # def natual_coloring(self, img, value):
    #     random_num = random.randrange(125,175)
    #     for i in range(random_num-value,random_num+value):
    #         for j in range(random_num-value,random_num+value):
    #             d = self.p2p_dst(i,j,random_num,random_num)
    #             if d <= value and self.img2np(img[i][j],[0,0,0]) and self.img2np(img[i][j],[255,255,255]):
    #                 for k in range(0,3):
    #                     img[i][j][k] = self.check255(img[i][j][k] + value - d)
    #     # img = cv2.GaussianBlur(img, (11, 11), 0)
    #
    # def p2p_dst(self,x1,y1,x2,y2):
    #     return int(math.sqrt((x2-x1)**2 + (y2-y1)**2))
    #
    # def img2np(self,v1,v2):
    #     if v1[0] == v2[0] and v1[1] == v2[1] and v1[2] == v2[2]:
    #         return False
    #     return True
    #
    # def check255(self,v):
    #     if v >= 255:
    #         return 255
    #     return v
    #
    # def filter(self, img):
    #     ft = cv2.imread('ra.png')
    #     for i in range(0,len(img)):
    #         for j in range(0,len(img[0])):
    #             if [img[i][j][0],img[i][j][1],img[i][j][2]] !=[255,255,255] and [img[i][j][0],img[i][j][1],img[i][j][2]] !=[0,0,0]:
    #                 # 명도 사용하기
    #                 img[i][j][0] = img[i][j][0] + ft[i][j][0]
    #                 img[i][j][1] = img[i][j][1] + ft[i][j][1]
    #                 img[i][j][2] = img[i][j][2] + ft[i][j][2]
    #
    #                 ## 그대로 가져오기
    #                 # img[i][j][0] = ft[i][j][0]
    #                 # img[i][j][1] = ft[i][j][1]
    #                 # img[i][j][2] = ft[i][j][2]

    def segmentation(self, img):
        segmentation_img = copy.deepcopy(img)
        offset = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        count = 0
        start_point = []

        for i in range(len(img)):
            for j in range(len(img[0])):
                if segmentation_img[i][j] == 255:
                    start_point.append([i,j])
                    count += 1

                    q = [[i,j]]
                    while q:
                        cur = q.pop(0)
                        x, y = cur[0], cur[1]
                        if x < 0 or y < 0:
                            pass
                        elif x > len(img) - 1 or y > len(img[0]) - 1:
                            pass
                        elif segmentation_img[x][y] != 255:
                            pass
                        else:
                            segmentation_img[x][y] = count
                            for i in range(4):
                                q.append([x + offset[i][0], y + offset[i][1]])
        return [segmentation_img, count]

    def segmentation_image_show(self,origin_img, segmentation_img , target):
        color_img = copy.deepcopy(origin_img)
        # print(count) # 세그먼트 개수 출력
        # [4,2,173] # 체리색

        color_count = self.return_size(copy.deepcopy(segmentation_img),3)
        if target == 0:
            # 사과
            color = [0,0,255]
            for i in range(len(segmentation_img)):
                for j in range(len(segmentation_img[0])):
                    if segmentation_img[i][j] != 0 and segmentation_img[i][j] != 255 and segmentation_img[i][j] == color_count[0]:
                        color_img[i][j] = color
        elif target == 1:
            # 체리
            color = [4,2,173]
            for seg_cnt in range(2):
                for i in range(len(segmentation_img)):
                    for j in range(len(segmentation_img[0])):
                        if segmentation_img[i][j] != 0 and segmentation_img[i][j] != 255 and segmentation_img[i][j] == color_count[seg_cnt]:
                            color_img[i][j] = color
        elif target == 2:
            # 토마토
            color = [[0,0,255],[0,255,0]]
            for seg_cnt in range(2):
                for i in range(len(segmentation_img)):
                    for j in range(len(segmentation_img[0])):
                        if segmentation_img[i][j] != 0 and segmentation_img[i][j] != 255 and segmentation_img[i][j] == color_count[seg_cnt]:
                            color_img[i][j] = color[seg_cnt]
        return color_img

    def return_size(self,img, return_num):
        count_list = [0] * 255
        for i in range(len(img)):
            for j in range(len(img[0])):
                if img[i][j] != 255 and img[i][j] != 0 and img[i][j] != 1:
                    count_list[img[i][j]] += 1

        count_sort_list = []
        for i in range(return_num):
            count_sort_list.append(count_list.index(max(count_list)))
            count_list[count_sort_list[i]] = 0
        return count_sort_list