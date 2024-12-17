from classes.viewer import Viewer
import numpy as np 
from PyQt5.QtWidgets import QFileDialog, QLabel
import pyqtgraph as pg 
from pyqtgraph import RectROI, mkBrush
from classes.CustomROI import CustomRectROI
from classes.controller import Controller
from classes.modesEnum import RegionMode

from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsPolygonItem
from PyQt5.QtGui import QPolygonF 
from PyQt5.QtCore import QPointF, QRectF
class ComponentViewer(Viewer):
    def __init__(self):
        super().__init__()
        
        self.roi = CustomRectROI([0, 0], [20, 20], pen='r', movable=True, resizable=True)
        self.roi.addScaleHandle([1, 1], [0, 0])  # Add handles for resizing
        self.roi.addScaleHandle([0, 0], [1, 1])
        self.roi.hide()
        

        
        # Add ROI to the view and connect its signal
        self.getView().addItem(self.roi)
        # self.roi.sigRegionChanged.connect(Controller.handle_roi_change(self.roi))
        view_range = self.getView().viewRange()

        self.xmin, self.xmax = view_range[0]  
        self.ymin, self.ymax = view_range[1]  
        
        # self.show_grid(x=False, y=False)  
    

    def update_plot(self, plot_type:str):
        if self.current_image.modified_image[2].ndim == 2:
            if hasattr(self, 'imageItem'):
                self.imageItem.setImage(self.current_image.modified_image[2])
            # self.current_Image_Item = pg.ImageItem(self.current_image.modified_image[2])
            if plot_type == "Magnitude":
                magnitude = np.abs(self.current_image.modified_image_fourier_components).T
                magnitude_log = np.log1p(magnitude)  
                magnitude_normalized = (magnitude_log - np.min(magnitude_log)) * (255.0 / (np.max(magnitude_log) - np.min(magnitude_log)))
                magnitude_normalized = magnitude_normalized.astype(np.uint8)
                self.setImage(magnitude_normalized)
                
            elif plot_type == "Phase":
                phase = np.angle(self.current_image.modified_image_fourier_components).T
                phase_normalized = (phase + np.pi) * (255.0 / (2 * np.pi))  # Normalize to [0, 255]
                phase_normalized = phase_normalized.astype(np.uint8)
                self.setImage(phase_normalized)

            elif plot_type == "Real":
                real = self.current_image.modified_image_fourier_components.T.real
                real_clipped = np.clip(real, 1e-10, None)
                real_log = np.log1p(real_clipped)
                real_normalized = (real_log - np.min(real_log)) * (255.0 / (np.max(real_log) - np.min(real_log)))
                real_normalized = real_normalized.astype(np.uint8)
                self.setImage(real_normalized)
            
                
            elif plot_type == "Imaginary":
                imaginary = self.current_image.modified_image_fourier_components.T.imag
                imaginary_clipped = np.clip(imaginary, 1e-10, None)
                imaginary_log = np.log1p(imaginary_clipped)
                imaginary_normalized = (imaginary_log - np.min(imaginary_log)) * (255.0 / (np.max(imaginary_log) - np.min(imaginary_log)))
                imaginary_normalized = imaginary_normalized.astype(np.uint8)
                self.setImage(imaginary_normalized)
                
            self.roi.show()
            self.getView().autoRange()
            self.getView().setMouseEnabled(x=False, y=False)
            view_range = self.getView().viewRange()

        # Extract the minimum x and y values
            self.xmin, self.xmax = view_range[0]  # x range (xmin, xmax)
            self.ymin, self.ymax = view_range[0]
            
            self.roi.maxBounds = self.getImageItem().boundingRect()  
            # self.roi.max_bounds = QRectF(self.roi.maxBounds.topLeft(), self.roi.maxBounds.size())
    
    def size_handle(self):
        pass
    