import open3d
from pathlib import Path
import os.path
import numpy as np
import matplotlib.pyplot as plt
import sys
from shutil import copyfile
from visualization import VisOpen3D

def GenerateDepthImageFromLidar(fname, strDColor, strDGray):
    # remember to adjust here for rendering image size
    w = 848
    h = 480
    print("reading"+str(fname))
    pcd = open3d.io.read_point_cloud(str(fname))

    # create window
    window_visible = False

    vis = VisOpen3D(width=w, height=h, visible=window_visible)

    # point cloud
    vis.add_geometry(pcd)

    # update view
    # vis.update_view_point(intrinsic, extrinsic)

    # save view point to file
    # vis.save_view_point("view_point.json")
    vis.load_view_point("view_point_outster.json")


    # capture images
    depth = vis.capture_depth_float_buffer(show=False)
    image = vis.capture_screen_float_buffer(show=False)

    # save to file
    basefname = os.path.basename(fname)
    basefname = basefname[:-4]+".png"
    # print(basefname)
    vis.capture_screen_image(strDColor+"/dc_"+os.path.basename(basefname))
    vis.capture_depth_image(strDGray+"/dg_"+os.path.basename(basefname))

    # draw camera
    if window_visible:
        vis.load_view_point("view_point.json")
        intrinsic = vis.get_view_point_intrinsics()
        extrinsic = vis.get_view_point_extrinsics()
        print(intrinsic)
        print(extrinsic)
        vis.update_view_point(intrinsic, extrinsic)
        vis.draw_camera(intrinsic, extrinsic, scale=0.5, color=[0.8, 0.2, 0.8])

    if window_visible:
        vis.load_view_point("view_point.json")
        vis.run()

    del vis

def main(arg):

    lenArg = len(arg)
    print(lenArg," and ",arg) 

    # input is the folder path
    folder = arg[0]
    if(folder[-1]=="/" ):
      folder1 = folder[:-1]

    # folder for saving images
    strDColor = folder+"depth_color"
    strDGray = folder+"depth_Gray"

    if not os.path.exists(strDColor):
      os.mkdir(strDColor)
    if not os.path.exists(strDGray):
      os.mkdir(strDGray)

    # all files in the dir path
    for fname in sorted(Path(arg[0]).rglob('*')):
      GenerateDepthImageFromLidar(fname, strDColor, strDGray)

if __name__ == "__main__":
  main(sys.argv[1:])
