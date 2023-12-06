#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: zhangjian
# date: 2023/7/13
import _queue
import logging
import os
import time
from queue import Queue
from threading import Thread

import cv2

from .files import makedirs
from .helper import get_time_str, setup_logger
from .timer import MyTimer, FPSRealTime

__all__ = ['FrameInfo', 'VideoReader']


class FrameInfo(object):
    def __init__(self, image, frame_idx=None, frame_elapsed_ms=None):
        self.image = image
        self.frame_idx = frame_idx
        self.frame_elapsed_ms = frame_elapsed_ms
        self.process_ret = None

    def get_image(self):
        return self.image

    def set_image(self, image):
        self.image = image

    def get_frame_idx(self):
        return self.frame_idx

    def get_frame_elapsed_s(self):
        return self.frame_elapsed_ms / 1000

    def get_frame_elapsed_ms(self):
        return self.frame_elapsed_ms

    def set_ret(self, result):
        self.process_ret = result

    def get_ret(self):
        return self.process_ret


class VideoReader(object):
    def __init__(self, video_input_param, auto_drop_frame=True, skip_frames=0, reload_video=True, log_name='demo'):
        self.video_input_param = video_input_param
        self.stopped = False
        self.skip_frames = skip_frames + 1
        self.auto_drop_frame = auto_drop_frame
        self.reload_video = reload_video
        self.mylogger = logging.getLogger(log_name)
        self.mylogger.info('VideoStreamReader init done.')
        self.cap_load_done = False

    def load_camera(self, ):
        cap = cv2.VideoCapture(self.video_input_param)
        self.mylogger.info(
            f'Video is {"opened." if cap.isOpened() else "not opened."}')
        self.cap_fps = cap.get(5)
        self.cap_height, self.cap_width = cap.get(cv2.CAP_PROP_FRAME_HEIGHT), cap.get(
            cv2.CAP_PROP_FRAME_WIDTH)
        self.mylogger.info(
            f'Video stream FPS: {self.cap_fps}\tshape: ({self.cap_height}, {self.cap_width})')
        self.mylogger.info(
            f'Load video stream from {self.video_input_param} done.')
        self.cap_load_done = True
        return cap

    def run(self, queue_i):
        self.mylogger.info('VideoReader running ...')
        cap = self.load_camera()
        frame_idx = 0
        mytimer = MyTimer()

        while not self.stopped:
            mytimer.restart()
            ret = cap.grab()
            frame_idx += 1
            if not ret:
                self.mylogger.info(
                    f'---VideoReader--- Grab NONE FRAME, Cap is opened: {cap.isOpened()}'
                )
                if self.reload_video:
                    cap = self.load_camera()
                else:
                    self.mylogger.info(
                        f'---VideoReader--- Grab NONE FRAME, exit.'
                    )
                    self.stopped = True
                continue
            if self.auto_drop_frame:
                if queue_i.full():
                    continue
            else:
                if frame_idx % self.skip_frames != 0:
                    continue
            ret, image = cap.retrieve()
            self.mylogger.debug(
                f'---VideoReader--- cap read elapsed: {mytimer.elapsed():.2f}ms'
            )
            if ret:
                frame = FrameInfo(image=image,
                                  frame_idx=frame_idx,
                                  frame_elapsed_ms=cap.get(
                                      cv2.CAP_PROP_POS_MSEC))
                queue_i.put(frame)
                self.mylogger.debug(
                    f'---VideoReader--- Put Frame-{frame_idx} to the list ---- len:{queue_i.qsize()} '
                    f'elapsed: {mytimer.elapsed():.2f}ms')
            else:
                self.mylogger.info(
                    f'---VideoReader--- READ NONE FRAME, Cap is opened: {cap.isOpened()}'
                )
                if self.reload_video:
                    cap = self.load_camera()

        cap.release()
        self.mylogger.info('Camera is closed.')

    def stop(self):
        self.stopped = True

    def _reset_cap_writer(self, record_save_root, fps, width, height):
        time_str = get_time_str()
        video_save_path = os.path.join(record_save_root, time_str[:10], time_str + '.avi')
        makedirs(os.path.dirname(video_save_path))

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        cap_writer = cv2.VideoWriter(video_save_path, fourcc, fps, (int(width), int(height)))
        self.mylogger.info('CapWriter reset.')
        return cap_writer, video_save_path

    def show_video(self, **kwargs):
        self._show_or_record(show=True, **kwargs)

    def record_video(self, record_save_root, **kwargs):
        kwargs['record_save_root'] = record_save_root
        self._show_or_record(record=True, **kwargs)

    def save_frames(self, save_image_root, **kwargs):
        kwargs['save_image_root'] = save_image_root
        self._show_or_record(save_image=True, **kwargs)

    def _show_or_record(self, show=False, record=False, save_image=False, **kwargs):
        queue_i = Queue(maxsize=1)
        video_reader_worker = Thread(target=self.run, kwargs={"queue_i": queue_i}, daemon=True)
        video_reader_worker.start()

        record_save_root = kwargs.get('record_save_root', None)
        fps = kwargs.get('fps', None)
        width = kwargs.get('width', None)
        height = kwargs.get('height', None)
        record_write_interval_m = kwargs.get('record_write_interval_m', -1)

        show_window_name = kwargs.get('show_window_name', 'Demo')
        show_window_width = kwargs.get('show_window_width', 1920)
        show_window_height = kwargs.get('show_window_height', 1080)
        show_fps = kwargs.get('show_fps', True)


        timeout = kwargs.get('timeout', 2)

        save_image_root = kwargs.get('save_image_root', None)
        while True:
            if self.cap_load_done:
                break

        if fps is None:
            fps = self.cap_fps
        if width is None:
            width = self.cap_width
        if height is None:
            height = self.cap_height

        if save_image_root:
            makedirs(save_image_root)

        run_time_total = -1
        mytimer = MyTimer()
        mytimer2 = MyTimer()
        if record:
            cap_writer, video_save_path = self._reset_cap_writer(record_save_root, fps, width, height)
        if show:
            cv2.namedWindow(show_window_name, 0)  # 0可调大小，注意：窗口名必须imshow里面的一窗口名一直
            cv2.resizeWindow(show_window_name, show_window_width, show_window_height)  # 设置宽和高
            if show_fps:
                fps_obj = FPSRealTime(buffer_len=150)

        while True:
            if record and record_write_interval_m > 0 and mytimer2.elapsed(restart=False,
                                                                           unit='min') >= record_write_interval_m:
                mytimer2.restart()
                cap_writer.release()
                cap_writer, video_save_path = self._reset_cap_writer(record_save_root, fps, width, height)
            mytimer.restart()
            try:
                frame = queue_i.get(timeout=timeout)
                frame_idx = frame.get_frame_idx()
                self.mylogger.debug(
                    f'---show_or_record--- Get Frame-{frame_idx} *** last elapsed: {run_time_total:.1f}ms')
                image_bgr = frame.get_image()
                if width is not None and height is not None:
                    image_bgr = cv2.resize(image_bgr, (int(width), int(height)))

            except:
                frame = None
            if frame is not None:
                if save_image:
                    save_path = os.path.join(save_image_root, f'{frame_idx:08d}.jpg')
                    cv2.imwrite(save_path, image_bgr)
                if record:
                    cap_writer.write(image_bgr)
                if show:
                    if show_fps:
                        # h, w = image_bgr.shape[:2]
                        # position = (int(0.02 * w), int(0.04 * h))
                        position = (20, 25)
                        fps = fps_obj.get_fps(number=1)
                        cv2.putText(image_bgr, f'FPS: {fps}', position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
                    cv2.imshow(show_window_name, image_bgr)
                    cv2.setMouseCallback(show_window_name, onMouse)
            else:
                self.mylogger.warning(
                    f'---show_or_record--- read image timeout, break.')
                break
            run_time_total = mytimer.elapsed(unit='ms')
        if record:
            cap_writer.release()
            self.mylogger.info(f'CapWriter is released.\n video is saved to {video_save_path}')

        if show:
            cv2.destroyAllWindows()



def onMouse(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f'({x}, {y})')




def main():
    pass


if __name__ == '__main__':
    main()
