import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QVBoxLayout, QFileDialog, QLabel, QComboBox, QPushButton , QSlider
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from helper_function.compile_qrc import compile_qrc
from classes.imageViewer import ImageViewer
from classes.componentsViewer import ComponentViewer
from classes.customImage import CustomImage
from classes.controller import Controller
from classes.modesEnum import RegionMode , Mode
from copy import copy
import cv2
import logging

# compile_qrc()

logging.basicConfig(
    filename='app.log',
    filemode='a',  # Append mode
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.logger = logging.getLogger(self.__class__.__name__)
        loadUi('main.ui', self)
        self.setWindowTitle('Image Mixer')
        self.setWindowIcon(QIcon('icons_setup\icons\logo.png'))
        
        self.image_viewer_frame_1 = self.findChild(QFrame, 'image1')
        self.components_viewer_frame_1 = self.findChild(QFrame, 'image1Frequancy')
        self.image_viewer_1 = ImageViewer()
        self.components_viewer_1 = ComponentViewer()
        self.components_viewer_frame_1.layout().addWidget(self.components_viewer_1)
        self.image_viewer_frame_1.layout().addWidget(self.image_viewer_1)
        
        self.image_viewer_frame_2 = self.findChild(QFrame, 'image2')
        self.components_viewer_frame_2 = self.findChild(QFrame, 'image2Frequency')
        self.image_viewer_2 = ImageViewer()
        self.components_viewer_2 = ComponentViewer()
        self.components_viewer_frame_2.layout().addWidget(self.components_viewer_2)
        self.image_viewer_frame_2.layout().addWidget(self.image_viewer_2)
        
        self.image_viewer_frame_3 = self.findChild(QFrame, 'image3')
        self.components_viewer_frame_3 = self.findChild(QFrame, 'image3Frequency')
        self.image_viewer_3 = ImageViewer()
        self.components_viewer_3 = ComponentViewer()
        self.components_viewer_frame_3.layout().addWidget(self.components_viewer_3)
        self.image_viewer_frame_3.layout().addWidget(self.image_viewer_3)
        
        self.image_viewer_frame_4 = self.findChild(QFrame, 'image4')
        self.components_viewer_frame_4 = self.findChild(QFrame, 'image4Frequency')
        self.image_viewer_4 = ImageViewer()
        self.components_viewer_4 = ComponentViewer()
        self.components_viewer_frame_4.layout().addWidget(self.components_viewer_4)
        self.image_viewer_frame_4.layout().addWidget(self.image_viewer_4)
        
        self.output_viewer_frame_1 = self.findChild(QFrame, 'output1Frame')
        self.output_viewer_1 = ImageViewer()
        self.output_viewer_frame_1.layout().addWidget(self.output_viewer_1)
        
        self.output_viewer_frame_2 = self.findChild(QFrame, 'output2Frame')
        self.output_viewer_2 = ImageViewer()
        self.output_viewer_frame_2.layout().addWidget(self.output_viewer_2)
        
        self.convert_button = self.findChild(QPushButton , "convertButton")
        self.convert_button.clicked.connect(self.mix_and_view)
        
        self.output_dispaly_combobox = self.findChild(QComboBox , "displayComboBox")
        self.output_dispaly_combobox.currentIndexChanged.connect(self.set_output_viewport)
        self.current_output_viewport = 0
        
        self.region_mode_combobox = self.findChild(QComboBox , "regionComboScale")
        self.region_mode_combobox.currentIndexChanged.connect(self.set_current_region_mode)
        self.current_region_mode = RegionMode.FULL
        
        self.current_mode_combobox = self.findChild(QComboBox , "modeComboBox")
        self.current_mode_combobox.currentIndexChanged.connect(self.set_current_mode)

        self.image1_weight_slider = self.findChild( QSlider , "image1Slider")
        self.image1_weight_slider.setRange(0,100)
        self.image1_weight_slider.sliderMoved.connect(self.set_image1_weight)
        
        
        self.image2_weight_slider = self.findChild( QSlider , "image2Slider")
        self.image2_weight_slider.setRange(0,100)
        self.image2_weight_slider.sliderMoved.connect(self.set_image2_weight)
        
        self.image3_weight_slider = self.findChild( QSlider , "image3Slider")
        self.image3_weight_slider.setRange(0,100)
        self.image3_weight_slider.sliderMoved.connect(self.set_image3_weight)
        
        self.image4_weight_slider = self.findChild( QSlider , "image4Slider")
        self.image4_weight_slider.setRange(0,100)
        self.image4_weight_slider.sliderMoved.connect(self.set_image4_weight)
        
        # Initialize the weights labels
        self.image1_weight_label = self.findChild(QLabel , "image1Loading")
        self.image2_weight_label = self.findChild(QLabel , "image2Loading")
        self.image3_weight_label = self.findChild(QLabel , "image3Loading")
        self.image4_weight_label = self.findChild(QLabel , "image4Loading")
        
        self.list_of_combo_boxes = []
        for i in range(1,5):
            index = copy(i)
            combo_box = self.findChild(QComboBox, f"image{i}ComboBox")
            self.list_of_combo_boxes.append(combo_box)
            
        
        
        self.list_of_images = [CustomImage(), CustomImage(), CustomImage(), CustomImage()]
        self.list_of_image_viewers = [self.image_viewer_1, self.image_viewer_2, self.image_viewer_3, self.image_viewer_4]
        self.list_of_component_viewers = [self.components_viewer_1, self.components_viewer_2, self.components_viewer_3, self.components_viewer_4]
        self.list_of_output_viewers = [self.output_viewer_1 , self.output_viewer_2]
        
        self.controller = Controller(self.list_of_images, self.list_of_component_viewers, self.list_of_image_viewers, self.list_of_combo_boxes , self.list_of_output_viewers)
        self.logger.info("Controller initialized with provided components")
        self.controller.list_of_images = self.list_of_images
        self.controller.list_of_component_viewers = self.list_of_component_viewers
        self.controller.list_of_image_viewers = self.list_of_image_viewers
        self.controller.list_of_combo_boxes = self.list_of_combo_boxes
        self.controller.Mixer.current_mode = Mode.MAGNITUDE_PHASE
        
        # Setting the mode of each image
        self.list_of_combo_boxes[0].currentIndexChanged.connect(self.set_image1_current_mode)
        self.list_of_combo_boxes[1].currentIndexChanged.connect(self.set_image2_current_mode)
        self.list_of_combo_boxes[2].currentIndexChanged.connect(self.set_image3_current_mode)
        self.list_of_combo_boxes[3].currentIndexChanged.connect(self.set_image4_current_mode)
        
        # Setting the slider of each image
        
        
        #setting the double click handlers
        for i, viewer in enumerate(self.list_of_image_viewers):
            viewer.set_double_click_handler(lambda i=i: self.load_image(i))
        
        
        
        
    def load_image(self, viewer_number):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open Image File', '', 'Image Files (*.jpeg *.jpg *.png *.bmp *.gif);;All Files (*)')
        self.logger.info(f"Selected file: {file_path}")

        print(viewer_number)
        if file_path:
            if file_path.endswith('.jpeg') or file_path.endswith('.jpg'):
                
                image = cv2.imread(file_path)
                if image is not None:
                    self.logger.info(f"Image loaded successfully for viewer {viewer_number}")
                    new_image = CustomImage(image)
                    self.list_of_images[viewer_number] = new_image
                    self.list_of_image_viewers[viewer_number].current_image = new_image
                    self.list_of_component_viewers[viewer_number].current_image = new_image
                    self.controller.set_current_images_list()
                    self.controller.image_weights[viewer_number] = 0
                else:
                    self.logger.error(f"Failed to load image from {file_path}")
        else:
            self.logger.warning("No file selected")
    
    def set_output_viewport(self , new_output_viewport):
        self.logger.info(f"Output viewport changed to: {new_output_viewport}")

        self.current_output_viewport = new_output_viewport
    
    def set_current_region_mode(self,new_region):
        if(new_region == 0 ):
            self.current_region_mode = RegionMode.FULL
        elif(new_region == 1 ):
            self.current_region_mode = RegionMode.INNER
        elif(new_region == 2 ):
            self.current_region_mode = RegionMode.OUTER
    
    def set_current_mode(self, new_mode_index):
        if(new_mode_index == 0):
            self.controller.Mixer.current_mode = Mode.MAGNITUDE_PHASE
            for combobox in self.list_of_combo_boxes:
                combobox.clear()
                combobox.addItems(["Magnitude" , "Phase"])
        elif(new_mode_index == 1):
            self.controller.Mixer.current_mode = Mode.REAL_IMAGINARY
            for combobox in self.list_of_combo_boxes:
                combobox.clear()
                combobox.addItems(["Real" , "Imaginary"])
    
    def set_image1_current_mode(self , mode_index):
        if (self.controller.Mixer.current_mode == Mode.MAGNITUDE_PHASE):
            if(mode_index == 0):
                self.controller.Mixer.images_modes[0] = Mode.MAGNITUDE
            elif(mode_index == 1):
                self.controller.Mixer.images_modes[0] = Mode.PHASE
        elif (self.controller.Mixer.current_mode == Mode.REAL_IMAGINARY):
            if(mode_index == 0):
                self.controller.Mixer.images_modes[0] = Mode.REAL
            elif(mode_index == 1):
                self.controller.Mixer.images_modes[0] = Mode.IMAGINARY
    
    def set_image2_current_mode(self , mode_index):
        if (self.controller.Mixer.current_mode == Mode.MAGNITUDE_PHASE):
            if(mode_index == 0):
                self.controller.Mixer.images_modes[1] = Mode.MAGNITUDE
            elif(mode_index == 1):
                self.controller.Mixer.images_modes[1] = Mode.PHASE
        elif (self.controller.Mixer.current_mode == Mode.REAL_IMAGINARY):
            if(mode_index == 0):
                self.controller.Mixer.images_modes[1] = Mode.REAL
            elif(mode_index == 1):
                self.controller.Mixer.images_modes[1] = Mode.IMAGINARY
                            
    def set_image3_current_mode(self , mode_index):
        if (self.controller.Mixer.current_mode == Mode.MAGNITUDE_PHASE):
            if(mode_index == 0):
                self.controller.Mixer.images_modes[2] = Mode.MAGNITUDE
            elif(mode_index == 1):
                self.controller.Mixer.images_modes[2] = Mode.PHASE
        elif (self.controller.Mixer.current_mode == Mode.REAL_IMAGINARY):
            if(mode_index == 0):
                self.controller.Mixer.images_modes[2] = Mode.REAL
            elif(mode_index == 1):
                self.controller.Mixer.images_modes[2] = Mode.IMAGINARY
                            
    def set_image4_current_mode(self , mode_index):
        if (self.controller.Mixer.current_mode == Mode.MAGNITUDE_PHASE):
            if(mode_index == 0):
                self.controller.Mixer.images_modes[3] = Mode.MAGNITUDE
            elif(mode_index == 1):
                self.controller.Mixer.images_modes[3] = Mode.PHASE
        elif (self.controller.Mixer.current_mode == Mode.REAL_IMAGINARY):
            if(mode_index == 0):
                self.controller.Mixer.images_modes[3] = Mode.REAL
            elif(mode_index == 1):
                self.controller.Mixer.images_modes[3] = Mode.IMAGINARY
    
    def set_image1_weight(self , slider_value):
        self.logger.debug(f"Image 1 weight slider moved to: {slider_value}")
        self.controller.image_weights[0] = slider_value
        self.image1_weight_label.setText(f'{slider_value} %')
    
    def set_image2_weight(self , slider_value):
        self.logger.debug(f"Image 2 weight slider moved to: {slider_value}")
        self.controller.image_weights[1] = slider_value
        self.image2_weight_label.setText(f'{slider_value} %')
    
    def set_image3_weight(self , slider_value):
        self.logger.debug(f"Image 3 weight slider moved to: {slider_value}")
        self.controller.image_weights[2] = slider_value
        self.image3_weight_label.setText(f'{slider_value} %')
    
    def set_image4_weight(self , slider_value):
        self.logger.debug(f"Image 4 weight slider moved to: {slider_value}")
        self.controller.image_weights[3] = slider_value
        self.image4_weight_label.setText(f'{slider_value} %')
    
    def mix_and_view(self):
        self.logger.info("Mixing images...")
        self.logger.debug(f"Current output viewport: {self.current_output_viewport}")
        self.logger.debug(f"Current region mode: {self.current_region_mode}")
        try:
            self.controller.mix_all(self.current_output_viewport, self.current_region_mode)
            self.logger.info("Mixing operation completed successfully")
        except Exception as e:
            self.logger.error(f"Error during mixing operation: {e}")
            raise


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())