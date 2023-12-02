import argparse
import os
import typing
from argparse import ArgumentParser
from glob import glob

import cryolo.imagereader as imagereader
import imageio
import matplotlib.pyplot as plt
import numpy as np

from cryolo.CoordsIO import read_cbox_boxfile, Filament
from tqdm import tqdm

from cryoloBM.bmtool import BMTool


class CBOXDirections(BMTool):

    def get_command_name(self) -> str:
        return "cbox_directions"

    def create_parser(self, parentparser: ArgumentParser) -> ArgumentParser:
        parser_cdir = parentparser.add_parser(
            self.get_command_name(),
            help="Plots the estimated directions when directions are predicted",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

        cdir_required_group = parser_cdir.add_argument_group(
            "Required arguments",
            "Plots the estimated directions when directions are predicted",
        )

        cdir_required_group.add_argument(
            "-m",
            "--micrographs",
            required=True,
            nargs='+',
            help="Path to micrograph files. Can be folder or a wildmask. In case of a wildmask, enclose the argument in single quotes like -c 'path/to/mics/*.mrc'.",
        )

        cdir_required_group.add_argument(
            "-c",
            "--coordinates",
            required=True,
            nargs='+',
            help="Path to CBOX files. Can be folder or a wildmask. In case of a wildmask, enclose the argument in single quotes like -c 'path/to/star/*.cbox'.",
        )

        cdir_required_group.add_argument(
            "-t",
            "--threshold",
            required=True,
            type=float,
            help="Threshold applied to CBOX before creating plot",
        )

        cdir_required_group.add_argument(
            "-o",
            "--output",
            required=True,
            help="Output folder where to write the plots.",
        )

    @staticmethod
    def get_paths(paths: typing.List[str], fallback_wildcard: str):
        files = paths
        if len(paths)==1:
            if os.path.isdir(paths[0]):
                path_for_glob = os.path.join(paths[0], fallback_wildcard)
            else:
                path_for_glob = paths[0]
            files = glob(path_for_glob)
        return files

    def is_tomo(self, pth):
        boxdata = read_cbox_boxfile(pth)
        if isinstance(boxdata[0], Filament):
            return boxdata[0].boxes[0].z != None
        else:
            return boxdata[0].z != None

    def make_plot(self, img, boxdata, thresh, z=None) -> np.array:
        if isinstance(boxdata[0], Filament):
            boxdata_help = []
            for fil in boxdata:
                boxdata_help.extend(fil.boxes)
            boxdata = boxdata_help
        boxdata = [box for box in boxdata if box.c > thresh]
        if z is not None:
            boxdata = [box for box in boxdata if int(box.z) == z]
        fig2 = plt.figure(figsize=(10, 10))
        ax3 = fig2.add_subplot(111)
        ax3.imshow(img, interpolation='none', cmap='gray')
        ax3.set_xlim((0, img.shape[1]))
        ax3.set_ylim((0, img.shape[0]))
        arrlength = 1
        for box in boxdata:
            a = box.meta['angle']
            arr = arrlength * np.array([np.cos(a), np.sin(a)])

            plt.arrow(box.x + box.w / 2, box.y + box.h / 2, arr[0], arr[1], head_width=int(np.max(img.shape)*0.01), color="black", overhang=1)

        fig2.canvas.draw()
        data = np.frombuffer(fig2.canvas.tostring_rgb(), dtype=np.uint8)
        data = data.reshape(fig2.canvas.get_width_height()[::-1] + (3,))
        data = data[:,:,1]
        plt.close(fig2)
        return data


    def run(self, args):
        mic_pth = args.micrographs
        coords_path = args.coordinates
        outpth = args.output
        thresh = args.threshold
        mics = CBOXDirections.get_paths(mic_pth, "*.mrc")
        coords = CBOXDirections.get_paths(coords_path, "*.cbox")
        os.makedirs(outpth, exist_ok=True)

        for mic in mics:
            imgs = []
            micname = os.path.splitext(os.path.basename(mic))[0]
            c = [c for c in coords if micname in c]
            img = imagereader.image_read(mic)
            is_tomo = False
            if len(np.squeeze(img).shape)==3:
                is_tomo=True
            mean = np.mean(img)
            sd = np.std(img)
            img = (img - mean) / sd

            boxdata = read_cbox_boxfile(c[0])
            if is_tomo:
                for i in tqdm(range(img.shape[0]), desc=micname):
                    imgflip = np.flipud(img[i,:,:])
                    data = self.make_plot(imgflip, boxdata, thresh,z=i)
                    imgs.append(data)
            else:
                img = np.flipud(img)
                data = self.make_plot(img, boxdata, thresh)
                imgs.append(data)




            if len(imgs)>1:
                img_conc = np.concatenate([np.expand_dims(i, axis=0) for i in imgs])
                imgpth = os.path.join(outpth, micname + ".tiff")
                print("Write", imgpth)
                imageio.mimwrite(imgpth, img_conc)
            else:
                imgpth = os.path.join(outpth, micname + ".png")
                print("Write", imgpth)
                imageio.imwrite(imgpth, imgs[0])