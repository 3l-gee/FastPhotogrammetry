use std::io::BufReader;
use std::fs::File;
use image::{self, DynamicImage};
use std::path::Path;

extern crate cv;

pub struct MetadataStruct {
    pub camera : String,
    pub focal : f32
    //TODO more Metadata
}
 
pub struct DescriptorStruct {
    pub keypoints : Vec<cv::feature::akaze::KeyPoint>,
    pub descriptors : Vec<cv::BitArray<64>>,
    pub method : String
}

pub struct ImageStruct {
    pub name : String,
    pub img_raw: image::DynamicImage,
    pub img_processed: Option<image::DynamicImage>,
    pub metadata : MetadataStruct,
    pub descriptor : Option<DescriptorStruct>,
    //TODO more Image parameters
}

pub trait ImageProcessing {
    fn load(path: &str) -> Result<ImageStruct, String>;
    fn info(&self);
    fn grayscale(image_input: DynamicImage) -> Result<DynamicImage, image::ImageError>;
    fn scale(image_input: DynamicImage) -> Result<DynamicImage, image::ImageError>;
    fn save(&self) -> Result<(), String>;
    fn show(&self);
    fn process(&mut self);
    fn compute(&mut self) -> Result<(), String>;
    fn draw(&mut self) -> Result<(), String>; 
}


impl ImageProcessing for ImageStruct {
    fn load(path: &str) -> Result<ImageStruct, String> {
        let name = path.split("/").last().unwrap_or_default().to_string();
        // Load the image from the specified file path
        let file = match File::open(path) {
            Ok(file) => file,
            Err(err) => return Err(format!("Failed to open image file: {}", err)),
        };

        let reader = BufReader::new(file);
        let format = match image::ImageFormat::from_path(path) {
            Ok(format) => format,
            Err(err) => return Err(format!("Failed to find the image format: {}", err)),
        };

        let img = match image::load(reader,    format) {
            Ok(img) => img,
            Err(err) => return Err(format!("Failed to decode image: {}", err)),
        };

        // Extract image metadata
        let metadata = MetadataStruct {
            //TODO PLACEHOLDER
            camera: String::from("Example Camera"),
            focal: 50.0,
        };

        // Create the Image struct with loaded image data and metadata
        Ok(ImageStruct {
            name,
            img_raw: img,
            img_processed: None,
            metadata,
            descriptor: None
        })
    }

    fn info(&self) {
        println!("Image Name: {}", self.name);
        println!("Image Format: {:?}", self.img_raw.color());
        println!("Image Dimensions: {} x {}", self.img_raw.width(), self.img_raw.height());
        println!("Camera: {}", self.metadata.camera);
        println!("Focal Length: {}", self.metadata.focal);
        // Print more information as needed
    }

    fn process(&mut self) {
        
        match ImageStruct::scale(self.img_raw.clone()) {
            Ok(scaled_image) => {
                match ImageStruct::grayscale(scaled_image) {
                    Ok(greyscale_image) => {
                        self.img_processed = Some(greyscale_image);
                    },
                    Err(err) => eprintln!("Error grayscaling image: {}", err),
                }
            },
            Err(err) => eprintln!("Error scaling image: {}", err),
        }
    }

    fn compute(&mut self) -> Result<(), String> {
        let akaze = cv::feature::akaze::Akaze::dense();

        // Ensure img_processed is Some; otherwise return an Err
        let image = match &self.img_processed {
            Some(image) => image,
            None => return Err("img_processed is None".to_string()),
        };

        // Proceed with the computation since we now have an image
        let (keypoints, descriptors) = akaze.extract(image);

        let descriptor = DescriptorStruct {
            keypoints,
            descriptors,
            method: "AKAZE".to_string(),
        };
        self.descriptor = Some(descriptor);

        Ok(())
    }

    fn grayscale(image: DynamicImage) -> Result<DynamicImage, image::ImageError> {
        Ok(image.grayscale())
    }

    fn scale(image : DynamicImage) -> Result<DynamicImage, image::ImageError> {
        Ok(image.resize(500, 500,  image::imageops::FilterType::Nearest))
    }

    fn draw(&mut self) -> Result<(), String> {  
        let descriptor = match &self.descriptor {
            Some(descriptor) => descriptor,
            None => return Err("descriptor is None".to_string()),
        };

        let image = match &self.img_processed {
            Some(image) => image,
            None => return Err("img_processed is None".to_string()),
        };

        for keypoint in descriptor.keypoints {
            let (x, y) = (keypoint.pt.x as i32, keypoint.pt.y as i32);
            cv::
            
            
            image::imageproc::drawing::draw_cross_mut(
                &mut image,
                image::Rgba([0, 255, 255, 128]),
                x,
                y,
            );
            
        }
        Ok(())
    }

    fn show(){

    }

    fn save(&self) -> Result<(), String> {
        let output_path = Path::new("C:/Users/Raphael_Gerth/Documents/HOME/FUNTIMES_Rust/photogrametry/output").join("test.png");

        match &self.img_processed {
            Some(image) => {
                match image.save_with_format(output_path, image::ImageFormat::Png) {
                    Ok(_) => Ok(()),
                    Err(e) => Err(format!("Failed to save image: {}", e)),
                }

            },
            None => Err("img_processed is None".to_string()),
        }
    }
}

